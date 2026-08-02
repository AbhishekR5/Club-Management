/** @odoo-module **/

export class AnimationEngine {
    constructor() {
        this.gsap = null;
        this.scrollTrigger = null;
        this.isInitialized = false;
        
        // Central registry for all active timelines
        this.timelines = new Map();
    }

    /**
     * Initializes the GSAP engine and registers ScrollTrigger.
     */
    initialize() {
        if (this.isInitialized) return;

        // Ensure global GSAP is loaded
        if (window.gsap) {
            this.gsap = window.gsap;
            
            // Register ScrollTrigger if available
            if (window.ScrollTrigger) {
                this.scrollTrigger = window.ScrollTrigger;
                this.gsap.registerPlugin(this.scrollTrigger);
            } else {
                console.warn("AnimationEngine: ScrollTrigger not found on window.");
            }
        } else {
            console.warn("AnimationEngine: GSAP not found on window. Animations disabled.");
            return;
        }

        this.isInitialized = true;
    }

    /**
     * Registers and stores a GSAP timeline for later playback.
     * @param {string} id - Unique identifier for the timeline.
     * @param {Object} config - GSAP timeline configuration options (e.g., { paused: true, scrollTrigger: {...} })
     * @returns {gsap.core.Timeline|null} The created timeline, or null if GSAP is unavailable.
     */
    registerTimeline(id, config = {}) {
        if (!this.isInitialized || !this.gsap) return null;

        // If a timeline with this ID already exists, kill it first to avoid duplicates
        if (this.timelines.has(id)) {
            this.kill(id);
        }

        const tl = this.gsap.timeline(config);
        this.timelines.set(id, tl);

        return tl;
    }

    /**
     * Plays a registered timeline.
     * @param {string} id - Unique identifier for the timeline.
     */
    play(id) {
        if (!this.isInitialized) return;
        const tl = this.timelines.get(id);
        if (tl) tl.play();
    }

    /**
     * Pauses a registered timeline.
     * @param {string} id - Unique identifier for the timeline.
     */
    pause(id) {
        if (!this.isInitialized) return;
        const tl = this.timelines.get(id);
        if (tl) tl.pause();
    }

    /**
     * Reverts and kills a specific timeline, freeing memory.
     * @param {string} id - Unique identifier for the timeline.
     */
    kill(id) {
        if (!this.isInitialized) return;
        
        const tl = this.timelines.get(id);
        if (tl) {
            tl.kill(); // Kill the timeline and its tweens
            if (tl.scrollTrigger) {
                tl.scrollTrigger.kill(); // Kill associated ScrollTrigger if any
            }
            this.timelines.delete(id);
        }
    }

    /**
     * Completely destroys the AnimationEngine.
     * Kills all registered timelines and ScrollTriggers to prevent memory leaks during route changes.
     */
    destroy() {
        if (!this.isInitialized) return;

        // Kill all tracked timelines
        this.timelines.forEach((tl) => {
            tl.kill();
            if (tl.scrollTrigger) tl.scrollTrigger.kill();
        });
        this.timelines.clear();

        // Kill any globally attached ScrollTriggers
        if (this.scrollTrigger) {
            this.scrollTrigger.killAll();
        }

        // Kill any rogue tweens
        if (this.gsap) {
            this.gsap.globalTimeline.clear();
        }

        this.isInitialized = false;
    }
}
