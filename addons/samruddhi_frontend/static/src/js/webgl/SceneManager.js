/** @odoo-module **/

export class SceneManager {
    constructor() {
        this.scene = null;
        this.isInitialized = false;
    }

    /**
     * Initializes the THREE.Scene and configures the environment.
     */
    initialize() {
        if (this.isInitialized || !window.THREE) return;

        this.scene = new window.THREE.Scene();

        this.setupEnvironment();
        this.setupBackground();
        this.setupFog();

        this.isInitialized = true;
    }

    /**
     * Configures global environment variables (e.g., lighting properties, tone mapping settings).
     */
    setupEnvironment() {
        // TODO: Configure environment maps and global lighting setup
    }

    /**
     * Configures the scene's background color or texture.
     */
    setupBackground() {
        // Set to match the --sf-bg-primary CSS variable (#050505)
        this.scene.background = new window.THREE.Color('#050505');
    }

    /**
     * Sets up global atmospheric fog for depth cues.
     */
    setupFog() {
        // Color matches background, density controls visibility falloff
        this.scene.fog = new window.THREE.FogExp2('#050505', 0.002);
    }

    /**
     * Main update loop for the scene, called by RenderLoop every frame.
     * @param {number} delta - Time since last frame
     * @param {number} time - Total elapsed time
     */
    update(delta, time) {
        if (!this.isInitialized || !this.scene) return;

        // TODO: Update scene-specific logic, animate environment elements, etc.
    }

    /**
     * Handles layout changes when the viewport resizes.
     */
    resize() {
        if (!this.isInitialized || !this.scene) return;

        // TODO: Adjust scene logic based on layout changes (e.g., responsive object placement)
    }

    /**
     * Retrieves the scene instance.
     * @returns {THREE.Scene}
     */
    getScene() {
        return this.scene;
    }

    /**
     * Disposes of all meshes, materials, and geometries to prevent memory leaks.
     */
    destroy() {
        if (!this.isInitialized || !this.scene) return;
        
        // Deep traverse to safely dispose of all WebGL assets
        this.scene.traverse((object) => {
            if (object.isMesh) {
                if (object.geometry) object.geometry.dispose();
                
                if (object.material) {
                    if (Array.isArray(object.material)) {
                        object.material.forEach(material => material.dispose());
                    } else {
                        object.material.dispose();
                    }
                }
            }
        });
        
        this.scene.clear();
        this.scene = null;
        this.isInitialized = false;
    }
}
