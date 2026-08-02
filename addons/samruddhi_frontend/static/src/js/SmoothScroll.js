/** @odoo-module **/

export class SmoothScroll {
    constructor() {
        this.lenis = null;
        this.isInitialized = false;
        this.animationId = null;
        
        // Bind methods to maintain 'this' context in RAF
        this.update = this.update.bind(this);
    }

    /**
     * Initializes Lenis smooth scrolling and hooks it into requestAnimationFrame.
     */
    initialize() {
        if (this.isInitialized) return;

        if (typeof window.Lenis === 'undefined') {
            console.warn("SmoothScroll: Lenis library is not loaded globally. Native scrolling fallback active.");
            return;
        }

        // Initialize Lenis with premium cinematic defaults
        this.lenis = new window.Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // Apple-like ease-out
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true,
            mouseMultiplier: 1,
            smoothTouch: false,
            touchMultiplier: 2,
            infinite: false,
        });

        // Setup ScrollTrigger synchronization hook
        if (window.ScrollTrigger) {
            this.lenis.on('scroll', window.ScrollTrigger.update);

            window.gsap.ticker.add((time) => {
                this.lenis.raf(time * 1000);
            });
            window.gsap.ticker.lagSmoothing(0);
        } else {
            // Fallback to standalone RAF loop if GSAP isn't tracking it
            this.animationId = requestAnimationFrame(this.update);
        }

        this.isInitialized = true;
    }

    /**
     * Main update loop for Lenis. 
     * Only runs if GSAP ticker is not handling the RAF.
     * @param {number} time - High res timestamp provided by RAF
     */
    update(time) {
        if (!this.isInitialized || !this.lenis) return;
        
        this.lenis.raf(time);
        
        this.animationId = requestAnimationFrame(this.update);
    }

    /**
     * Programmatically scroll to a target.
     * @param {HTMLElement|string|number} target 
     * @param {Object} options 
     */
    scrollTo(target, options = {}) {
        if (!this.isInitialized || !this.lenis) return;
        this.lenis.scrollTo(target, options);
    }

    /**
     * Stops the scrolling loop and destroys the Lenis instance to free memory.
     */
    destroy() {
        if (!this.isInitialized) return;

        if (this.animationId !== null) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        if (this.lenis) {
            if (window.ScrollTrigger) {
                this.lenis.off('scroll', window.ScrollTrigger.update);
            }
            this.lenis.destroy();
            this.lenis = null;
        }

        this.isInitialized = false;
    }
}
