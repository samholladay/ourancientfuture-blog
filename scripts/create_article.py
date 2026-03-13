#!/usr/bin/env python3
"""
Manual Article Creator
Create articles from Markdown files without scraping.
"""

import json
import os
import sys
import re
from datetime import datetime
import shutil

try:
    import markdown
except ImportError:
    print("Error: markdown package not installed.")
    print("Install it with: pip install markdown")
    sys.exit(1)

class ArticleCreator:
    def __init__(self):
        self.articles_dir = 'data/articles'
        self.media_dir = 'media/articles'
        self.articles_index = 'data/articles.json'
        self.drafts_dir = 'drafts'
        
        # Create necessary directories
        os.makedirs(self.articles_dir, exist_ok=True)
        os.makedirs(self.media_dir, exist_ok=True)
        os.makedirs(self.drafts_dir, exist_ok=True)
        os.makedirs('data', exist_ok=True)
    
    def parse_frontmatter(self, content):
        """Parse YAML-style frontmatter from markdown."""
        frontmatter = {}
        body = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                body = parts[2].strip()
                
                # Parse simple key: value pairs
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        # Handle lists
                        if value.startswith('[') and value.endswith(']'):
                            value = [v.strip().strip('"').strip("'") 
                                   for v in value[1:-1].split(',')]
                        
                        frontmatter[key] = value
        
        return frontmatter, body
    
    def create_slug(self, title):
        """Create URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def process_images(self, html_content, article_slug, markdown_dir):
        """Process and copy images referenced in the article."""
        # Find all image tags
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        
        def replace_image(match):
            img_tag = match.group(0)
            img_src = match.group(1)
            
            # Skip if already absolute URL
            if img_src.startswith('http://') or img_src.startswith('https://'):
                return img_tag
            
            # Skip if already in media directory
            if img_src.startswith('media/'):
                return img_tag
            
            # Construct source path relative to markdown file
            src_path = os.path.join(markdown_dir, img_src)
            
            if os.path.exists(src_path):
                # Create destination filename
                ext = os.path.splitext(img_src)[1] or '.jpg'
                base_name = os.path.basename(img_src)
                dest_filename = f"{article_slug}_{base_name}"
                dest_path = os.path.join(self.media_dir, dest_filename)
                
                # Copy image
                shutil.copy2(src_path, dest_path)
                
                # Update image tag
                new_src = f"media/articles/{dest_filename}"
                new_tag = img_tag.replace(img_src, new_src)
                
                print(f"  Copied image: {img_src} -> {new_src}")
                return new_tag
            else:
                print(f"  Warning: Image not found: {src_path}")
                return img_tag
        
        return re.sub(img_pattern, replace_image, html_content)
    
    def create_from_markdown(self, markdown_file):
        """Create an article from a Markdown file."""
        print(f"Creating article from {markdown_file}...")
        
        if not os.path.exists(markdown_file):
            print(f"Error: File not found: {markdown_file}")
            return None
        
        # Read markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter and body
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract metadata
        title = frontmatter.get('title', 'Untitled')
        subtitle = frontmatter.get('subtitle', '')
        category = frontmatter.get('category', 'uncategorized')
        date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
        tags = frontmatter.get('tags', [])
        cover_image = frontmatter.get('cover_image', '')
        
        # Create slug
        slug = frontmatter.get('slug', self.create_slug(title))
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'fenced_code'])
        html_content = md.convert(body)
        
        # Process images
        markdown_dir = os.path.dirname(os.path.abspath(markdown_file))
        html_content = self.process_images(html_content, slug, markdown_dir)
        
        # Process cover image if specified
        if cover_image and not cover_image.startswith('http'):
            cover_src = os.path.join(markdown_dir, cover_image)
            if os.path.exists(cover_src):
                ext = os.path.splitext(cover_image)[1]
                dest_filename = f"{slug}_cover{ext}"
                dest_path = os.path.join(self.media_dir, dest_filename)
                shutil.copy2(cover_src, dest_path)
                cover_image = f"media/articles/{dest_filename}"
                print(f"  Copied cover image: {cover_image}")
        
        # Extract plain text for excerpt
        text_content = re.sub(r'<[^>]+>', '', html_content)
        excerpt = text_content[:200] + '...' if len(text_content) > 200 else text_content
        
        # Create article object
        article = {
            'id': slug,
            'title': title,
            'subtitle': subtitle,
            'date': date,
            'category': category,
            'url': f'article.html?id={slug}',
            'cover_image': cover_image,
            'content': html_content,
            'excerpt': excerpt,
            'tags': tags if isinstance(tags, list) else []
        }
        
        # Save article
        article_file = os.path.join(self.articles_dir, f"{slug}.json")
        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Article created: {slug}")
        
        # Update index
        self.update_index(article)
        
        return article
    
    def update_index(self, new_article):
        """Update the articles index with the new article."""
        # Load existing index
        if os.path.exists(self.articles_index):
            with open(self.articles_index, 'r', encoding='utf-8') as f:
                articles = json.load(f)
        else:
            articles = []
        
        # Remove old version if exists
        articles = [a for a in articles if a['id'] != new_article['id']]
        
        # Add new article metadata
        articles.append({
            'id': new_article['id'],
            'title': new_article['title'],
            'subtitle': new_article['subtitle'],
            'date': new_article['date'],
            'category': new_article['category'],
            'cover_image': new_article['cover_image'],
            'excerpt': new_article['excerpt']
        })
        
        # Sort by date (newest first)
        articles.sort(key=lambda x: x['date'], reverse=True)
        
        # Save index
        with open(self.articles_index, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Index updated")
    
    def delete_article(self, article_id):
        """Delete an article by ID."""
        article_file = os.path.join(self.articles_dir, f"{article_id}.json")
        
        if not os.path.exists(article_file):
            print(f"Error: Article not found: {article_id}")
            return False
        
        # Remove article file
        os.remove(article_file)
        
        # Update index
        if os.path.exists(self.articles_index):
            with open(self.articles_index, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            articles = [a for a in articles if a['id'] != article_id]
            
            with open(self.articles_index, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Article deleted: {article_id}")
        return True
    
    def list_articles(self):
        """List all articles."""
        if not os.path.exists(self.articles_index):
            print("No articles found.")
            return
        
        with open(self.articles_index, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"\nFound {len(articles)} articles:\n")
        for article in articles:
            print(f"  [{article['category']}] {article['title']}")
            print(f"    ID: {article['id']}")
            print(f"    Date: {article['date']}")
            print()

def main():
    """Main function."""
    creator = ArticleCreator()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create article:  python3 scripts/create_article.py create <markdown_file>")
        print("  Delete article:  python3 scripts/create_article.py delete <article_id>")
        print("  List articles:   python3 scripts/create_article.py list")
        print("\nExample:")
        print("  python3 scripts/create_article.py create drafts/my-article.md")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        if len(sys.argv) < 3:
            print("Error: Please specify a markdown file")
            sys.exit(1)
        
        markdown_file = sys.argv[2]
        creator.create_from_markdown(markdown_file)
        
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Please specify an article ID")
            sys.exit(1)
        
        article_id = sys.argv[2]
        creator.delete_article(article_id)
        
    elif command == 'list':
        creator.list_articles()
        
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
