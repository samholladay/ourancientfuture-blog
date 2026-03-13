#!/usr/bin/env python3
"""
Substack Article Scraper
Scrapes articles from a Substack blog and organizes them by topic.
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
import hashlib

class SubstackScraper:
    def __init__(self, config_path='config.json'):
        """Initialize the scraper with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.substack_url = self.config['substack_url']
        self.articles_dir = 'data/articles'
        self.media_dir = 'media/articles'
        self.articles_index = 'data/articles.json'
        
        # Create necessary directories
        os.makedirs(self.articles_dir, exist_ok=True)
        os.makedirs(self.media_dir, exist_ok=True)
        os.makedirs('data', exist_ok=True)
    
    def fetch_article_list(self):
        """Fetch the list of articles from Substack."""
        print(f"Fetching articles from {self.substack_url}...")
        
        # Substack archive page
        archive_url = urljoin(self.substack_url, '/archive')
        
        try:
            response = requests.get(archive_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching archive: {e}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Find article links (Substack structure may vary)
        # This looks for common patterns in Substack archives
        article_links = soup.find_all('a', href=re.compile(r'/p/'))
        
        seen_urls = set()
        for link in article_links:
            url = urljoin(self.substack_url, link.get('href'))
            # Remove query parameters and fragments
            clean_url = url.split('?')[0].split('#')[0]
            
            if clean_url not in seen_urls:
                seen_urls.add(clean_url)
                articles.append(clean_url)
        
        print(f"Found {len(articles)} articles")
        return articles
    
    def categorize_article(self, title, content, url):
        """
        Categorize article based on keywords in title and content.
        Uses the category mappings from config.json.
        """
        text = (title + ' ' + content).lower()
        
        category_keywords = self.config.get('category_keywords', {})
        category_scores = {}
        
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or 'uncategorized'
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'uncategorized'
    
    def extract_preview(self, content_elem):
        """
        Extract the first 3 paragraphs as HTML preview.
        """
        from copy import copy
        
        # Find all paragraph elements
        paragraphs = content_elem.find_all('p')
        
        # Get first 3 non-empty paragraphs
        preview_paras = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip empty paragraphs or very short ones (likely not content)
            if text and len(text) > 20:
                preview_paras.append(str(p))
                if len(preview_paras) >= 3:
                    break
        
        # Join paragraphs
        preview_html = '\n'.join(preview_paras)
        
        return preview_html
    
    def clean_content(self, content_elem):
        """
        Clean up Substack-specific formatting issues.
        """
        # Remove Subscribe buttons and subscription CTAs
        for elem in content_elem.find_all(['button', 'a'], class_=re.compile(r'subscribe|subscription', re.I)):
            elem.decompose()
        
        # Remove subscribe forms
        for form in content_elem.find_all('form'):
            form.decompose()
        
        # Remove elements with subscribe-related text
        for elem in content_elem.find_all(text=re.compile(r'subscribe', re.I)):
            if elem.parent and elem.parent.name in ['button', 'a', 'div', 'p']:
                # Check if this is primarily a subscribe element
                parent_text = elem.parent.get_text(strip=True).lower()
                if 'subscribe' in parent_text and len(parent_text) < 200:
                    elem.parent.decompose()
        
        # Remove specific Substack subscription prompts
        for elem in content_elem.find_all(text=re.compile(r'Thanks for reading.*Subscribe', re.I | re.DOTALL)):
            if elem.parent:
                elem.parent.decompose()
        
        # Remove the first image if it appears at the very start (will be used as cover)
        first_img = content_elem.find('img')
        if first_img:
            # Check if image is at the start of content
            parent = first_img.parent
            # Remove the entire container (figure, div, etc.) if it's the first element
            if parent and not parent.find_previous_sibling():
                # Remove the parent container, not just the image
                if parent.name in ['figure', 'div', 'p']:
                    parent.decompose()
                else:
                    first_img.decompose()
        
        # Remove image expand/zoom buttons (common Substack pattern)
        # These are usually small buttons or links near images
        for img_container in content_elem.find_all(['div', 'figure'], class_=re.compile(r'image|picture|photo', re.I)):
            # Remove buttons within image containers (but NOT links)
            buttons = img_container.find_all('button')
            for button in buttons:
                button.decompose()
            
            # Unwrap links around images (Substack lightbox links)
            # These are <a> tags that wrap the image for lightbox functionality
            for link in img_container.find_all('a', class_=re.compile(r'image-link', re.I)):
                # Unwrap the link, keeping its contents (the image)
                link.unwrap()
            
            # Unwrap picture elements - extract the img tag
            for picture in img_container.find_all('picture'):
                img = picture.find('img')
                if img:
                    # Replace picture with just the img
                    picture.replace_with(img)
            
            # Remove extra wrapper divs (like image2-inset)
            for div in img_container.find_all('div', class_=re.compile(r'image2-inset|image-inset', re.I)):
                div.unwrap()
        
        # Clean up image captions
        for figcaption in content_elem.find_all('figcaption'):
            # Remove any buttons or links in captions
            for elem in figcaption.find_all(['button', 'a']):
                elem.decompose()
            
            # Clean up caption formatting - remove extra spans and divs
            caption_text = figcaption.get_text(strip=True)
            figcaption.clear()
            figcaption.string = caption_text
        
        # Remove anchor links from headings (the tiny buttons)
        for heading in content_elem.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            # Remove anchor links
            for anchor in heading.find_all('a', class_=re.compile(r'anchor|header-anchor', re.I)):
                anchor.decompose()
            
            # Remove any buttons in headings
            for button in heading.find_all('button'):
                button.decompose()
            
            # Convert all headings to h3 for consistent styling
            if heading.name != 'h3':
                heading.name = 'h3'
        
        # Remove any remaining standalone buttons that might be Substack UI elements
        for button in content_elem.find_all('button'):
            # Keep buttons that are clearly part of content (rare)
            if not button.get_text(strip=True):
                button.decompose()
        
        return content_elem
    
    def download_image(self, img_url, article_slug):
        """Download an image and return the local path."""
        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()
            
            # Generate filename from URL
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            ext = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
            filename = f"{article_slug}_{url_hash}{ext}"
            
            filepath = os.path.join(self.media_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Return relative path for web use
            return f"media/articles/{filename}"
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")
            return img_url  # Return original URL if download fails
    
    def scrape_article(self, url):
        """Scrape a single article from Substack."""
        print(f"Scraping: {url}")
        
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching article: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract article metadata
        title_elem = soup.find('h1', class_='post-title') or soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else 'Untitled'
        
        # Extract subtitle
        subtitle_elem = soup.find('h3', class_='subtitle') or soup.find('p', class_='subtitle')
        subtitle = subtitle_elem.get_text(strip=True) if subtitle_elem else ''
        
        # Extract date
        date_elem = soup.find('time') or soup.find('span', class_='post-date')
        date_str = date_elem.get('datetime', '') if date_elem else ''
        if not date_str and date_elem:
            date_str = date_elem.get_text(strip=True)
        
        # Try to parse date
        try:
            if 'T' in date_str:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
        
        # Extract article content
        content_elem = soup.find('div', class_='available-content') or \
                      soup.find('div', class_='body') or \
                      soup.find('article')
        
        if not content_elem:
            print(f"Could not find content for {url}")
            return None
        
        # Create article slug from URL
        slug = url.rstrip('/').split('/')[-1]
        
        # Extract cover image BEFORE cleaning (get the first image)
        cover_img = None
        first_img = content_elem.find('img')
        if first_img:
            img_url = first_img.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                cover_img = self.download_image(img_url, slug)
        
        # Clean up Substack-specific formatting
        content_elem = self.clean_content(content_elem)
        
        # Download remaining images and update src attributes
        for img in content_elem.find_all('img'):
            img_url = img.get('src')
            if img_url:
                # Make URL absolute
                img_url = urljoin(url, img_url)
                local_path = self.download_image(img_url, slug)
                img['src'] = local_path
        
        # Get HTML content
        content_html = str(content_elem)
        
        # Get plain text for categorization
        content_text = content_elem.get_text(strip=True)
        
        # Extract preview (first 3 paragraphs as HTML)
        preview_html = self.extract_preview(content_elem)
        
        # Categorize article
        category = self.categorize_article(title, content_text, url)
        
        # Create article object
        article = {
            'id': slug,
            'title': title,
            'subtitle': subtitle,
            'date': formatted_date,
            'category': category,
            'url': url,
            'cover_image': cover_img,
            'content': content_html,
            'excerpt': content_text[:200] + '...' if len(content_text) > 200 else content_text,
            'preview': preview_html,
            'meta_description': ''  # To be filled in manually later
        }
        
        # Save article content to file
        article_file = os.path.join(self.articles_dir, f"{slug}.json")
        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        return article
    
    def scrape_all(self):
        """Scrape all articles and create index."""
        article_urls = self.fetch_article_list()
        
        if not article_urls:
            print("No articles found. Please check your Substack URL.")
            return
        
        articles_metadata = []
        
        for url in article_urls:
            article = self.scrape_article(url)
            if article:
                # Store metadata (including preview) in index
                articles_metadata.append({
                    'id': article['id'],
                    'title': article['title'],
                    'subtitle': article['subtitle'],
                    'date': article['date'],
                    'category': article['category'],
                    'cover_image': article['cover_image'],
                    'excerpt': article['excerpt'],
                    'preview': article['preview'],
                    'meta_description': article['meta_description']
                })
        
        # Sort by date (newest first)
        articles_metadata.sort(key=lambda x: x['date'], reverse=True)
        
        # Save articles index
        with open(self.articles_index, 'w', encoding='utf-8') as f:
            json.dump(articles_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully scraped {len(articles_metadata)} articles!")
        print(f"Articles index saved to {self.articles_index}")
        
        # Print category breakdown
        categories = {}
        for article in articles_metadata:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nCategory breakdown:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

def main():
    """Main function to run the scraper."""
    scraper = SubstackScraper()
    scraper.scrape_all()

if __name__ == '__main__':
    main()
