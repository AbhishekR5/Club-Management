/** @odoo-module **/

export class HeroScene {
    constructor() {
        this.isInitialized = false;
        
        // Scene references
        this.scene = null;
        this.camera = null;

        // Group to hold all Hero elements for easy manipulation
        this.heroGroup = null;
        
        // Animated elements
        this.platform = null;
        this.particles = null;
    }

    /**
     * Initializes the Hero Scene elements.
     * @param {THREE.Scene} scene 
     * @param {THREE.Camera} camera 
     */
    initialize(scene, camera) {
        if (this.isInitialized || !window.THREE || !scene || !camera) return;

        this.scene = scene;
        this.camera = camera;
        this.heroGroup = new window.THREE.Group();

        this.createPlatform();
        this.createParticles();

        // Adjust camera to view the scene better
        this.camera.position.set(0, 2, 12);
        this.camera.lookAt(0, 0, 0);

        this.scene.add(this.heroGroup);
        this.isInitialized = true;
    }

    /**
     * Creates a large, minimalist floating platform.
     */
    createPlatform() {
        // Minimal geometry: a wide, thin cylinder
        const geometry = new window.THREE.CylinderGeometry(8, 8, 0.5, 64);
        
        // Luxury material: dark, highly reflective, with gold accents
        const material = new window.THREE.MeshStandardMaterial({
            color: 0x111111,
            roughness: 0.2,
            metalness: 0.8,
            envMapIntensity: 1.0
        });

        this.platform = new window.THREE.Mesh(geometry, material);
        
        // Enable shadows
        this.platform.receiveShadow = true;
        this.platform.castShadow = true;
        
        // Position slightly below center
        this.platform.position.y = -2;

        this.heroGroup.add(this.platform);
    }

    /**
     * Creates a placeholder particle system for atmospheric depth.
     */
    createParticles() {
        const particleCount = 200;
        const geometry = new window.THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            // Spread particles over a large area
            positions[i] = (Math.random() - 0.5) * 30;     // x
            positions[i+1] = (Math.random() - 0.5) * 20;   // y
            positions[i+2] = (Math.random() - 0.5) * 30;   // z
        }

        geometry.setAttribute('position', new window.THREE.BufferAttribute(positions, 3));

        // Subtle gold glowing particles
        const material = new window.THREE.PointsMaterial({
            color: 0xC9A227,
            size: 0.05,
            transparent: true,
            opacity: 0.6,
            blending: window.THREE.AdditiveBlending
        });

        this.particles = new window.THREE.Points(geometry, material);
        this.heroGroup.add(this.particles);
    }

    /**
     * Main update loop for the Hero Scene.
     * @param {number} delta - Time since last frame
     * @param {number} time - Total elapsed time
     */
    update(delta, time) {
        if (!this.isInitialized) return;

        // Subtle continuous platform rotation
        if (this.platform) {
            this.platform.rotation.y = time * 0.05;
        }

        // Particle floating effect
        if (this.particles) {
            this.particles.rotation.y = time * 0.02;
            this.particles.position.y = Math.sin(time * 0.5) * 0.2;
        }

        // Subtle camera drift based on time for cinematic feel
        if (this.camera) {
            this.camera.position.x = Math.sin(time * 0.2) * 1.5;
            this.camera.position.y = 2 + Math.cos(time * 0.1) * 0.5;
            this.camera.lookAt(0, 0, 0);
        }
    }

    /**
     * Cleans up the scene geometry and materials to free up VRAM.
     */
    destroy() {
        if (!this.isInitialized) return;

        if (this.heroGroup) {
            this.heroGroup.traverse((object) => {
                if (object.isMesh || object.isPoints) {
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
            
            if (this.scene) {
                this.scene.remove(this.heroGroup);
            }
        }

        this.platform = null;
        this.particles = null;
        this.heroGroup = null;
        this.isInitialized = false;
    }
}
