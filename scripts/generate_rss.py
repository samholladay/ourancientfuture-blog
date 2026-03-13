#!/usr/bin/env python3
"""
Generate RSS feed for the blog
"""

import json
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_rss():
    """Generate RSS 2.0 feed from articles."""
    
    # Read config for site info
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    site_url = config.get('site_url', 'https://myblog.com')
    blog_title = config.get('blog_title', 'My Blog')
    blog_description = config.get('blog_description', 'A personal blog')
    author_name = config.get('author', {}).get('name', 'Blog Author')
    
    # Create RSS root
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    
    channel = SubElement(rss, 'channel')
    
    # Channel metadata
    SubElement(channel, 'title').text = blog_title
    SubElement(channel, 'link').text = site_url
    SubElement(channel, 'description').text = blog_description
    SubElement(channel, 'language').text = 'en-us'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    SubElement(channel, 'generator').text = 'Custom Blog Generator'
    
    # Self link
    atom_link = SubElement(channel, 'atom:link')
    atom_link.set('href', f'{site_url}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Load articles
    articles_index = 'data/articles.json'
    if not os.path.exists(articles_index):
        print("No articles found. Generate some articles first.")
        return
    
    with open(articles_index, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Add items (limit to 20 most recent)
    for article in articles[:20]:
        item = SubElement(channel, 'item')
        
        # Basic info
        SubElement(item, 'title').text = article['title']
        
        article_url = f"{site_url}/article.html?id={article['id']}"
        SubElement(item, 'link').text = article_url
        SubElement(item, 'guid').text = article_url
        
        # Description (use subtitle or excerpt)
        description = article.get('subtitle') or article.get('excerpt', '')
        SubElement(item, 'description').text = description
        
        # Author
        SubElement(item, 'author').text = f"noreply@example.com ({author_name})"
        
        # Category
        SubElement(item, 'category').text = article['category']
        
        # Publication date (RFC 822 format)
        try:
            pub_date = datetime.strptime(article['date'], '%Y-%m-%d')
            SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y 00:00:00 GMT')
        except:
            pass
        
        # Enclosure (cover image)
        if article.get('cover_image'):
            enclosure = SubElement(item, 'enclosure')
            enclosure.set('url', f"{site_url}/{article['cover_image']}")
            enclosure.set('type', 'image/jpeg')
        
        # Full content (if available)
        if os.path.exists(f"data/articles/{article['id']}.json"):
            with open(f"data/articles/{article['id']}.json", 'r', encoding='utf-8') as af:
                full_article = json.load(af)
                if full_article.get('content'):
                    content_encoded = SubElement(item, 'content:encoded')
                    content_encoded.text = f"<![CDATA[{full_article['content']}]]>"
    
    # Pretty print XML
    xml_string = minidom.parseString(tostring(rss)).toprettyxml(indent='  ')
    
    # Remove extra blank lines
    xml_string = '\n'.join([line for line in xml_string.split('\n') if line.strip()])
    
    # Write to file
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(xml_string)
    
    print(f"✓ RSS feed generated: feed.xml")
    print(f"  Total items: {min(len(articles), 20)}")
    print(f"  Feed URL: {site_url}/feed.xml")

if __name__ == '__main__':
    generate_rss()
