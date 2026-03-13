# About Page Configuration

The About page (`about.html`) displays information about you and your blog. All content is dynamically loaded from `config.json`.

## Configuration

Edit the `author` section in `config.json`:

```json
{
  "author": {
    "name": "Your Name",
    "tagline": "Writer, Thinker, Creator",
    "photo": "media/author.jpg",
    "bio": [
      "First paragraph of your bio",
      "Second paragraph of your bio",
      "Add as many paragraphs as you want"
    ],
    "about_blog": [
      "What your blog is about",
      "Why you started it",
      "What readers can expect"
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

## Author Photo

1. **Add your photo** to `media/author.jpg`
2. **Recommended specs:**
   - Format: JPG or PNG
   - Size: Square (1:1 aspect ratio)
   - Resolution: At least 500x500px
   - File size: Under 500KB (optimize for web)

3. **Custom path:** If you want a different filename, update the `photo` field in config.json

## Bio Section

The `bio` array supports multiple paragraphs:
- Each array item becomes a separate paragraph
- Write in first person
- Share your background, interests, and expertise
- Keep it authentic and engaging

**Example:**
```json
"bio": [
  "I'm a software engineer and writer based in San Francisco.",
  "I've been writing about technology for over 10 years, with a focus on AI, web development, and digital culture.",
  "When I'm not coding or writing, you can find me reading classic literature or watching art house films."
]
```

## About Blog Section

The `about_blog` array describes your blog:
- What topics you cover
- Why you started the blog
- What makes it unique
- What readers can expect

**Example:**
```json
"about_blog": [
  "This blog features in-depth articles on technology, literature, and film.",
  "I started it in 2020 as a way to explore the intersections between these fields and share my thoughts with a wider audience.",
  "Each piece is carefully researched and written to provide unique perspectives and thoughtful analysis."
]
```

## Social Links

Supported platforms:
- **Twitter** - Your Twitter/X profile
- **GitHub** - Your GitHub profile
- **LinkedIn** - Your LinkedIn profile
- **Email** - Your email (use `mailto:` format)

**To hide a platform:** Simply remove it from the config or set it to an empty string.

**Example:**
```json
"social": {
  "twitter": "https://twitter.com/johndoe",
  "github": "https://github.com/johndoe",
  "email": "mailto:john@example.com"
}
```

## Customization

### Topics Section

The topics section is currently hardcoded in `about.html`. To customize:

1. Open `about.html`
2. Find the `topics-section`
3. Edit the topic cards:

```html
<div class="topic-card">
    <h3>Your Topic</h3>
    <p>Description of what you write about.</p>
</div>
```

### Styling

Edit `styles/about.css` to customize:
- Author photo size and shape
- Bio text styling
- Social link appearance
- Topic card layout
- Colors and spacing

**Example customizations:**

**Circular author photo:**
```css
.author-photo {
    border-radius: 50%; /* Makes it circular */
}
```

**Different layout:**
```css
.author-section {
    grid-template-columns: 300px 1fr; /* Wider photo */
}
```

## Dynamic Content

The About page uses `scripts/about.js` to load content from `config.json`. This means:

✅ **No HTML editing needed** - Just update config.json
✅ **Consistent branding** - Same data used across the site
✅ **Easy updates** - Change once, updates everywhere

## SEO

The About page includes:
- Proper meta tags
- Open Graph tags for social sharing
- Structured data (AboutPage schema)
- Canonical URL

To optimize:
1. Update the meta description in `about.html` to describe you
2. Add an og:image if you want a custom social sharing image
3. Consider adding more structured data about yourself

## Best Practices

### Writing Your Bio

1. **Be authentic** - Write in your own voice
2. **Be specific** - Mention concrete achievements or interests
3. **Be concise** - 2-4 paragraphs is ideal
4. **Include credentials** - Relevant experience or expertise
5. **Show personality** - Let your unique voice shine through

### Photo Tips

1. **Professional but approachable** - Smile, make eye contact
2. **Good lighting** - Natural light works best
3. **Simple background** - Don't distract from your face
4. **Recent photo** - Use a current image
5. **High quality** - Sharp, well-composed

### Social Links

1. **Keep it relevant** - Only include platforms you actively use
2. **Keep them updated** - Make sure links work
3. **Professional presence** - Ensure your profiles are current
4. **Consistency** - Use the same name/handle across platforms

## Testing

After updating your About page:

1. **Check locally:**
   ```bash
   python3 -m http.server 8000
   # Visit http://localhost:8000/about.html
   ```

2. **Verify:**
   - [ ] Author photo loads correctly
   - [ ] Bio displays properly
   - [ ] Social links work
   - [ ] Page is responsive on mobile
   - [ ] No console errors

3. **Test social sharing:**
   - Use Facebook Debugger
   - Use Twitter Card Validator
   - Check how it looks when shared

## Troubleshooting

### Photo not showing
- Check the file path in config.json
- Ensure the image file exists
- Check file permissions
- Try a different image format

### Bio not displaying
- Check JSON syntax in config.json
- Ensure bio is an array of strings
- Check browser console for errors

### Social links not working
- Verify URLs are complete (include https://)
- Check for typos in platform names
- Ensure config.json is valid JSON

### Styling issues
- Clear browser cache
- Check for CSS conflicts
- Verify about.css is loaded
- Check responsive breakpoints

## Examples

### Minimal Configuration
```json
"author": {
  "name": "Jane Doe",
  "photo": "media/author.jpg",
  "bio": ["I write about tech and culture."]
}
```

### Full Configuration
```json
"author": {
  "name": "John Smith",
  "tagline": "Software Engineer & Writer",
  "photo": "media/author.jpg",
  "bio": [
    "I'm a full-stack developer with 10 years of experience building web applications.",
    "I started this blog to share my knowledge and connect with other developers.",
    "When I'm not coding, I enjoy reading science fiction and hiking."
  ],
  "about_blog": [
    "This blog covers modern web development, with a focus on JavaScript, React, and Node.js.",
    "I also write about software architecture, best practices, and the occasional book review."
  ],
  "social": {
    "twitter": "https://twitter.com/johnsmith",
    "github": "https://github.com/johnsmith",
    "linkedin": "https://linkedin.com/in/johnsmith",
    "email": "mailto:john@example.com"
  }
}
```

## Next Steps

- Customize the topics section in `about.html`
- Add more social platforms if needed
- Consider adding a newsletter signup
- Link to your best articles
- Add testimonials or press mentions
