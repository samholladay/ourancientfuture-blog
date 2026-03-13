#!/usr/bin/env python3
"""
Generate HTML pages for translated articles
Creates article pages and index pages for each language
"""

import json
import os
from pathlib import Path
import shutil

LANGUAGES = {
    'es': 'Spanish',
    'ru': 'Russian',
    'de': 'German',
    'fr': 'French',
    'cn': 'Chinese'
}

def generate_article_pages_for_language(lang_code):
    """Generate article HTML pages for a specific language."""
    
    lang_dir = Path(lang_code)
    articles_dir = lang_dir / 'articles'
    articles_dir.mkdir(parents=True, exist_ok=True)
    
    # Load translated articles index
    index_file = lang_dir / 'data' / 'articles.json'
    if not index_file.exists():
        print(f"No articles found for {lang_code}")
        return 0
    
    with open(index_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Read the English template
    with open('article.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Update paths for language subdirectory (two levels deep: /es/articles/)
    template = template.replace('href="styles/', 'href="../../styles/')
    template = template.replace('src="scripts/', 'src="../../scripts/')
    template = template.replace('href="index.html"', 'href="../../index.html"')
    template = template.replace('href="about.html"', 'href="../../about.html"')
    template = template.replace('href="/favicon', 'href="../../favicon')
    template = template.replace('href="/apple-touch-icon', 'href="../../apple-touch-icon')
    template = template.replace('href="/site.webmanifest"', 'href="../../site.webmanifest"')
    
    # Generate pages
    for article in articles:
        output_file = articles_dir / f"{article['id']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template)
    
    return len(articles)

def generate_index_page_for_language(lang_code, lang_name):
    """Generate index page for a specific language."""
    
    lang_dir = Path(lang_code)
    lang_dir.mkdir(exist_ok=True)
    
    # Read the English index template
    with open('index.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Update paths for language subdirectory (one level deep: /es/)
    template = template.replace('href="styles/', 'href="../styles/')
    template = template.replace('src="scripts/', 'src="../scripts/')
    template = template.replace('href="about.html"', 'href="../about.html"')
    template = template.replace('href="/favicon', 'href="../favicon')
    template = template.replace('href="/apple-touch-icon', 'href="../apple-touch-icon')
    template = template.replace('href="/site.webmanifest"', 'href="../site.webmanifest"')
    
    # Update data path in the HTML
    template = template.replace('src="scripts/main.js"', f'src="../scripts/main.js" data-lang="{lang_code}"')
    
    # Write index page
    output_file = lang_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"  ✓ Created /{lang_code}/index.html")

def generate_all_language_pages():
    """Generate all HTML pages for all languages."""
    
    print("Generating language-specific pages...")
    print()
    
    for lang_code, lang_name in LANGUAGES.items():
        print(f"{lang_name} ({lang_code}):")
        
        # Generate article pages
        count = generate_article_pages_for_language(lang_code)
        if count > 0:
            print(f"  ✓ Generated {count} article pages in /{lang_code}/articles/")
            
            # Generate index page
            generate_index_page_for_language(lang_code, lang_name)
        else:
            print(f"  ⚠ No translated articles found")
        
        print()
    
    print("✓ All language pages generated!")

if __name__ == '__main__':
    generate_all_language_pages()
