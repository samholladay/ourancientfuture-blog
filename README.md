# Personal Blog - Substack Scraper

A static website that scrapes and displays articles from your Substack blog, organized by topic with a beautiful, Substack-inspired design.

## Features

- 🎨 **Substack-inspired design** - Clean, readable typography and layout
- 📝 **Multiple content sources** - Scrape from Substack OR write in Markdown
- 🏷️ **Topic categorization** - Organize articles by Tech, Literature, Film, etc.
- 🖼️ **Photo gallery** - Add custom photos to your landing page
- 📱 **Responsive design** - Works beautifully on all devices
- 🚀 **Static site** - Fast, secure, and easy to host
- ✍️ **Easy article creation** - Write articles in Markdown, no HTML needed

## Project Structure

```
blog/
├── index.html              # Landing page
├── article.html            # Article template page
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── styles/
│   ├── main.css          # Main stylesheet
│   └── article.css       # Article page styles
├── scripts/
│   ├── scraper.py        # Python scraper for Substack
│   ├── create_article.py # Manual article creator (Markdown)
│   ├── main.js           # Landing page JavaScript
│   └── article.js        # Article page JavaScript
├── drafts/               # Write your articles here (Markdown)
│   ├── template.md       # Article template
│   └── example-article.md # Example article
├── media/
│   ├── gallery/          # Landing page photos (add your own)
│   └── articles/         # Article images (auto-downloaded)
├── data/
│   ├── articles.json     # Articles index (generated)
│   └── articles/         # Individual article data (generated)
└── docs/                 # Additional documentation
    ├── MANUAL_ARTICLES.md # Guide for manual article creation
    ├── DEPLOYMENT.md     # Deployment guide
    └── CUSTOMIZATION.md  # Customization guide
```

## Setup Instructions

### 1. Configure Your Blog

Edit `config.json` and update all settings:

```json
{
  "site_url": "https://yourdomain.com",
  "substack_url": "https://yoursubstack.substack.com",
  "blog_title": "Your Blog Name",
  "blog_description": "Your description",
  "hero_title": "Welcome to Your Blog",
  "hero_subtitle": "Your tagline",
  "author": {
    "name": "Your Name",
    "tagline": "Your professional tagline",
    "photo": "media/author.jpg",
    "bio": [
      "Your bio paragraph 1",
      "Your bio paragraph 2"
    ],
    "about_blog": [
      "About your blog paragraph 1"
    ],
    "social": {
      "twitter": "https://twitter.com/yourusername",
      "github": "https://github.com/yourusername",
      "linkedin": "https://linkedin.com/in/yourusername",
      "email": "mailto:your@email.com"
    }
  }
}
```

**Note:** The homepage and About page now dynamically load content from `config.json`!

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using pip3:

```bash
pip3 install -r requirements.txt
```

### 3. Add Articles

You have two options:

#### Option A: Scrape from Substack

```bash
python3 scripts/scraper.py
```

This will:
- Fetch all articles from your Substack
- Download article images
- Categorize articles by topic
- Generate `data/articles.json` and individual article files

#### Option B: Write Articles Manually

Write articles in Markdown (much easier than HTML!):

```bash
# Copy the template
cp drafts/template.md drafts/my-article.md

# Edit your article
nano drafts/my-article.md

# Create the article
python3 scripts/create_article.py create drafts/my-article.md
```

See `docs/MANUAL_ARTICLES.md` for detailed instructions.

### 4. Add Your Author Photo

1. Add your photo to `media/` as `author.jpg` (or update the path in config.json)
2. Recommended size: Square image, at least 500x500px

### 5. Add Gallery Photos (Optional)

1. Add your photos to `media/gallery/`
2. Update the `gallery_photos` array in `config.json`:

```json
"gallery_photos": [
  {
    "path": "media/gallery/your-photo.jpg",
    "caption": "Photo description"
  }
]
```

### 5. Test Locally (Optional)

Start a local server to preview your site:

```bash
python3 -m http.server 8000
```

Then visit: `http://localhost:8000`

### 6. Deploy Your Site

You can host this static site on:

- **GitHub Pages**: Push to a GitHub repo and enable Pages
- **Netlify**: Drag and drop your folder
- **Vercel**: Connect your Git repository
- **Your own server**: Upload via FTP/SFTP

## Customization

### Categories

Edit the `category_keywords` in `config.json` to customize how articles are categorized:

```json
"category_keywords": {
  "tech": ["technology", "software", "AI"],
  "literature": ["book", "novel", "author"],
  "film": ["movie", "cinema", "director"]
}
```

### Styling

- Edit `styles/main.css` for landing page styles
- Edit `styles/article.css` for article page styles
- CSS variables are defined in `:root` for easy theming

### Navigation

To add or remove categories, edit:
1. The navigation in `index.html`
2. The `category_keywords` in `config.json`

## Creating and Managing Articles

### Create a New Article

```bash
python3 scripts/create_article.py create drafts/my-article.md
```

### List All Articles

```bash
python3 scripts/create_article.py list
```

### Delete an Article

```bash
python3 scripts/create_article.py delete article-slug
```

### Update from Substack

To fetch new articles from your Substack:

```bash
python3 scripts/scraper.py
```

The scraper will:
- Fetch any new articles
- Update existing articles
- Maintain your categorization

For detailed instructions on writing articles, see `docs/MANUAL_ARTICLES.md`.

## Generate Feeds

### Generate RSS Feed

```bash
python3 scripts/generate_rss.py
```

This creates `feed.xml` with your 20 most recent articles.

### Generate Sitemap

```bash
python3 scripts/generate_sitemap.py
```

This creates `sitemap.xml` for search engines.

**Tip:** Run both after adding new articles!

## Domain Setup

1. Point your domain (myblog.com) to your hosting provider
2. Configure DNS settings:
   - For GitHub Pages: Add CNAME record
   - For Netlify/Vercel: Follow their domain setup guide
3. Enable HTTPS (usually automatic with modern hosts)

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Troubleshooting

### Scraper Issues

If the scraper doesn't find articles:
1. Verify your Substack URL in `config.json`
2. Check that your Substack is public
3. Substack's HTML structure may have changed - you may need to update the scraper

### Images Not Loading

- Check file paths in `config.json`
- Ensure images are in the correct directories
- Check browser console for 404 errors

### Articles Not Displaying

- Verify `data/articles.json` exists
- Check browser console for JavaScript errors
- Ensure you're serving the site (not just opening HTML files)

## Development

To develop locally, you can use Python's built-in server:

```bash
python3 -m http.server 8000
```

Then visit: `http://localhost:8000`

## License

This project is open source and available for personal use.

## Support

For issues or questions, please check:
1. This README
2. The `docs/` folder for additional documentation
3. Browser console for error messages
