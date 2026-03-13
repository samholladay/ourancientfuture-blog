#!/usr/bin/env python3
"""
Generate individual HTML files for each article with clean URLs
Creates /articles/slug.html for each article
"""

import json
import os
from pathlib import Path

def generate_article_pages():
    """Generate individual HTML pages for each article."""
    
    # Load articles index
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Create articles directory if it doesn't exist
    articles_dir = Path('articles')
    articles_dir.mkdir(exist_ok=True)
    
    # Read the template
    with open('article.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Update paths for subdirectory
    # Change relative paths to work from /articles/ subdirectory
    template = template.replace('href="styles/', 'href="../styles/')
    template = template.replace('src="scripts/', 'src="../scripts/')
    template = template.replace('href="index.html"', 'href="../index.html"')
    template = template.replace('href="about.html"', 'href="../about.html"')
    template = template.replace('href="/favicon', 'href="../favicon')
    template = template.replace('href="/apple-touch-icon', 'href="../apple-touch-icon')
    template = template.replace('href="/site.webmanifest"', 'href="../site.webmanifest"')
    
    # Generate a page for each article
    for article in articles:
        slug = article['id']
        
        # Create the HTML file
        output_file = articles_dir / f"{slug}.html"
        
        # Write the modified template
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"Generated: {output_file}")
    
    print(f"\n✓ Generated {len(articles)} article pages in /articles/")
    print("  Articles are now accessible at /articles/slug.html")

if __name__ == '__main__':
    generate_article_pages()
