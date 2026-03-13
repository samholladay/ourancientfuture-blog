# SEO & Performance Guide

This guide covers all SEO optimizations, AI bot support, and performance enhancements implemented in your blog.

## Table of Contents

1. [SEO Features](#seo-features)
2. [AI Bot Optimization](#ai-bot-optimization)
3. [Performance Optimizations](#performance-optimizations)
4. [Setup Instructions](#setup-instructions)
5. [Monitoring & Testing](#monitoring--testing)

## SEO Features

### Meta Tags

Every page includes comprehensive meta tags:

#### Homepage (`index.html`)
- **Title tag**: Optimized for search engines
- **Meta description**: Compelling description for search results
- **Keywords**: Relevant keywords for your content
- **Canonical URL**: Prevents duplicate content issues
- **Open Graph tags**: Optimized for Facebook/LinkedIn sharing
- **Twitter Cards**: Optimized for Twitter sharing
- **Structured Data**: JSON-LD schema for rich snippets

#### Article Pages (`article.html`)
- **Dynamic meta tags**: Updated per article via JavaScript
- **Article-specific Open Graph**: Includes cover image, publish date
- **Structured Data**: BlogPosting schema for rich snippets
- **Canonical URLs**: Unique URL for each article

### Structured Data (Schema.org)

Implemented schemas:
- **Blog schema** (homepage): Tells search engines this is a blog
- **BlogPosting schema** (articles): Rich snippets with author, date, image
- **Organization schema**: Publisher information
- **Person schema**: Author information

### Sitemap

Generate `sitemap.xml` automatically:

```bash
python3 scripts/generate_sitemap.py
```

The sitemap includes:
- Homepage with priority 1.0
- All articles with priority 0.8
- Last modified dates
- Image information
- Change frequency hints

Submit to search engines:
- Google Search Console: https://search.google.com/search-console
- Bing Webmaster Tools: https://www.bing.com/webmasters

### Robots.txt

Located at `/robots.txt`, it:
- Allows all search engines to crawl
- Allows all AI bots to crawl
- Specifies sitemap location
- Sets crawl delays for politeness
- Explicitly allows major AI bots (GPTBot, Claude, etc.)

### Canonical URLs

Every page has a canonical URL to prevent duplicate content penalties.

## AI Bot Optimization

### Supported AI Bots

Your site explicitly allows these AI bots in `robots.txt`:
- **GPTBot** (OpenAI)
- **ChatGPT-User** (OpenAI)
- **CCBot** (Common Crawl)
- **anthropic-ai** (Anthropic)
- **Claude-Web** (Anthropic)
- **ClaudeBot** (Anthropic)
- **Google-Extended** (Google AI)
- **PerplexityBot** (Perplexity)
- **Applebot-Extended** (Apple)
- **Bytespider** (ByteDance)
- **FacebookBot** (Meta)
- **YouBot** (You.com)

### AI.txt File

Located at `/.well-known/ai.txt`, it specifies:
- Crawling permissions
- Content licensing for AI training
- Preferred formats
- Attribution preferences
- Contact information

This helps AI companies understand how to use your content ethically.

### Benefits

1. **AI Search**: Your content appears in AI-powered search (Perplexity, ChatGPT, etc.)
2. **Training Data**: Your content can be used to train AI models
3. **Attribution**: AI systems can properly cite your work
4. **Discoverability**: Better visibility in AI-powered tools

## Performance Optimizations

### Lighthouse Score Improvements

#### Performance
- **Preconnect**: Font resources preconnected
- **Lazy Loading**: Images load only when needed
- **Caching**: Aggressive caching via `.htaccess`
- **Compression**: Gzip/Deflate enabled
- **Minification**: CSS/JS can be minified for production

#### Accessibility
- **Semantic HTML**: Proper heading hierarchy
- **Alt text**: All images should have alt attributes
- **ARIA labels**: Where appropriate
- **Color contrast**: Meets WCAG standards

#### Best Practices
- **HTTPS**: Enforced via `.htaccess`
- **Security headers**: X-Frame-Options, CSP, etc.
- **Error pages**: Custom 404 page
- **Manifest**: PWA manifest for mobile

#### SEO
- **Meta tags**: Comprehensive on every page
- **Structured data**: Schema.org markup
- **Sitemap**: XML sitemap
- **Robots.txt**: Proper crawl directives
- **Canonical URLs**: Prevent duplicate content

### Caching Strategy

Via `.htaccess`:
- **Images**: 1 year cache
- **CSS/JS**: 1 month cache
- **Fonts**: 1 year cache
- **HTML**: 1 hour cache
- **JSON**: 1 day cache

### Security Headers

Implemented headers:
- `X-Frame-Options: SAMEORIGIN` - Prevent clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `X-Content-Type-Options: nosniff` - Prevent MIME sniffing
- `Referrer-Policy` - Control referrer information
- `Content-Security-Policy` - Restrict resource loading
- `Permissions-Policy` - Control browser features

### Progressive Web App (PWA)

Basic PWA support via `site.webmanifest`:
- App name and description
- Theme colors
- Icons (add your own)
- Standalone display mode

## Setup Instructions

### 1. Update Configuration

Edit `config.json`:

```json
{
  "site_url": "https://yourdomain.com",
  "blog_title": "Your Blog Name",
  "blog_description": "Your description"
}
```

### 2. Update HTML Files

Replace `myblog.com` with your actual domain in:
- `index.html` (meta tags)
- `article.html` (meta tags)

### 3. Generate Sitemap

After adding articles:

```bash
python3 scripts/generate_sitemap.py
```

Re-run this whenever you add new articles.

### 4. Add Favicon and Images

Create these files:
- `/favicon-32x32.png` (32x32px)
- `/favicon-16x16.png` (16x16px)
- `/apple-touch-icon.png` (180x180px)
- `/android-chrome-192x192.png` (192x192px)
- `/android-chrome-512x512.png` (512x512px)
- `/media/og-image.jpg` (1200x630px for social sharing)
- `/media/logo.png` (for structured data)

### 5. Submit to Search Engines

#### Google Search Console
1. Go to https://search.google.com/search-console
2. Add your property
3. Verify ownership
4. Submit sitemap: `https://yourdomain.com/sitemap.xml`

#### Bing Webmaster Tools
1. Go to https://www.bing.com/webmasters
2. Add your site
3. Verify ownership
4. Submit sitemap

### 6. Configure Server

If using Apache, the `.htaccess` file is ready.

If using Nginx, create a similar config (see `docs/DEPLOYMENT.md`).

## Monitoring & Testing

### Test SEO

**Google Rich Results Test**
- URL: https://search.google.com/test/rich-results
- Test your homepage and article pages
- Verify structured data is valid

**Schema Markup Validator**
- URL: https://validator.schema.org/
- Paste your page URL
- Check for errors

**Open Graph Debugger**
- Facebook: https://developers.facebook.com/tools/debug/
- LinkedIn: https://www.linkedin.com/post-inspector/
- Twitter: https://cards-dev.twitter.com/validator

### Test Performance

**Google Lighthouse**
```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Run test
lighthouse https://yourdomain.com --view
```

Or use Chrome DevTools:
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Click "Generate report"

**PageSpeed Insights**
- URL: https://pagespeed.web.dev/
- Test both mobile and desktop
- Aim for 90+ scores

**GTmetrix**
- URL: https://gtmetrix.com/
- Comprehensive performance analysis

### Monitor Rankings

**Google Search Console**
- Track impressions, clicks, CTR
- Monitor search queries
- Check for indexing issues

**Google Analytics**
- Track visitor behavior
- Monitor traffic sources
- Analyze popular content

### Check Crawling

**Robots.txt Tester**
- Google Search Console > Crawl > robots.txt Tester
- Verify bots can access your content

**Sitemap Status**
- Google Search Console > Sitemaps
- Check for errors
- Monitor indexed pages

## Best Practices

### Content SEO

1. **Title Tags**
   - Keep under 60 characters
   - Include primary keyword
   - Make it compelling

2. **Meta Descriptions**
   - Keep under 160 characters
   - Include call-to-action
   - Summarize content

3. **Headings**
   - Use H1 for page title (one per page)
   - Use H2-H6 for structure
   - Include keywords naturally

4. **Images**
   - Always add alt text
   - Use descriptive filenames
   - Optimize file size
   - Use modern formats (WebP)

5. **Internal Linking**
   - Link between related articles
   - Use descriptive anchor text
   - Create topic clusters

### Technical SEO

1. **URL Structure**
   - Keep URLs short and descriptive
   - Use hyphens, not underscores
   - Avoid special characters

2. **Mobile-First**
   - Site is already responsive
   - Test on real devices
   - Check mobile usability in Search Console

3. **Page Speed**
   - Optimize images
   - Minimize CSS/JS
   - Use CDN if needed
   - Enable compression

4. **HTTPS**
   - Always use HTTPS
   - Redirect HTTP to HTTPS
   - Update all internal links

### Regular Maintenance

**Weekly**
- Check Google Search Console for errors
- Review new search queries
- Monitor site speed

**Monthly**
- Generate new sitemap
- Check for broken links
- Review analytics
- Update content

**Quarterly**
- Run full Lighthouse audit
- Review and update meta descriptions
- Check competitor rankings
- Update structured data if needed

## Troubleshooting

### Pages Not Indexed

1. Check robots.txt isn't blocking
2. Verify sitemap is submitted
3. Check for noindex tags
4. Request indexing in Search Console

### Low Lighthouse Scores

1. Optimize images (compress, resize)
2. Minify CSS/JS
3. Enable caching
4. Remove unused code
5. Use CDN for assets

### Structured Data Errors

1. Validate with Schema.org validator
2. Check JSON-LD syntax
3. Ensure all required fields present
4. Test with Rich Results Test

### Social Sharing Issues

1. Verify Open Graph tags
2. Check image dimensions (1200x630)
3. Clear social media caches
4. Test with debuggers

## Resources

- [Google Search Central](https://developers.google.com/search)
- [Schema.org Documentation](https://schema.org/)
- [Web.dev Performance](https://web.dev/performance/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
