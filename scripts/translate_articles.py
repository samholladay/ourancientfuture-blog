#!/usr/bin/env python3
"""
Translate articles into multiple languages using Google Translate (free tier via googletrans)
Generates translated versions under /es/, /ru/, /de/, /fr/, /cn/ directories
"""

import json
import os
from pathlib import Path
from googletrans import Translator
import time

# Language configurations
LANGUAGES = {
    'es': {'name': 'Spanish', 'code': 'es'},
    'ru': {'name': 'Russian', 'code': 'ru'},
    'de': {'name': 'German', 'code': 'de'},
    'fr': {'name': 'French', 'code': 'fr'},
    'cn': {'name': 'Chinese', 'code': 'zh-cn'}
}

def translate_text(text, target_lang, translator, max_retries=3):
    """Translate text to target language with retry logic."""
    if not text or text.strip() == '':
        return text
    
    for attempt in range(max_retries):
        try:
            # Split long text into chunks to avoid API limits
            max_length = 4500
            if len(text) > max_length:
                # Split by paragraphs
                paragraphs = text.split('\n')
                translated_paragraphs = []
                
                for para in paragraphs:
                    if para.strip():
                        translated = translator.translate(para, dest=target_lang)
                        translated_paragraphs.append(translated.text)
                        time.sleep(0.3)  # Increased delay for rate limiting
                    else:
                        translated_paragraphs.append('')
                
                return '\n'.join(translated_paragraphs)
            else:
                translated = translator.translate(text, dest=target_lang)
                time.sleep(0.3)  # Increased delay
                return translated.text
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"  Warning: Translation error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  Error: Translation failed after {max_retries} attempts - {e}")
                return text  # Return original text if all retries fail
    
    return text

def translate_html_content(html, target_lang, translator):
    """Translate HTML content while preserving tags."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Translate text in paragraphs
    for p in soup.find_all('p'):
        # Get all text content, not just direct string
        text = p.get_text(strip=False)
        if text and text.strip():
            translated = translate_text(text, target_lang, translator)
            # Clear the paragraph and set new text
            p.clear()
            p.string = translated
    
    # Translate headings
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = heading.get_text(strip=False)
        if text and text.strip():
            translated = translate_text(text, target_lang, translator)
            heading.clear()
            heading.string = translated
    
    # Translate list items
    for li in soup.find_all('li'):
        text = li.get_text(strip=False)
        if text and text.strip():
            translated = translate_text(text, target_lang, translator)
            li.clear()
            li.string = translated
    
    # Translate blockquotes
    for blockquote in soup.find_all('blockquote'):
        text = blockquote.get_text(strip=False)
        if text and text.strip():
            translated = translate_text(text, target_lang, translator)
            blockquote.clear()
            blockquote.string = translated
    
    # Translate figcaptions (image captions)
    for figcaption in soup.find_all('figcaption'):
        text = figcaption.get_text(strip=False)
        if text and text.strip():
            translated = translate_text(text, target_lang, translator)
            figcaption.clear()
            figcaption.string = translated
    
    return str(soup)

def translate_article(article, target_lang, lang_code, translator):
    """Translate a single article."""
    print(f"  Translating to {LANGUAGES[lang_code]['name']}...")
    
    translated_article = article.copy()
    
    # Translate title
    translated_article['title'] = translate_text(article['title'], target_lang, translator)
    
    # Translate subtitle
    if article.get('subtitle'):
        translated_article['subtitle'] = translate_text(article['subtitle'], target_lang, translator)
    
    # Translate excerpt
    if article.get('excerpt'):
        translated_article['excerpt'] = translate_text(article['excerpt'], target_lang, translator)
    
    # Translate preview
    if article.get('preview'):
        translated_article['preview'] = translate_html_content(article['preview'], target_lang, translator)
    
    # Translate content
    if article.get('content'):
        translated_article['content'] = translate_html_content(article['content'], target_lang, translator)
    
    # Add language metadata
    translated_article['language'] = lang_code
    translated_article['original_id'] = article['id']
    
    return translated_article

def generate_translated_pages():
    """Generate translated versions of all articles."""
    
    # Load articles
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Initialize translator
    translator = Translator()
    
    # Process each language
    for lang_code, lang_info in LANGUAGES.items():
        print(f"\n{'='*60}")
        print(f"Translating to {lang_info['name']} ({lang_code})")
        print(f"{'='*60}")
        
        # Create language directories
        lang_dir = Path(lang_code)
        lang_dir.mkdir(exist_ok=True)
        
        articles_dir = lang_dir / 'articles'
        articles_dir.mkdir(exist_ok=True)
        
        data_dir = lang_dir / 'data' / 'articles'
        data_dir.mkdir(parents=True, exist_ok=True)
        
        translated_index = []
        
        # Translate each article
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] {article['title']}")
            
            # Load full article data
            article_file = f"data/articles/{article['id']}.json"
            if os.path.exists(article_file):
                with open(article_file, 'r', encoding='utf-8') as f:
                    full_article = json.load(f)
            else:
                full_article = article
            
            # Translate
            translated = translate_article(full_article, lang_info['code'], lang_code, translator)
            
            # Save translated article data
            output_file = data_dir / f"{article['id']}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(translated, f, indent=2, ensure_ascii=False)
            
            # Add to index
            translated_index.append({
                'id': translated['id'],
                'title': translated['title'],
                'subtitle': translated.get('subtitle', ''),
                'date': translated['date'],
                'category': translated['category'],
                'cover_image': translated['cover_image'],
                'excerpt': translated.get('excerpt', ''),
                'preview': translated.get('preview', ''),
                'meta_description': translated.get('meta_description', ''),
                'language': lang_code
            })
            
            print(f"  ✓ Saved to {output_file}")
        
        # Save translated index
        index_file = lang_dir / 'data' / 'articles.json'
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(translated_index, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ {lang_info['name']} translation complete!")
        print(f"  Articles: {len(translated_index)}")
        print(f"  Location: /{lang_code}/")
    
    print(f"\n{'='*60}")
    print("All translations complete!")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("Article Translation Tool")
    print("This will translate all articles into multiple languages.")
    print("Note: This uses Google Translate and may take several minutes.")
    print("\nLanguages: Spanish, Russian, German, French, Chinese")
    
    response = input("\nContinue? (y/n): ")
    if response.lower() == 'y':
        generate_translated_pages()
    else:
        print("Translation cancelled.")
