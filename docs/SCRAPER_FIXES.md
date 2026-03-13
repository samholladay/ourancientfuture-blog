# Substack Scraper - Formatting Fixes

## Issues Fixed

The scraper now automatically cleans up Substack-specific formatting issues:

### 1. ✅ Subscribe Buttons Removed
- Removes all Subscribe buttons at the bottom of articles
- Removes subscription forms and CTAs
- Cleans up any subscribe-related elements

### 2. ✅ Duplicate Cover Images Fixed
- The first image is extracted as the cover image
- That same image is then removed from the article content
- No more duplicate images at the top

### 3. ✅ Image Expand Buttons Removed
- Removes the two expand/zoom buttons below each image
- Cleans up image containers and lightbox elements
- Keeps only the image itself

### 4. ✅ Image Captions Cleaned
- Removes buttons and links from captions
- Strips extra formatting (spans, divs)
- Keeps only clean caption text

### 5. ✅ Heading Anchor Buttons Removed
- Removes the tiny anchor link buttons next to headings
- Removes any other buttons in headings
- Keeps headings clean

### 6. ✅ Consistent Heading Styling
- All headings in articles are converted to `<h3>`
- Ensures consistent styling across all articles
- Uses the Header3 styling from your CSS

## How It Works

The scraper now follows this process:

1. **Fetch article** from Substack
2. **Extract cover image** (before cleaning)
3. **Clean content**:
   - Remove subscribe elements
   - Remove first image (already used as cover)
   - Remove image buttons
   - Clean captions
   - Remove heading anchors
   - Convert headings to h3
4. **Download remaining images**
5. **Save cleaned article**

## Re-scraping Existing Articles

To apply these fixes to articles you've already scraped:

```bash
python3 scripts/scraper.py
```

The scraper will re-fetch and clean all articles with the new formatting.

## Manual Override

If you need to manually edit an article after scraping:

1. Find the article JSON in `data/articles/[slug].json`
2. Edit the `content` field
3. The changes will appear immediately on your site

## Additional Cleaning

If you notice other Substack elements that need removal, you can add them to the `clean_content()` method in `scripts/scraper.py`.

Common patterns to look for:
- Class names containing: `subscribe`, `button`, `anchor`, `expand`, `zoom`
- Form elements
- Standalone buttons
- Extra wrapper divs

## Testing

After re-scraping, check:
- [ ] No subscribe buttons at article bottom
- [ ] Cover image appears once (at top)
- [ ] No expand buttons below images
- [ ] Clean image captions
- [ ] No anchor buttons on headings
- [ ] All headings use h3 styling
