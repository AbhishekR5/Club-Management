/** @odoo-module **/

export class Navigation {
    constructor() {
        this.isOpen = false;
        this.header = document.getElementById('sf-header');
        this.nav = document.getElementById('sf-nav');
        this.toggleBtn = document.getElementById('sf-nav-toggle');
        this.scrollThreshold = 50; // pixels to scroll before glassmorphism applies
        
        // Bind context for event listeners
        this.handleScroll = this.handleScroll.bind(this);
        this.toggleMenu = this.toggleMenu.bind(this);
        this.closeMenu = this.closeMenu.bind(this);
    }

    init() {
        if (!this.header || !this.nav || !this.toggleBtn) return;
        
        // Initial check in case page is loaded already scrolled
        this.handleScroll();
        
        // Bind Events
        window.addEventListener('scroll', this.handleScroll, { passive: true });
        this.toggleBtn.addEventListener('click', this.toggleMenu);
        
        // Close mobile menu when a link is clicked
        const links = this.nav.querySelectorAll('.sf-nav__link');
        links.forEach(link => {
            link.addEventListener('click', this.closeMenu);
        });
    }
    
    handleScroll() {
        if (window.scrollY > this.scrollThreshold) {
            this.header.classList.add('is-scrolled');
        } else {
            this.header.classList.remove('is-scrolled');
        }
    }
    
    toggleMenu() {
        this.isOpen = !this.isOpen;
        this.toggleBtn.setAttribute('aria-expanded', this.isOpen);
        
        if (this.isOpen) {
            this.nav.classList.add('is-open');
            this.toggleBtn.classList.add('is-active');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        } else {
            this.nav.classList.remove('is-open');
            this.toggleBtn.classList.remove('is-active');
            document.body.style.overflow = '';
        }
    }
    
    closeMenu() {
        if (this.isOpen) {
            this.toggleMenu();
        }
    }
}

