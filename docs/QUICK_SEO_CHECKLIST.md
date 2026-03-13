# Quick SEO Setup Checklist

Use this checklist to ensure your blog is fully optimized.

## Initial Setup

### 1. Configuration
- [ ] Update `site_url` in `config.json` to your actual domain
- [ ] Update `blog_title` and `blog_description` in `config.json`
- [ ] Replace all instances of `myblog.com` in HTML files with your domain

### 2. Create Required Images
- [ ] `/favicon-32x32.png` (32x32px)
- [ ] `/favicon-16x16.png` (16x16px)
- [ ] `/apple-touch-icon.png` (180x180px)
- [ ] `/android-chrome-192x192.png` (192x192px)
- [ ] `/android-chrome-512x512.png` (512x512px)
- [ ] `/media/og-image.jpg` (1200x630px - for social sharing)
- [ ] `/media/logo.png` (square, at least 512x512px)

### 3. Generate Sitemap
```bash
python3 scripts/generate_sitemap.py
```
- [ ] Sitemap generated at `/sitemap.xml`
- [ ] Re-run after adding new articles

### 4. Verify Files Exist
- [ ] `/robots.txt` - Tells bots how to crawl
- [ ] `/sitemap.xml` - Lists all pages
- [ ] `/.well-known/ai.txt` - AI bot instructions
- [ ] `/.well-known/security.txt` - Security contact
- [ ] `/site.webmanifest` - PWA manifest
- [ ] `/.htaccess` - Server configuration (Apache)
- [ ] `/404.html` - Custom error page

## Search Engine Submission

### Google
- [ ] Create Google Search Console account
- [ ] Add and verify your property
- [ ] Submit sitemap: `https://yourdomain.com/sitemap.xml`
- [ ] Request indexing for homepage

### Bing
- [ ] Create Bing Webmaster Tools account
- [ ] Add and verify your site
- [ ] Submit sitemap

## Testing

### SEO Tests
- [ ] Test with Google Rich Results: https://search.google.com/test/rich-results
- [ ] Validate structured data: https://validator.schema.org/
- [ ] Test Open Graph: https://developers.facebook.com/tools/debug/
- [ ] Test Twitter Cards: https://cards-dev.twitter.com/validator

### Performance Tests
- [ ] Run Google Lighthouse (aim for 90+ in all categories)
- [ ] Test with PageSpeed Insights: https://pagespeed.web.dev/
- [ ] Check mobile-friendliness: https://search.google.com/test/mobile-friendly

### Functionality Tests
- [ ] All meta tags populate correctly on article pages
- [ ] Images have alt text
- [ ] Internal links work
- [ ] 404 page displays correctly
- [ ] HTTPS redirect works (if applicable)

## Content Optimization

### Every Article Should Have
- [ ] Compelling title (under 60 characters)
- [ ] Meta description (under 160 characters)
- [ ] Cover image (optimized, with alt text)
- [ ] Proper category
- [ ] Relevant tags
- [ ] Internal links to related articles

### Homepage
- [ ] Clear value proposition
- [ ] Updated gallery photos
- [ ] Recent articles displayed
- [ ] All navigation links work

## Ongoing Maintenance

### Weekly
- [ ] Check Search Console for errors
- [ ] Review new search queries
- [ ] Monitor site speed

### After Adding Articles
- [ ] Regenerate sitemap: `python3 scripts/generate_sitemap.py`
- [ ] Check article meta tags
- [ ] Verify images load correctly
- [ ] Test social sharing

### Monthly
- [ ] Review analytics
- [ ] Check for broken links
- [ ] Update old content if needed
- [ ] Run Lighthouse audit

## AI Bot Optimization

### Verified in robots.txt
- [ ] GPTBot (OpenAI)
- [ ] Claude (Anthropic)
- [ ] Google-Extended
- [ ] PerplexityBot
- [ ] Other major AI bots

### AI.txt Configuration
- [ ] Contact information updated
- [ ] License information correct
- [ ] Attribution preferences set

## Performance Checklist

### Images
- [ ] All images compressed
- [ ] Appropriate sizes (not oversized)
- [ ] Lazy loading enabled (already in code)
- [ ] Alt text on all images

### Caching
- [ ] `.htaccess` configured (Apache)
- [ ] Or nginx config set up
- [ ] Browser caching enabled
- [ ] Compression enabled

### Security
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] CSP policy set
- [ ] No mixed content warnings

## Common Issues

### "Pages not indexed"
1. Check robots.txt isn't blocking
2. Submit sitemap in Search Console
3. Request indexing manually
4. Wait 1-2 weeks

### "Low Lighthouse score"
1. Compress images
2. Minify CSS/JS (for production)
3. Enable caching
4. Check for render-blocking resources

### "Social sharing not working"
1. Verify og:image is 1200x630px
2. Check image is publicly accessible
3. Clear Facebook/Twitter cache
4. Verify meta tags with debuggers

## Quick Commands

```bash
# Generate sitemap
python3 scripts/generate_sitemap.py

# Create new article
python3 scripts/create_article.py create drafts/my-article.md

# Scrape from Substack
python3 scripts/scraper.py

# Test locally
python3 -m http.server 8000

# Run Lighthouse (if installed)
lighthouse https://yourdomain.com --view
```

## Resources

- **SEO Guide**: `docs/SEO_GUIDE.md` (comprehensive)
- **Deployment**: `docs/DEPLOYMENT.md`
- **Manual Articles**: `docs/MANUAL_ARTICLES.md`
- **Customization**: `docs/CUSTOMIZATION.md`

## Success Metrics

After 1 month, you should see:
- [ ] Pages indexed in Google
- [ ] Lighthouse scores 90+
- [ ] Rich snippets in search results
- [ ] Social sharing working
- [ ] AI bots crawling (check logs)

After 3 months:
- [ ] Organic search traffic
- [ ] Improved rankings
- [ ] Content appearing in AI search
- [ ] Social media engagement

---

**Need help?** Check the full guides in the `docs/` folder!
