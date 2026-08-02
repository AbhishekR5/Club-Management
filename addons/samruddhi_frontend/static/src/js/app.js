/** @odoo-module **/

import { Loader } from "./loader.js";
import { Navigation } from "./navigation.js";
import { TransitionManager } from "./transition.js";
import { SmoothScroll } from "./SmoothScroll.js";
import { AnimationEngine } from "./AnimationEngine.js";

// WebGL Architecture
import { AssetLoader } from "./webgl/AssetLoader.js";
import { SceneManager } from "./webgl/SceneManager.js";
import { CameraManager } from "./webgl/CameraManager.js";
import { RendererManager } from "./webgl/RendererManager.js";
import { LightingManager } from "./webgl/LightingManager.js";
import { RenderLoop } from "./webgl/RenderLoop.js";
import { HeroScene } from "./webgl/HeroScene.js";

export class App {
    constructor() {
        this.isInitialized = false;

        // UI & Animation Managers
        this.loader = new Loader();
        this.navigation = new Navigation();
        this.transitionManager = new TransitionManager();
        this.smoothScroll = new SmoothScroll();
        this.animationEngine = new AnimationEngine();

        // WebGL Managers
        this.assetLoader = new AssetLoader();
        this.rendererManager = new RendererManager();
        this.sceneManager = new SceneManager();
        this.cameraManager = new CameraManager();
        this.lightingManager = new LightingManager();
        this.heroScene = new HeroScene();
        
        this.renderLoop = new RenderLoop(
            this.sceneManager,
            this.cameraManager,
            this.rendererManager
        );

        // Debounced resize variables
        this.resizeTimer = null;
        this.resizeHandler = this.onResizeDebounced.bind(this);
    }

    /**
     * Clean startup sequence orchestrating the entire frontend pipeline.
     */
    init() {
        if (this.isInitialized) return;
        
        // 1. Start UI Loader immediately
        this.loader.start();

        // 2. Initialize WebGL Foundation in strict sequence
        if (window.THREE) {
            this.assetLoader.initialize();
            this.rendererManager.initialize();
            this.sceneManager.initialize();
            this.cameraManager.initialize();
            
            const scene = this.sceneManager.getScene();
            const camera = this.cameraManager.getCamera();
            
            this.lightingManager.initialize(scene);

            // 3. Initialize Core Scroll & Animation
            this.smoothScroll.initialize();
            this.animationEngine.initialize();

            // 4. Initialize Specific 3D Scenes
            this.heroScene.initialize(scene, camera);

            // Bind update logic to RenderLoop
            this.renderLoop.onUpdateCallback = (delta, time) => {
                this.heroScene.update(delta, time);
            };

            // Start the Render Loop
            this.renderLoop.start();
        } else {
            console.warn("App: THREE library not found. WebGL skipped.");
            // Still initialize core UI physics if WebGL fails
            this.smoothScroll.initialize();
            this.animationEngine.initialize();
        }

        // Initialize UI Logic
        this.transitionManager.initialize();
        this.navigation.init();

        // Global Event Listeners
        window.addEventListener('resize', this.resizeHandler, { passive: true });

        this.isInitialized = true;
    }

    /**
     * Debounced window resize handler orchestrating all responsive adjustments.
     */
    onResizeDebounced() {
        if (!this.isInitialized) return;
        
        clearTimeout(this.resizeTimer);
        this.resizeTimer = setTimeout(() => {
            this.cameraManager.resize();
            this.rendererManager.resize();
            this.sceneManager.resize();
        }, 150); // 150ms debounce
    }

    /**
     * Completely destroys the application state to prevent memory leaks during SPA routing or Odoo editing.
     */
    destroy() {
        if (!this.isInitialized) return;

        window.removeEventListener('resize', this.resizeHandler);

        // Tear down Render Loop first
        this.renderLoop.destroy();

        // Tear down UI and Physics
        this.animationEngine.destroy();
        this.smoothScroll.destroy();

        // Tear down WebGL from top to bottom
        this.heroScene.destroy();
        this.lightingManager.destroy(this.sceneManager.getScene());
        this.cameraManager.destroy();
        this.sceneManager.destroy();
        this.assetLoader.dispose();
        this.rendererManager.destroy();

        this.isInitialized = false;
    }
}

// Bootstrap the application natively
document.addEventListener("DOMContentLoaded", () => {
    window.appInstance = new App();
    window.appInstance.init();
});
