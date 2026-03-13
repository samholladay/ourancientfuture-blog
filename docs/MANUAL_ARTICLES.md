# Manual Article Creation Guide

You have **three ways** to add articles to your blog:

1. **Scrape from Substack** (automatic)
2. **Write in Markdown** (recommended for manual articles)
3. **Create JSON directly** (advanced)

## Method 1: Scraping from Substack

This is covered in the main README. Simply run:

```bash
python3 scripts/scraper.py
```

## Method 2: Writing in Markdown (Recommended)

This is the easiest way to manually create articles.

### Step 1: Install Dependencies

Make sure you have the markdown package installed:

```bash
pip install -r requirements.txt
```

### Step 2: Create Your Article

Create a new Markdown file in the `drafts/` directory:

```bash
cp drafts/template.md drafts/my-new-article.md
```

Edit the file with your favorite text editor:

```markdown
---
title: My Amazing Article
subtitle: This is what the article is about
category: tech
date: 2026-03-05
cover_image: images/cover.jpg
tags: [technology, tutorial]
---

# Introduction

Write your article here using Markdown...
```

### Step 3: Add Images (Optional)

If your article has images:

1. Create an `images/` folder next to your Markdown file:
   ```bash
   mkdir drafts/images
   ```

2. Add your images there:
   ```
   drafts/
   ├── my-new-article.md
   └── images/
       ├── cover.jpg
       └── diagram.png
   ```

3. Reference them in your Markdown:
   ```markdown
   ![Description](images/diagram.png)
   ```

The script will automatically copy images to `media/articles/` and update paths.

### Step 4: Create the Article

Run the creation script:

```bash
python3 scripts/create_article.py create drafts/my-new-article.md
```

That's it! Your article is now live on your site.

### Frontmatter Fields

The frontmatter (between the `---` markers) supports these fields:

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `title` | Yes | Article title | `My Article` |
| `subtitle` | No | Subtitle/description | `A deep dive into...` |
| `category` | Yes | Category (tech/literature/film) | `tech` |
| `date` | No | Publication date (YYYY-MM-DD) | `2026-03-05` |
| `cover_image` | No | Path to cover image | `images/cover.jpg` |
| `tags` | No | List of tags | `[tag1, tag2]` |
| `slug` | No | Custom URL slug | `my-custom-slug` |

### Markdown Features

You can use all standard Markdown features:

#### Headings
```markdown
# Heading 1
## Heading 2
### Heading 3
```

#### Text Formatting
```markdown
**Bold text**
*Italic text*
`Inline code`
```

#### Links
```markdown
[Link text](https://example.com)
```

#### Images
```markdown
![Alt text](images/photo.jpg)
```

#### Lists
```markdown
- Unordered item
- Another item

1. Ordered item
2. Another item
```

#### Code Blocks
````markdown
```python
def hello():
    print("Hello!")
```
````

#### Blockquotes
```markdown
> This is a quote
```

#### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

## Method 3: Direct JSON Creation (Advanced)

If you prefer, you can create article JSON files directly.

### Step 1: Create Article JSON

Create a file in `data/articles/` named `your-slug.json`:

```json
{
  "id": "your-slug",
  "title": "Your Article Title",
  "subtitle": "Optional subtitle",
  "date": "2026-03-05",
  "category": "tech",
  "url": "article.html?id=your-slug",
  "cover_image": "media/articles/cover.jpg",
  "content": "<p>Your HTML content here...</p>",
  "excerpt": "A brief excerpt...",
  "tags": ["tag1", "tag2"]
}
```

### Step 2: Update Index

Manually add an entry to `data/articles.json`:

```json
[
  {
    "id": "your-slug",
    "title": "Your Article Title",
    "subtitle": "Optional subtitle",
    "date": "2026-03-05",
    "category": "tech",
    "cover_image": "media/articles/cover.jpg",
    "excerpt": "A brief excerpt..."
  }
]
```

Keep the array sorted by date (newest first).

## Managing Articles

### List All Articles

```bash
python3 scripts/create_article.py list
```

### Update an Article

Just edit the Markdown file and run the create command again:

```bash
python3 scripts/create_article.py create drafts/my-article.md
```

It will overwrite the existing article.

### Delete an Article

```bash
python3 scripts/create_article.py delete article-slug
```

This removes the article from both `data/articles/` and the index.

## Workflow Examples

### Quick Article

```bash
# Copy template
cp drafts/template.md drafts/quick-thoughts.md

# Edit the file
nano drafts/quick-thoughts.md

# Create article
python3 scripts/create_article.py create drafts/quick-thoughts.md
```

### Article with Images

```bash
# Create article directory
mkdir -p drafts/my-photo-essay/images

# Create markdown file
nano drafts/my-photo-essay/article.md

# Add images
cp ~/Pictures/photo1.jpg drafts/my-photo-essay/images/

# Create article
python3 scripts/create_article.py create drafts/my-photo-essay/article.md
```

### Batch Create

```bash
# Create multiple articles
for file in drafts/*.md; do
    python3 scripts/create_article.py create "$file"
done
```

## Tips

### Organizing Drafts

Keep your drafts organized:

```
drafts/
├── tech/
│   ├── article1.md
│   └── article2.md
├── literature/
│   └── book-review.md
└── film/
    └── movie-analysis.md
```

### Preview Before Publishing

You can preview your Markdown locally before creating the article:
- Use a Markdown editor with preview (VS Code, Typora, etc.)
- Or use online tools like StackEdit

### Version Control

Keep your drafts in version control:

```bash
git add drafts/
git commit -m "Add new article draft"
```

### Image Optimization

Optimize images before adding them:

```bash
# Resize large images
convert large-image.jpg -resize 1200x image.jpg

# Compress
jpegoptim --max=85 image.jpg
```

### Scheduling

To schedule articles for future publication:

1. Set a future date in the frontmatter
2. Create the article
3. It will appear in the list but sorted by date

Or use a cron job to create articles automatically:

```bash
# In crontab
0 9 * * * cd /path/to/blog && python3 scripts/create_article.py create drafts/scheduled.md
```

## Troubleshooting

### "markdown package not installed"

Install it:
```bash
pip install markdown
```

### Images not showing

- Check that image paths are relative to the Markdown file
- Ensure images exist in the specified location
- Check console for error messages

### Article not appearing

- Verify the article was created in `data/articles/`
- Check that `data/articles.json` was updated
- Clear browser cache
- Check browser console for errors

### Formatting issues

- Ensure frontmatter is properly formatted (YAML syntax)
- Check that there are exactly three dashes (`---`) before and after frontmatter
- Validate your Markdown syntax

## Comparison: Scraper vs Manual

| Feature | Scraper | Manual (Markdown) |
|---------|---------|-------------------|
| **Speed** | Fast for bulk | Quick for single |
| **Control** | Limited | Full control |
| **Formatting** | Substack's | Your choice |
| **Images** | Auto-download | Manual selection |
| **Editing** | Re-scrape | Edit & recreate |
| **Best for** | Importing existing | New content |

## Best Practices

1. **Use meaningful slugs**: They become part of the URL
2. **Add alt text to images**: Good for accessibility
3. **Keep drafts folder organized**: Use subdirectories
4. **Test locally first**: Preview before creating
5. **Backup your drafts**: Use version control
6. **Optimize images**: Compress before adding
7. **Use consistent categories**: Stick to your defined categories
8. **Write good excerpts**: If not provided, first 200 chars are used

## Next Steps

- Read `CUSTOMIZATION.md` to customize article styling
- Read `DEPLOYMENT.md` to publish your site
- Check `README.md` for general information
