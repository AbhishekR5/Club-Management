/** @odoo-module **/

export class RendererManager {
    constructor() {
        this.renderer = null;
        this.container = null;
        this.isInitialized = false;
    }

    /**
     * Initializes the THREE.WebGLRenderer with premium cinematic settings.
     */
    initialize() {
        if (this.isInitialized || !window.THREE) return;

        this.container = document.getElementById('hero-canvas-container');
        if (!this.container) {
            console.error("RendererManager: Container #hero-canvas-container not found.");
            return;
        }

        // Initialize Renderer with premium settings
        this.renderer = new window.THREE.WebGLRenderer({
            alpha: true,           // Support transparent background
            antialias: true,       // Smooth jagged edges
            powerPreference: "high-performance",
            stencil: false,        // Optimization: Disable if stencil buffer not used
            depth: true            // Optimization: Depth buffer is required
        });

        // Setup size and append to DOM
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.container.appendChild(this.renderer.domElement);

        // Responsive Pixel Ratio (Optimize for High DPI Retina displays, cap at 2 for performance)
        this.updatePixelRatio();

        // Modern Color Space and Cinematic Tone Mapping
        this.renderer.outputColorSpace = window.THREE.SRGBColorSpace;
        this.renderer.toneMapping = window.THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;

        // Shadow Support
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = window.THREE.PCFSoftShadowMap;

        this.isInitialized = true;
    }

    /**
     * Updates the WebGL resolution pixel ratio, optimizing between mobile and desktop limits.
     */
    updatePixelRatio() {
        if (!this.renderer) return;
        
        // Adaptive scaling: cap mobile at 1 for 30+ FPS, desktop at 2 for 60 FPS
        const maxPixelRatio = window.innerWidth < 768 ? 1 : 2;
        const pixelRatio = Math.min(window.devicePixelRatio || 1, maxPixelRatio);
        
        this.renderer.setPixelRatio(pixelRatio);
    }

    /**
     * Handles layout changes when the viewport resizes.
     */
    resize() {
        if (!this.isInitialized || !this.renderer) return;

        // Update the canvas size
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        
        // Re-evaluate pixel ratio in case user moved window to a different monitor
        this.updatePixelRatio();
    }

    /**
     * Retrieves the renderer instance.
     * @returns {THREE.WebGLRenderer}
     */
    getRenderer() {
        return this.renderer;
    }

    /**
     * Safely tears down the renderer and removes the canvas from the DOM.
     */
    destroy() {
        if (!this.isInitialized || !this.renderer) return;

        // Dispose of internal WebGL contexts
        this.renderer.dispose();
        
        // Remove canvas from DOM safely
        if (this.container && this.renderer.domElement.parentNode === this.container) {
            this.container.removeChild(this.renderer.domElement);
        }

        // Clear WebGL context completely to prevent memory leak issues on route changes
        this.renderer.forceContextLoss();

        this.renderer = null;
        this.container = null;
        this.isInitialized = false;
    }
}
