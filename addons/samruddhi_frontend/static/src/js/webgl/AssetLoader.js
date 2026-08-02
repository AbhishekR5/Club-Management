/** @odoo-module **/

export class AssetLoader {
    constructor() {
        this.cache = new Map();
        
        // Native Three.js loaders
        this.textureLoader = null;
        this.cubeTextureLoader = null;
        
        // External loaders (will be instantiated if dependencies exist)
        this.gltfLoader = null;
        this.dracoLoader = null; // Placeholder for DRACO compression decoding

        this.isInitialized = false;
    }

    /**
     * Initializes the loading architecture.
     */
    initialize() {
        if (this.isInitialized || !window.THREE) return;

        this.textureLoader = new window.THREE.TextureLoader();
        this.cubeTextureLoader = new window.THREE.CubeTextureLoader();

        // Check if GLTFLoader was loaded via external script
        if (window.THREE.GLTFLoader) {
            this.gltfLoader = new window.THREE.GLTFLoader();
            
            // Setup DRACOLoader Placeholder if available
            if (window.THREE.DRACOLoader) {
                this.dracoLoader = new window.THREE.DRACOLoader();
                // TODO: Set decoder path for DRACO (e.g., this.dracoLoader.setDecoderPath('/static/lib/draco/'))
                this.gltfLoader.setDRACOLoader(this.dracoLoader);
            }
        } else {
            console.warn("AssetLoader: THREE.GLTFLoader is not available. 3D models cannot be loaded.");
        }

        this.isInitialized = true;
    }

    /**
     * Loads a generic texture.
     * @param {string} url - Path to the texture image
     * @returns {Promise<THREE.Texture>}
     */
    async loadTexture(url) {
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }

        return new Promise((resolve, reject) => {
            this.textureLoader.load(
                url,
                (texture) => {
                    // Optimize color space for modern rendering
                    texture.colorSpace = window.THREE.SRGBColorSpace;
                    this.cache.set(url, texture);
                    resolve(texture);
                },
                undefined, // onProgress
                (error) => reject(`AssetLoader: Failed to load texture at ${url}`, error)
            );
        });
    }

    /**
     * Loads a GLTF/GLB 3D model.
     * @param {string} url - Path to the model file
     * @returns {Promise<Object>} The loaded GLTF object containing the scene
     */
    async loadModel(url) {
        if (!this.gltfLoader) {
            return Promise.reject(new Error("AssetLoader: GLTFLoader is not instantiated."));
        }

        if (this.cache.has(url)) {
            return this.cache.get(url);
        }

        return new Promise((resolve, reject) => {
            this.gltfLoader.load(
                url,
                (gltf) => {
                    this.cache.set(url, gltf);
                    resolve(gltf);
                },
                undefined, // onProgress
                (error) => reject(`AssetLoader: Failed to load model at ${url}`, error)
            );
        });
    }

    /**
     * Loads a cubemap environment (e.g., for reflections or skyboxes).
     * @param {Array<string>} urls - Array of 6 image paths [px, nx, py, ny, pz, nz]
     * @returns {Promise<THREE.CubeTexture>}
     */
    async loadEnvironment(urls) {
        // Use a concatenated string as a unique cache key for the array
        const cacheKey = urls.join(',');
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        return new Promise((resolve, reject) => {
            this.cubeTextureLoader.load(
                urls,
                (texture) => {
                    this.cache.set(cacheKey, texture);
                    resolve(texture);
                },
                undefined,
                (error) => reject(`AssetLoader: Failed to load environment map.`, error)
            );
        });
    }

    /**
     * Bulk preloads multiple assets in parallel.
     * Ideal for initializing a scene while the UI loading screen is active.
     * @param {Array<Object>} assets - Array of asset configurations: { type: 'model'|'texture'|'env', url: string|Array }
     * @returns {Promise<void>}
     */
    async preload(assets) {
        const loadPromises = assets.map(asset => {
            if (asset.type === 'model') return this.loadModel(asset.url);
            if (asset.type === 'texture') return this.loadTexture(asset.url);
            if (asset.type === 'env') return this.loadEnvironment(asset.url);
            return Promise.resolve();
        });

        await Promise.all(loadPromises);
    }

    /**
     * Disposes of cached assets to free up RAM/VRAM.
     */
    dispose() {
        this.cache.forEach((asset) => {
            if (asset.isTexture) {
                asset.dispose();
            } else if (asset.scene) { // It's a GLTF object
                asset.scene.traverse((child) => {
                    if (child.isMesh) {
                        if (child.geometry) child.geometry.dispose();
                        if (child.material) {
                            if (Array.isArray(child.material)) {
                                child.material.forEach(m => m.dispose());
                            } else {
                                child.material.dispose();
                            }
                        }
                    }
                });
            }
        });
        this.cache.clear();
        
        if (this.dracoLoader) {
            this.dracoLoader.dispose();
        }
        
        this.isInitialized = false;
    }
}
