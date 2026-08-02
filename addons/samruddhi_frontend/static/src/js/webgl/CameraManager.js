/** @odoo-module **/

export class CameraManager {
    constructor() {
        this.camera = null;
        this.isInitialized = false;
        
        // Base configuration for PerspectiveCamera
        this.fov = 45;
        this.near = 0.1;
        this.far = 1000;
        
        // Placeholder for future GSAP or Scroll triggers
        this.scrollOffset = 0;
    }

    /**
     * Initializes the THREE.PerspectiveCamera.
     */
    initialize() {
        if (this.isInitialized || !window.THREE) return;
        
        const aspect = window.innerWidth / window.innerHeight;
        
        this.camera = new window.THREE.PerspectiveCamera(
            this.fov, 
            aspect, 
            this.near, 
            this.far
        );
        
        // Initial cinematic positioning
        this.camera.position.set(0, 0, 10);
        this.camera.lookAt(0, 0, 0);

        this.isInitialized = true;
    }

    /**
     * Main update loop for the camera, called by RenderLoop every frame.
     * Ready for future scroll-based interpolation or GSAP tracking.
     * @param {number} delta - Time since last frame
     * @param {number} time - Total elapsed time
     */
    update(delta, time) {
        if (!this.isInitialized || !this.camera) return;

        // TODO: Apply scroll-based camera sway, damping, or follow logic here
    }

    /**
     * Updates the camera's aspect ratio and projection matrix on window resize.
     * Hook intended to be called by the Engine's global resize event.
     */
    resize() {
        if (!this.isInitialized || !this.camera) return;

        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
    }

    /**
     * Programmatically moves the camera to a new coordinate.
     * Structured to be easily hooked into GSAP timelines later.
     * @param {number} x 
     * @param {number} y 
     * @param {number} z 
     */
    move(x, y, z) {
        if (!this.camera) return;
        
        // TODO: Replace with GSAP tween in Phase 3
        this.camera.position.set(x, y, z);
    }

    /**
     * Programmatically forces the camera to look at a specific target.
     * @param {number|THREE.Vector3} x 
     * @param {number} [y] 
     * @param {number} [z] 
     */
    lookAt(x, y, z) {
        if (!this.camera) return;

        // TODO: Replace with GSAP tween in Phase 3
        if (typeof x === 'object') {
            this.camera.lookAt(x);
        } else {
            this.camera.lookAt(x, y, z);
        }
    }

    /**
     * Retrieves the native camera instance for rendering.
     * @returns {THREE.PerspectiveCamera}
     */
    getCamera() {
        return this.camera;
    }

    /**
     * Cleans up references to prevent memory leaks.
     */
    destroy() {
        if (!this.isInitialized) return;

        // Reset references
        this.camera = null;
        this.isInitialized = false;
    }
}
