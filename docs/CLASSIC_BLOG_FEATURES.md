# Classic Blog Features

Your blog now has a classic blog layout with all the traditional features readers expect.

## Features Overview

### 1. **Reverse Chronological Order**
- All posts are displayed newest first
- This is the standard blog format
- Already sorted by the scraper and article creator

### 2. **Archives Sidebar**
- Posts grouped by month and year
- Shows post count for each month
- Click any month to filter posts
- Automatically generated from your articles

### 3. **RSS Feed**
- Standard RSS 2.0 format
- Includes 20 most recent posts
- Full content in feed
- Cover images included
- Compatible with all RSS readers

### 4. **Sidebar Layout**
- Left sidebar with navigation
- Main content area for posts
- Fully responsive (sidebar moves below on mobile)

## Layout Structure

```
┌─────────────────────────────────────┐
│           Header / Nav              │
├─────────────────────────────────────┤
│           Hero Section              │
├──────────┬──────────────────────────┤
│ Sidebar  │   Main Content           │
│          │                          │
│ RSS      │   Latest Posts           │
│ Archives │   (Reverse Chrono)       │
│ Categories│                         │
└──────────┴──────────────────────────┘
```

## RSS Feed

### Generate the Feed

After adding or updating articles:

```bash
python3 scripts/generate_rss.py
```

This creates `feed.xml` in your root directory.

### Feed Features

- **Title**: Your blog title from config.json
- **Description**: Your blog description
- **20 Most Recent Posts**: Keeps feed size manageable
- **Full Content**: Readers can read in their RSS reader
- **Cover Images**: Included as enclosures
- **Categories**: Each post tagged with category
- **Proper Dates**: RFC 822 format for compatibility

### Feed URL

Your RSS feed will be available at:
```
https://yourdomain.com/feed.xml
```

### Promote Your Feed

The RSS button in the sidebar links to `feed.xml`. Users can:
- Click to subscribe in their browser
- Copy the URL for their RSS reader
- Use browser extensions to auto-detect

### Popular RSS Readers

- **Feedly** - https://feedly.com
- **Inoreader** - https://www.inoreader.com
- **NewsBlur** - https://newsblur.com
- **The Old Reader** - https://theoldreader.com
- **Feedbin** - https://feedbin.com

## Archives

### How It Works

The archives are automatically built from your articles:

1. **Grouping**: Articles grouped by month/year
2. **Counting**: Shows number of posts per month
3. **Sorting**: Newest months first
4. **Filtering**: Click to see posts from that month

### Archive Format

```
March 2026 (5)
February 2026 (8)
January 2026 (12)
December 2025 (6)
```

### Customization

Archives are generated in `scripts/main.js` in the `buildArchives()` function.

To customize the format, edit that function.

## Sidebar Sections

### 1. Subscribe (RSS)
- Prominent RSS button
- Orange color (standard RSS color)
- Opens feed in new tab

### 2. Archives
- Month/Year grouping
- Post counts
- Clickable to filter
- Newest first

### 3. Categories
- All your blog categories
- Click to filter posts
- Active state highlighting

## Responsive Behavior

### Desktop (> 968px)
- Sidebar on left (280px wide)
- Sticky positioning (follows scroll)
- Main content on right

### Tablet (768px - 968px)
- Sidebar moves below content
- Displays as horizontal grid
- 3 columns side-by-side

### Mobile (< 768px)
- Sidebar stacks vertically
- Full width sections
- Easy thumb navigation

## Customization

### Sidebar Width

Edit `styles/main.css`:

```css
.blog-layout {
    grid-template-columns: 280px 1fr; /* Change 280px */
}
```

### Sidebar Position

To move sidebar to the right:

```css
.blog-layout {
    grid-template-columns: 1fr 280px; /* Swap order */
}
```

### RSS Button Color

```css
.rss-button {
    background-color: #ff6719; /* Change color */
}
```

### Archive Date Format

Edit `scripts/main.js` in `buildArchives()`:

```javascript
const month = date.toLocaleDateString('en-US', { 
    month: 'short' // Change to 'short' for "Mar" instead of "March"
});
```

## Best Practices

### RSS Feed

1. **Update regularly**: Run `generate_rss.py` after adding articles
2. **Test the feed**: Use https://validator.w3.org/feed/
3. **Promote it**: Mention RSS in your About page
4. **Keep it fresh**: 20 items is a good limit

### Archives

1. **Consistent posting**: Try to post regularly
2. **Date accuracy**: Ensure article dates are correct
3. **Don't backdate**: Use actual publication dates

### Sidebar

1. **Keep it simple**: Don't overcrowd the sidebar
2. **Prioritize**: Most important items at top
3. **Test mobile**: Ensure it works on small screens

## Automation

### Auto-generate Feeds

Create a script to update everything:

**update-blog.sh**:
```bash
#!/bin/bash

# Generate RSS feed
python3 scripts/generate_rss.py

# Generate sitemap
python3 scripts/generate_sitemap.py

echo "✓ Feeds updated!"
```

Make it executable:
```bash
chmod +x update-blog.sh
```

Run after adding articles:
```bash
./update-blog.sh
```

### Cron Job

Automate if scraping from Substack:

```bash
# Edit crontab
crontab -e

# Add: Run daily at 2 AM
0 2 * * * cd /path/to/blog && python3 scripts/scraper.py && python3 scripts/generate_rss.py && python3 scripts/generate_sitemap.py
```

## Testing

### Test RSS Feed

1. **Validate**: https://validator.w3.org/feed/
2. **Preview**: Open `feed.xml` in browser
3. **Test reader**: Try subscribing in Feedly
4. **Check images**: Verify cover images load

### Test Archives

1. **Create test articles** with different dates
2. **Check grouping**: Verify months are correct
3. **Test filtering**: Click archive links
4. **Check counts**: Ensure numbers are accurate

### Test Responsive

1. **Desktop**: Full sidebar layout
2. **Tablet**: Horizontal sidebar
3. **Mobile**: Stacked sidebar
4. **Sticky**: Sidebar should stick on desktop

## Troubleshooting

### RSS feed not updating

1. Regenerate: `python3 scripts/generate_rss.py`
2. Clear browser cache
3. Check file permissions
4. Verify articles.json exists

### Archives not showing

1. Check articles have valid dates
2. Verify articles.json is loaded
3. Check browser console for errors
4. Ensure JavaScript is enabled

### Sidebar not sticky

1. Check CSS is loaded
2. Verify screen width > 968px
3. Check header height calculation
4. Test in different browsers

### Mobile layout broken

1. Clear cache
2. Check responsive CSS
3. Test in device mode
4. Verify viewport meta tag

## SEO Benefits

### RSS Feed

- **Syndication**: Content distributed wider
- **Backlinks**: RSS directories link to you
- **Engagement**: Readers stay updated
- **Authority**: Shows you're a serious blogger

### Archives

- **Internal linking**: More pages linked together
- **Crawlability**: Search engines find old posts
- **User experience**: Readers find content easily
- **Time on site**: Encourages exploration

## Analytics

Track RSS subscribers:
- Use FeedBurner (Google)
- Check server logs for feed.xml requests
- Use RSS-specific analytics services

Track archive usage:
- Google Analytics events
- Click tracking on archive links
- Monitor filtered views

## Next Steps

1. **Generate your RSS feed**: `python3 scripts/generate_rss.py`
2. **Test it**: Validate and preview
3. **Promote it**: Add to About page, social media
4. **Submit to directories**: Add to RSS directories
5. **Monitor**: Track subscribers and usage

## Resources

- **RSS Spec**: https://www.rssboard.org/rss-specification
- **Feed Validator**: https://validator.w3.org/feed/
- **RSS Directories**: Submit your feed to increase reach
- **RSS Best Practices**: https://www.rssboard.org/rss-profile

Your blog now has all the classic features readers expect! 📰
