// Main JavaScript for landing page

let allArticles = [];
let currentFilter = 'all';

// Load configuration and initialize
async function init() {
    try {
        // Determine config path based on current location
        const path = window.location.pathname;
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        const configPath = langMatch ? '../config.json' : 'config.json';
        
        // Load config
        const config = await fetch(configPath).then(r => r.json());
        
        // Update page content from config
        updatePageContent(config);
        
        // Load gallery photos
        loadGallery(config.gallery_photos);
        
        // Load articles
        await loadArticles();
        
        // Set up event listeners
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing:', error);
    }
}

// Update page content from config
function updatePageContent(config) {
    // Update page title
    document.title = `${config.blog_title} - ${config.blog_description}`;
    
    // Update logo
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.textContent = config.blog_title;
    }
    
    // Update hero section
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle && config.hero_title) {
        heroTitle.textContent = config.hero_title;
    }
    
    const heroSubtitle = document.querySelector('.hero-subtitle');
    if (heroSubtitle && config.hero_subtitle) {
        heroSubtitle.textContent = config.hero_subtitle;
    }
    
    // Update footer
    const footer = document.querySelector('.footer p');
    if (footer && config.blog_title) {
        footer.innerHTML = `&copy; 2026 ${config.blog_title}. All rights reserved.`;
    }
}

// Load gallery photos
function loadGallery(photos) {
    const gallery = document.getElementById('photoGallery');
    
    if (!photos || photos.length === 0) {
        return; // Keep placeholder
    }
    
    gallery.innerHTML = '';
    
    // Check if we're in a language directory
    const path = window.location.pathname;
    const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
    
    photos.forEach(photo => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        
        const img = document.createElement('img');
        // Fix path for language directories
        img.src = langMatch ? '../' + photo.path : photo.path;
        img.alt = photo.caption || 'Gallery photo';
        img.loading = 'lazy';
        
        item.appendChild(img);
        gallery.appendChild(item);
    });
}

// Load articles from JSON
async function loadArticles() {
    try {
        // Determine the correct path based on current location
        const path = window.location.pathname;
        let dataPath;
        
        console.log('Current pathname:', path);
        
        // Check if we're in a language-specific directory
        // Match /es/, /es/index.html, or /es (with or without trailing slash)
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        console.log('Language match:', langMatch);
        
        if (langMatch) {
            // Language-specific index - use explicit relative path
            dataPath = `./data/articles.json`;
        } else {
            // English index
            dataPath = './data/articles.json';
        }
        
        console.log('Fetching from:', dataPath);
        console.log('Full URL:', window.location.origin + '/' + dataPath);
        
        const response = await fetch(dataPath);
        console.log('Response status:', response.status, response.ok);
        
        if (!response.ok) {
            throw new Error('Articles not found');
        }
        
        allArticles = await response.json();
        console.log('Loaded articles:', allArticles.length);
        
        // Articles are already sorted by date (newest first) from scraper
        displayArticles(allArticles);
        buildArchives(allArticles);
    } catch (error) {
        console.error('Error loading articles:', error);
        const grid = document.getElementById('articlesGrid');
        grid.innerHTML = `
            <div class="loading">
                <p>No articles found. Run the scraper script to fetch articles from your Substack.</p>
                <p style="margin-top: 1rem; font-size: 0.875rem;">
                    Run: <code style="background: #f5f5f5; padding: 0.25rem 0.5rem; border-radius: 3px;">python3 scripts/scraper.py</code>
                </p>
            </div>
        `;
    }
}

// Build archives sidebar grouped by month/year
function buildArchives(articles) {
    const archivesList = document.getElementById('archivesList');
    
    if (!articles || articles.length === 0) {
        archivesList.innerHTML = '<p class="loading-small">No archives yet</p>';
        return;
    }
    
    // Group articles by month/year
    const archives = {};
    
    articles.forEach(article => {
        const date = new Date(article.date);
        const year = date.getFullYear();
        const month = date.toLocaleDateString('en-US', { month: 'long' });
        const key = `${year}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        const label = `${month} ${year}`;
        
        if (!archives[key]) {
            archives[key] = {
                label: label,
                year: year,
                month: date.getMonth() + 1,
                count: 0,
                articles: []
            };
        }
        
        archives[key].count++;
        archives[key].articles.push(article);
    });
    
    // Sort by date (newest first)
    const sortedArchives = Object.entries(archives).sort((a, b) => b[0].localeCompare(a[0]));
    
    // Build HTML
    archivesList.innerHTML = '';
    
    sortedArchives.forEach(([key, archive]) => {
        const link = document.createElement('a');
        link.href = '#';
        link.className = 'archive-link';
        link.dataset.yearMonth = key;
        
        link.innerHTML = `
            <span class="archive-month">${archive.label}</span>
            <span class="archive-count">(${archive.count})</span>
        `;
        
        link.addEventListener('click', (e) => {
            e.preventDefault();
            filterByArchive(archive.articles, archive.label);
        });
        
        archivesList.appendChild(link);
    });
}

// Filter articles by archive
function filterByArchive(articles, label) {
    displayArticles(articles);
    
    // Update category links
    document.querySelectorAll('.category-link').forEach(link => {
        link.classList.remove('active');
    });
}

// Display articles in grid
function displayArticles(articles) {
    const grid = document.getElementById('articlesGrid');
    
    if (articles.length === 0) {
        grid.innerHTML = '<div class="loading">No articles found for this category.</div>';
        return;
    }
    
    grid.innerHTML = '';
    
    articles.forEach(article => {
        const card = createArticleCard(article);
        grid.appendChild(card);
    });
}

// Create article card element
function createArticleCard(article) {
    const card = document.createElement('a');
    
    // Determine correct article path based on current location
    const path = window.location.pathname;
    const langMatch = path.match(/^\/(es|ru|de|fr|cn)\//);
    
    if (langMatch) {
        // We're in a language directory, link to language-specific articles
        card.href = `articles/${article.id}.html`;
    } else {
        // We're in the root, link to English articles
        card.href = `articles/${article.id}.html`;
    }
    
    card.className = 'article-card';
    
    // Format date
    const date = new Date(article.date);
    const formattedDate = date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    
    // Build the card HTML
    let cardHTML = '';
    
    // Add cover image if available
    if (article.cover_image) {
        // Fix image path for language directories
        const imagePath = langMatch ? '../' + article.cover_image : article.cover_image;
        cardHTML += `
            <div class="article-cover-image">
                <img src="${imagePath}" alt="${article.title}" loading="lazy">
            </div>
        `;
    }
    
    cardHTML += `
        <div class="article-meta">
            <span class="article-category">${article.category}</span>
            <span class="article-date">${formattedDate}</span>
        </div>
        <h3 class="article-card-title">${article.title}</h3>
        ${article.subtitle ? `<p class="article-subtitle">${article.subtitle}</p>` : ''}
    `;
    
    // Add preview if available, otherwise use excerpt
    if (article.preview && article.preview.trim()) {
        cardHTML += `<div class="article-preview">${article.preview}</div>`;
    } else if (article.excerpt) {
        cardHTML += `<p class="article-excerpt">${article.excerpt}</p>`;
    }
    
    cardHTML += `<span class="article-read-more">Read more →</span>`;
    
    card.innerHTML = cardHTML;
    
    return card;
}

// Set up event listeners
function setupEventListeners() {
    // Top navigation category filters
    const navLinks = document.querySelectorAll('.nav-link[data-category]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state (only for category links)
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Filter articles
            const category = link.dataset.category;
            filterArticles(category);
        });
    });
    
    // Sidebar category links
    const categoryLinks = document.querySelectorAll('.category-link');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state
            categoryLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Filter articles
            const category = link.dataset.category;
            filterArticles(category);
        });
    });
}

// Filter articles by category
function filterArticles(category) {
    currentFilter = category;
    
    let filtered;
    if (category === 'all') {
        filtered = allArticles;
    } else {
        filtered = allArticles.filter(article => 
            article.category.toLowerCase() === category.toLowerCase()
        );
    }
    
    displayArticles(filtered);
}

// Language selector functionality
function setupLanguageSelector() {
    const langButton = document.getElementById('langButton');
    const langDropdown = document.getElementById('langDropdown');
    
    if (langButton && langDropdown) {
        langButton.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            langDropdown.classList.remove('show');
        });
        
        // Update button text based on current language
        const path = window.location.pathname;
        const langMatch = path.match(/^\/(es|ru|de|fr|cn)(\/|$)/);
        if (langMatch) {
            const langCodes = {
                'es': '🌐 ES',
                'ru': '🌐 RU',
                'de': '🌐 DE',
                'fr': '🌐 FR',
                'cn': '🌐 CN'
            };
            langButton.textContent = langCodes[langMatch[1]] || '🌐 EN';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    init();
    setupLanguageSelector();
});
