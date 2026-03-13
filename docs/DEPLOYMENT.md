# Deployment Guide

This guide covers various options for deploying your static blog site.

## Prerequisites

Before deploying, make sure you have:
1. Run the scraper to generate article data
2. Added any custom gallery photos
3. Tested the site locally

## Option 1: GitHub Pages (Free)

### Steps:

1. **Create a GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to Pages section
   - Select source: Deploy from branch
   - Choose branch: `main` and folder: `/ (root)`
   - Save

3. **Configure custom domain**
   - Add a `CNAME` file with your domain:
     ```
     myblog.com
     ```
   - In your domain registrar, add DNS records:
     ```
     Type: A
     Name: @
     Value: 185.199.108.153
     Value: 185.199.109.153
     Value: 185.199.110.153
     Value: 185.199.111.153
     
     Type: CNAME
     Name: www
     Value: yourusername.github.io
     ```

4. **Enable HTTPS**
   - In GitHub Pages settings, check "Enforce HTTPS"

## Option 2: Netlify (Free)

### Steps:

1. **Sign up at netlify.com**

2. **Deploy via drag-and-drop**
   - Drag your blog folder to Netlify
   - Site will be live at `random-name.netlify.app`

3. **Or deploy via Git**
   - Connect your GitHub repository
   - Build settings: Leave empty (static site)
   - Deploy

4. **Configure custom domain**
   - Go to Domain settings
   - Add custom domain: `myblog.com`
   - Follow DNS configuration instructions
   - Netlify provides automatic HTTPS

### Netlify Configuration (Optional)

Create `netlify.toml`:

```toml
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Option 3: Vercel (Free)

### Steps:

1. **Sign up at vercel.com**

2. **Deploy via CLI**
   ```bash
   npm i -g vercel
   vercel
   ```

3. **Or deploy via Git**
   - Import your GitHub repository
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: `.`
   - Deploy

4. **Configure custom domain**
   - Go to project Settings > Domains
   - Add `myblog.com`
   - Configure DNS as instructed
   - Automatic HTTPS included

## Option 4: Traditional Web Hosting

For shared hosting or VPS:

### Steps:

1. **Upload files via FTP/SFTP**
   - Connect to your server
   - Upload all files to public_html or www directory

2. **Configure domain**
   - Point domain to your server's IP
   - Configure DNS A record:
     ```
     Type: A
     Name: @
     Value: your.server.ip.address
     ```

3. **Enable HTTPS**
   - Use Let's Encrypt (free)
   - Or use hosting provider's SSL certificate

### Apache Configuration

Create `.htaccess`:

```apache
# Enable HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Cache static assets
<FilesMatch "\.(jpg|jpeg|png|gif|css|js|woff|woff2)$">
  Header set Cache-Control "max-age=31536000, public"
</FilesMatch>
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name myblog.com www.myblog.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myblog.com www.myblog.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    root /var/www/blog;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(jpg|jpeg|png|gif|css|js|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Continuous Deployment

### Automated Updates

Create a script to update articles automatically:

**update.sh**:
```bash
#!/bin/bash

# Run scraper
python3 scripts/scraper.py

# Commit and push (for Git-based hosting)
git add data/ media/articles/
git commit -m "Update articles $(date +%Y-%m-%d)"
git push origin main
```

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line to run daily at 2 AM
0 2 * * * cd /path/to/blog && ./update.sh
```

### GitHub Actions

Create `.github/workflows/update.yml`:

```yaml
name: Update Articles

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run scraper
        run: python3 scripts/scraper.py
      
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/ media/articles/
          git commit -m "Update articles $(date +%Y-%m-%d)" || exit 0
          git push
```

## Performance Optimization

### Image Optimization

Before deploying, optimize images:

```bash
# Install imagemagick
sudo apt-get install imagemagick

# Optimize gallery images
for img in media/gallery/*.jpg; do
  convert "$img" -quality 85 -resize 1200x "$img"
done
```

### Minification

Minify CSS and JS for production:

```bash
# Install minifiers
npm install -g csso-cli terser

# Minify CSS
csso styles/main.css -o styles/main.min.css
csso styles/article.css -o styles/article.min.css

# Minify JS
terser scripts/main.js -o scripts/main.min.js
terser scripts/article.js -o scripts/article.min.js
```

Update HTML to use minified versions in production.

## Monitoring

### Analytics

Add Google Analytics or similar:

In `index.html` and `article.html`, add before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Troubleshooting

### Site not updating
- Clear browser cache
- Check deployment logs
- Verify files were uploaded

### Images not loading
- Check file paths are relative
- Verify images were uploaded
- Check file permissions (755 for directories, 644 for files)

### HTTPS issues
- Wait for SSL certificate propagation (can take 24 hours)
- Check DNS configuration
- Verify certificate is valid

## Security

### Best Practices

1. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use HTTPS only**
   - Redirect HTTP to HTTPS
   - Enable HSTS header

3. **Set security headers**
   ```
   X-Frame-Options: DENY
   X-Content-Type-Options: nosniff
   X-XSS-Protection: 1; mode=block
   ```

4. **Regular backups**
   - Backup your repository
   - Export article data regularly
