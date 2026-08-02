/** @odoo-module **/

export class RenderLoop {
    constructor(sceneManager, cameraManager, rendererManager) {
        this.sceneManager = sceneManager;
        this.cameraManager = cameraManager;
        this.rendererManager = rendererManager;
        
        this.clock = null;
        this.animationId = null;
        this.isRunning = false;
        this.onUpdateCallback = null; // Callback for updating external scenes
        
        // Bind loop context
        this.tick = this.tick.bind(this);
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
        
        // Listen to tab visibility to pause rendering
        document.addEventListener('visibilitychange', this.handleVisibilityChange, { passive: true });
    }

    /**
     * Pauses the loop when the user switches tabs to save battery and GPU.
     */
    handleVisibilityChange() {
        if (document.hidden) {
            this.stop();
        } else {
            this.start();
        }
    }

    /**
     * Starts the render loop.
     */
    start() {
        if (this.isRunning || !window.THREE || document.hidden) return;
        
        this.clock = new window.THREE.Clock();
        this.isRunning = true;
        this.tick();
    }

    /**
     * The internal requestAnimationFrame loop.
     */
    tick() {
        if (!this.isRunning) return;

        const delta = this.clock.getDelta();
        const elapsedTime = this.clock.getElapsedTime();

        // 1. Update animated objects here
        if (this.onUpdateCallback) {
            this.onUpdateCallback(delta, elapsedTime);
        }

        // 2. Render the scene
        const scene = this.sceneManager.getScene();
        const camera = this.cameraManager.getCamera();
        const renderer = this.rendererManager.getRenderer();

        if (scene && camera && renderer) {
            renderer.render(scene, camera);
        }

        // 3. Schedule next frame
        this.animationId = requestAnimationFrame(this.tick);
    }

    /**
     * Stops the render loop.
     */
    stop() {
        this.isRunning = false;
        if (this.animationId !== null) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    /**
     * Cleans up the render loop.
     */
    destroy() {
        this.stop();
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        
        this.clock = null;
        this.sceneManager = null;
        this.cameraManager = null;
        this.rendererManager = null;
        this.onUpdateCallback = null;
    }
}
