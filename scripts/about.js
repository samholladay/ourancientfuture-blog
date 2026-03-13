// JavaScript for About page - loads content from config.json

async function loadAboutPage() {
    try {
        const response = await fetch('config.json');
        const config = await response.json();
        
        // Update page title and logo
        document.title = `About - ${config.blog_title}`;
        document.getElementById('siteLogo').textContent = config.blog_title;
        document.getElementById('footerName').textContent = config.blog_title;
        
        // Update author information
        const author = config.author;
        
        if (author) {
            // Author name and tagline
            document.getElementById('authorName').textContent = author.name || 'Author Name';
            document.getElementById('authorTagline').textContent = author.tagline || '';
            
            // Author photo
            if (author.photo) {
                const photoImg = document.getElementById('authorPhoto');
                photoImg.src = author.photo;
                photoImg.alt = `Photo of ${author.name}`;
            }
            
            // Author bio
            if (author.bio && author.bio.length > 0) {
                const bioDiv = document.getElementById('authorBio');
                bioDiv.innerHTML = '';
                author.bio.forEach(paragraph => {
                    const p = document.createElement('p');
                    p.textContent = paragraph;
                    bioDiv.appendChild(p);
                });
            }
            
            // About blog content
            if (author.about_blog && author.about_blog.length > 0) {
                const aboutBlogDiv = document.getElementById('aboutBlogContent');
                aboutBlogDiv.innerHTML = '';
                author.about_blog.forEach(paragraph => {
                    const p = document.createElement('p');
                    p.textContent = paragraph;
                    aboutBlogDiv.appendChild(p);
                });
            }
            
            // Social links
            if (author.social) {
                const socialLinksDiv = document.getElementById('socialLinks');
                socialLinksDiv.innerHTML = '';
                
                const socialIcons = {
                    twitter: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/></svg>',
                    github: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z"/></svg>',
                    linkedin: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
                    email: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'
                };
                
                const socialLabels = {
                    twitter: 'Twitter',
                    github: 'GitHub',
                    linkedin: 'LinkedIn',
                    email: 'Email'
                };
                
                Object.keys(author.social).forEach(platform => {
                    if (author.social[platform]) {
                        const link = document.createElement('a');
                        link.href = author.social[platform];
                        link.className = 'social-link';
                        link.target = platform !== 'email' ? '_blank' : '';
                        link.rel = platform !== 'email' ? 'noopener noreferrer' : '';
                        link.innerHTML = `${socialIcons[platform] || ''} ${socialLabels[platform] || platform}`;
                        socialLinksDiv.appendChild(link);
                    }
                });
            }
        }
        
    } catch (error) {
        console.error('Error loading about page:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadAboutPage);
