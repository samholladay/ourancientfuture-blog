// JavaScript for article page

// Get article ID from URL
function getArticleId() {
    // First check for clean URL format: /articles/slug.html or articles/slug.html
    const path = window.location.pathname;
    
    // Match both /articles/slug.html and articles/slug.html (with or without leading slash)
    const match = path.match(/articles\/([^\/]+)\.html$/);
    if (match) {
        return match[1];
    }
    
    // Fallback to query parameter for backwards compatibility
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// Load and display article
async function loadArticle() {
    const articleId = getArticleId();
    
    if (!articleId) {
        showError('No article specified');
        return;
    }
    
    try {
        // Determine the correct path based on current location
        const path = window.location.pathname;
        let dataPath;
        
        // Check if we're in a language-specific directory (e.g., /es/articles/)
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        if (langMatch && path.includes('/articles/')) {
            // Language-specific article (two levels deep)
            dataPath = `../../${langMatch[1]}/data/articles/`;
        } else if (path.includes('/articles/')) {
            // English article (one level deep)
            dataPath = '../data/articles/';
        } else {
            // Root level
            dataPath = 'data/articles/';
        }
        
        const response = await fetch(`${dataPath}${articleId}.json`);
        if (!response.ok) {
            throw new Error('Article not found');
        }
        
        const article = await response.json();
        displayArticle(article);
        
        // Load related posts
        await loadRelatedPosts(article);
    } catch (error) {
        console.error('Error loading article:', error);
        showError('Article not found. Please return to the home page.');
    }
}

// Load related posts from the same category
async function loadRelatedPosts(currentArticle) {
    try {
        // Determine the correct path based on current location
        const path = window.location.pathname;
        let indexPath;
        
        // Check if we're in a language-specific directory
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        if (langMatch && path.includes('/articles/')) {
            // Language-specific (two levels deep)
            indexPath = `../../${langMatch[1]}/data/articles.json`;
        } else if (path.includes('/articles/')) {
            // English (one level deep)
            indexPath = '../data/articles.json';
        } else {
            // Root level
            indexPath = 'data/articles.json';
        }
        
        const response = await fetch(indexPath);
        if (!response.ok) return;
        
        const allArticles = await response.json();
        
        // Filter articles from same category, excluding current article
        const relatedArticles = allArticles
            .filter(article => 
                article.category === currentArticle.category && 
                article.id !== currentArticle.id
            )
            .slice(0, 3); // Get 3 most recent
        
        if (relatedArticles.length > 0) {
            displayRelatedPosts(relatedArticles);
        }
    } catch (error) {
        console.error('Error loading related posts:', error);
    }
}

// Display related posts
function displayRelatedPosts(articles) {
    const relatedDiv = document.getElementById('relatedPosts');
    if (!relatedDiv) return;
    
    relatedDiv.innerHTML = '<h3>Related Posts</h3>';
    
    const list = document.createElement('ul');
    list.className = 'related-posts-list';
    
    articles.forEach(article => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = `${article.id}.html`;
        link.textContent = article.title;
        li.appendChild(link);
        list.appendChild(li);
    });
    
    relatedDiv.appendChild(list);
}

// Update SEO meta tags
function updateSEO(article) {
    const baseUrl = window.location.origin;
    const articleUrl = `${baseUrl}/articles/${article.id}.html`;
    const description = article.meta_description || article.subtitle || article.excerpt || `Read ${article.title} on Our Ancient Future`;
    const imageUrl = article.cover_image ? `${baseUrl}/${article.cover_image}` : `${baseUrl}/media/og-image.jpg`;
    const keywords = article.tags ? article.tags.join(', ') : `${article.category}, blog, article`;
    
    // Update title
    const titleText = `${article.title} - My Blog`;
    document.title = titleText;
    document.getElementById('articleTitle').textContent = titleText;
    document.getElementById('metaTitle').setAttribute('content', titleText);
    
    // Update description
    document.getElementById('metaDescription').setAttribute('content', description);
    
    // Update keywords
    document.getElementById('metaKeywords').setAttribute('content', keywords);
    
    // Update canonical URL
    document.getElementById('canonicalUrl').setAttribute('href', articleUrl);
    
    // Update Open Graph tags
    document.getElementById('ogUrl').setAttribute('content', articleUrl);
    document.getElementById('ogTitle').setAttribute('content', titleText);
    document.getElementById('ogDescription').setAttribute('content', description);
    document.getElementById('ogImage').setAttribute('content', imageUrl);
    document.getElementById('articlePublished').setAttribute('content', article.date);
    
    // Update Twitter Card tags
    document.getElementById('twitterUrl').setAttribute('content', articleUrl);
    document.getElementById('twitterTitle').setAttribute('content', titleText);
    document.getElementById('twitterDescription').setAttribute('content', description);
    document.getElementById('twitterImage').setAttribute('content', imageUrl);
    
    // Add structured data for article
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article.title,
        "description": description,
        "image": imageUrl,
        "datePublished": article.date,
        "dateModified": article.date,
        "author": {
            "@type": "Person",
            "name": "My Blog Author"
        },
        "publisher": {
            "@type": "Organization",
            "name": "My Blog",
            "logo": {
                "@type": "ImageObject",
                "url": `${baseUrl}/media/logo.png`
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": articleUrl
        }
    };
    
    // Add or update structured data script
    let structuredDataScript = document.getElementById('structuredData');
    if (!structuredDataScript) {
        structuredDataScript = document.createElement('script');
        structuredDataScript.id = 'structuredData';
        structuredDataScript.type = 'application/ld+json';
        document.head.appendChild(structuredDataScript);
    }
    structuredDataScript.textContent = JSON.stringify(structuredData);
}

// Display article content
function displayArticle(article) {
    // Update SEO meta tags
    updateSEO(article);
    
    // Set article header
    document.getElementById('articleTitleMain').textContent = article.title;
    document.getElementById('articleSubtitle').textContent = article.subtitle || '';
    
    // Set metadata
    document.getElementById('articleCategory').textContent = article.category;
    
    // Format date
    const date = new Date(article.date);
    const formattedDate = date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    document.getElementById('articleDate').textContent = formattedDate;
    
    // Set cover image
    const coverDiv = document.getElementById('articleCover');
    if (article.cover_image) {
        const img = document.createElement('img');
        // Fix path based on directory depth
        const path = window.location.pathname;
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        
        let imagePath;
        if (langMatch && path.includes('/articles/')) {
            // Language-specific article (two levels deep: /es/articles/)
            imagePath = '../../' + article.cover_image;
        } else if (path.includes('/articles/')) {
            // English article (one level deep: /articles/)
            imagePath = '../' + article.cover_image;
        } else {
            // Root level
            imagePath = article.cover_image;
        }
        
        img.src = imagePath;
        img.alt = article.title;
        coverDiv.appendChild(img);
    } else {
        coverDiv.classList.add('empty');
    }
    
    // Set content
    const contentDiv = document.getElementById('articleContent');
    contentDiv.innerHTML = article.content;
    
    // Process content images to ensure they're properly styled
    const images = contentDiv.querySelectorAll('img');
    images.forEach(img => {
        // Wrap images in figure if not already
        if (img.parentElement.tagName !== 'FIGURE') {
            const figure = document.createElement('figure');
            img.parentNode.insertBefore(figure, img);
            figure.appendChild(img);
        }
    });
    
    // Set tags (if any)
    const tagsDiv = document.getElementById('articleTags');
    if (article.tags && article.tags.length > 0) {
        article.tags.forEach(tag => {
            const tagLink = document.createElement('a');
            tagLink.href = `index.html#${tag}`;
            tagLink.className = 'tag';
            tagLink.textContent = tag;
            tagsDiv.appendChild(tagLink);
        });
    }
}

// Show error message
function showError(message) {
    const contentDiv = document.getElementById('articleContent');
    contentDiv.innerHTML = `
        <div class="loading" style="color: #ff6719;">
            <p>${message}</p>
            <p style="margin-top: 1rem;">
                <a href="index.html" style="color: #ff6719;">← Return to home page</a>
            </p>
        </div>
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadArticle);
