# Multi-Language Translation Guide

Your blog now supports automatic machine translation into 5 major languages!

## Supported Languages

- 🇪🇸 **Spanish** (`/es/`)
- 🇷🇺 **Russian** (`/ru/`)
- 🇩🇪 **German** (`/de/`)
- 🇫🇷 **French** (`/fr/`)
- 🇨🇳 **Chinese** (`/cn/`)

## How It Works

### URL Structure

Each language has its own directory:

```
English:  https://ourancientfuture.com/articles/napoleon.html
Spanish:  https://ourancientfuture.com/es/articles/napoleon.html
Russian:  https://ourancientfuture.com/ru/articles/napoleon.html
German:   https://ourancientfuture.com/de/articles/napoleon.html
French:   https://ourancientfuture.com/fr/articles/napoleon.html
Chinese:  https://ourancientfuture.com/cn/articles/napoleon.html
```

### Directory Structure

```
/
├── articles/           # English articles
├── es/
│   ├── index.html     # Spanish homepage
│   ├── articles/      # Spanish articles
│   └── data/          # Spanish article data
├── ru/
│   ├── index.html     # Russian homepage
│   ├── articles/      # Russian articles
│   └── data/          # Russian article data
└── ... (same for de, fr, cn)
```

## Setup

### 1. Install Dependencies

```bash
pip install googletrans==4.0.0rc1
```

Or update from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Translate Articles

Run the translation script:

```bash
python3 scripts/translate_articles.py
```

**Note:** This will:
- Translate ALL articles into ALL 5 languages
- Take several minutes (rate-limited to avoid API issues)
- Use Google Translate (free tier)
- Preserve HTML formatting and images

### 3. Generate Language Pages

After translation, generate the HTML pages:

```bash
python3 scripts/generate_language_pages.py
```

This creates:
- Index pages for each language
- Article pages for each language
- Proper path adjustments for subdirectories

### 4. Update Sitemap (Optional)

To include translated pages in your sitemap:

```bash
python3 scripts/generate_sitemap.py
```

## Usage

### Language Selector

A language selector appears in the navigation:

```
🌐 EN ▼
  🇬🇧 English
  🇪🇸 Español
  🇷🇺 Русский
  🇩🇪 Deutsch
  🇫🇷 Français
  🇨🇳 中文
```

Users can click to switch languages.

### Automatic Detection

The JavaScript automatically detects which language directory you're in and:
- Loads the correct translated articles
- Shows the correct language in the selector
- Links to articles in the same language

## Translation Quality

### What's Translated

✅ Article titles
✅ Article subtitles  
✅ Article content (all text)
✅ Article excerpts
✅ Article previews
✅ Metadata

### What's NOT Translated

❌ Images (paths preserved)
❌ Code blocks (preserved as-is)
❌ URLs and links
❌ HTML tags and structure
❌ Navigation menu items (hardcoded)

### Improving Translations

The translations use Google Translate, which is good but not perfect. To improve:

1. **Manual editing**: Edit the JSON files in each language directory
   ```bash
   nano es/data/articles/napoleon.json
   ```

2. **Professional translation**: Replace machine translations with professional ones

3. **Community contributions**: Accept pull requests from native speakers

## Workflow

### After Adding New Articles

1. Scrape or create new English articles:
   ```bash
   python3 scripts/scraper.py
   ```

2. Translate new articles:
   ```bash
   python3 scripts/translate_articles.py
   ```

3. Generate pages:
   ```bash
   python3 scripts/generate_language_pages.py
   ```

4. Update sitemap:
   ```bash
   python3 scripts/generate_sitemap.py
   ```

### Updating Existing Translations

If you edit an English article and want to update translations:

1. Delete the old translation:
   ```bash
   rm es/data/articles/article-slug.json
   rm ru/data/articles/article-slug.json
   # ... etc
   ```

2. Re-run translation script (it will translate missing articles)

## SEO Benefits

### Hreflang Tags

Each language version should have hreflang tags (to be added):

```html
<link rel="alternate" hreflang="en" href="https://ourancientfuture.com/articles/napoleon.html" />
<link rel="alternate" hreflang="es" href="https://ourancientfuture.com/es/articles/napoleon.html" />
<link rel="alternate" hreflang="ru" href="https://ourancientfuture.com/ru/articles/napoleon.html" />
```

### Benefits

- **Wider audience**: Reach non-English speakers
- **Better SEO**: Google ranks pages in user's language higher
- **More traffic**: Tap into Spanish, Russian, German, French, Chinese markets
- **International presence**: Establish authority in multiple regions

## Technical Details

### Translation API

Uses `googletrans` library:
- Free tier of Google Translate
- No API key required
- Rate-limited (0.1s delay between requests)
- May occasionally fail (retry if needed)

### Path Resolution

The JavaScript automatically handles paths based on directory depth:

- Root (`/`): `data/articles/`
- English (`/articles/`): `../data/articles/`
- Language (`/es/articles/`): `../../es/data/articles/`

### Related Posts

Related posts work within each language:
- Spanish articles show Spanish related posts
- Russian articles show Russian related posts
- etc.

## Troubleshooting

### Translation Fails

If translation fails:

```bash
# Install/reinstall googletrans
pip uninstall googletrans
pip install googletrans==4.0.0rc1
```

### Pages Don't Load

Check paths in browser console:
- Verify data files exist in language directories
- Check that paths are correct (../ for subdirectories)

### Language Selector Doesn't Work

- Clear browser cache
- Check that main.js is loaded
- Verify language selector HTML is present

## Future Enhancements

Potential improvements:

1. **Hreflang tags**: Add proper SEO tags
2. **Language detection**: Auto-redirect based on browser language
3. **Better translation**: Use DeepL or professional services
4. **Partial translation**: Only translate specific articles
5. **Translation memory**: Reuse translations for common phrases
6. **UI translation**: Translate navigation, buttons, etc.

## Cost

**Current setup: FREE**

- Uses free Google Translate API
- No API keys required
- No usage limits for personal blogs

**Professional alternatives:**

- DeepL API: €20/month for 500,000 characters
- Google Cloud Translation: $20 per million characters
- Professional translators: $0.10-0.30 per word

## Statistics

After translation, you'll have:

- **Original**: 9 English articles
- **Translated**: 45 additional articles (9 × 5 languages)
- **Total**: 54 articles across 6 languages
- **Reach**: ~2.5 billion additional potential readers

Your blog is now truly international! 🌍
