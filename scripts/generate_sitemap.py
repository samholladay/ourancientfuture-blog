#!/usr/bin/env python3
"""
Generate sitemap.xml for SEO
"""

import json
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_sitemap():
    """Generate sitemap.xml from articles."""
    
    # Read config for base URL
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    base_url = config.get('site_url', 'https://myblog.com')
    
    # Create root element
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:news', 'http://www.google.com/schemas/sitemap-news/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    # Add homepage
    url = SubElement(urlset, 'url')
    SubElement(url, 'loc').text = base_url + '/'
    SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    SubElement(url, 'changefreq').text = 'daily'
    SubElement(url, 'priority').text = '1.0'
    
    # Add articles
    articles_index = 'data/articles.json'
    if os.path.exists(articles_index):
        with open(articles_index, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        for article in articles:
            url = SubElement(urlset, 'url')
            article_url = f"{base_url}/articles/{article['id']}.html"
            SubElement(url, 'loc').text = article_url
            SubElement(url, 'lastmod').text = article['date']
            SubElement(url, 'changefreq').text = 'monthly'
            SubElement(url, 'priority').text = '0.8'
            
            # Add image if available
            if article.get('cover_image'):
                image = SubElement(url, 'image:image')
                SubElement(image, 'image:loc').text = base_url + '/' + article['cover_image']
                SubElement(image, 'image:title').text = article['title']
    
    # Pretty print XML
    xml_string = minidom.parseString(tostring(urlset)).toprettyxml(indent='  ')
    
    # Remove extra blank lines
    xml_string = '\n'.join([line for line in xml_string.split('\n') if line.strip()])
    
    # Write to file
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_string)
    
    print(f"✓ Sitemap generated: sitemap.xml")
    print(f"  Total URLs: {len(articles) + 1 if os.path.exists(articles_index) else 1}")

if __name__ == '__main__':
    generate_sitemap()
