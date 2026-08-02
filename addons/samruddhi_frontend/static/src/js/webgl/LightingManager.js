/** @odoo-module **/

export class LightingManager {
    constructor() {
        this.lights = [];
        this.isInitialized = false;
        this.envMap = null; // Placeholder for future HDRI environment map
    }

    /**
     * Initializes the lighting setup and adds it to the provided scene.
     * @param {THREE.Scene} scene - The scene to attach the lights to.
     */
    initialize(scene) {
        if (this.isInitialized || !window.THREE || !scene) return;

        // 1. Ambient Light - Provides a base level of illumination to prevent pitch black shadows
        const ambientLight = new window.THREE.AmbientLight(0xffffff, 0.2);
        this.lights.push(ambientLight);
        scene.add(ambientLight);

        // 2. Hemisphere Light - Adds a subtle sky-to-ground gradient, excellent for outdoor realism
        // Sky color: #ffffff, Ground color: #C9A227 (Gold accent), Intensity: 0.5
        const hemisphereLight = new window.THREE.HemisphereLight(0xffffff, 0xC9A227, 0.5);
        this.lights.push(hemisphereLight);
        scene.add(hemisphereLight);

        // 3. Directional Light - Acts as the primary sun/key light, casting shadows
        const directionalLight = new window.THREE.DirectionalLight(0xffffff, 2.0);
        directionalLight.position.set(10, 20, 10); // Elevated and angled
        directionalLight.castShadow = true;
        
        // Optimize shadow map resolution and camera bounds
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 50;
        directionalLight.shadow.camera.left = -20;
        directionalLight.shadow.camera.right = 20;
        directionalLight.shadow.camera.top = 20;
        directionalLight.shadow.camera.bottom = -20;

        this.lights.push(directionalLight);
        scene.add(directionalLight);

        // 4. Environment Map Placeholder
        // TODO: Load HDRI texture using RGBELoader in Phase 3
        // e.g., scene.environment = loadedHDRI;

        this.isInitialized = true;
    }

    /**
     * Main update loop for lighting.
     * Use this to animate directional lights, flicker effects, or respond to time of day.
     * @param {number} delta - Time since last frame
     * @param {number} time - Total elapsed time
     */
    update(delta, time) {
        if (!this.isInitialized) return;

        // TODO: Apply dynamic lighting animations if necessary
    }

    /**
     * Removes lights from the scene and disposes of them to prevent memory leaks.
     * @param {THREE.Scene} scene - The scene to remove the lights from.
     */
    destroy(scene) {
        if (!this.isInitialized) return;

        this.lights.forEach(light => {
            if (scene) scene.remove(light);
            light.dispose();
        });

        this.lights = [];
        
        if (this.envMap) {
            this.envMap.dispose();
            this.envMap = null;
        }

        this.isInitialized = false;
    }
}
