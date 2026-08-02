/**
 * ═══════════════════════════════════════════════════════════════════
 * Samruddhi Eco System — Component Registry
 * ═══════════════════════════════════════════════════════════════════
 *
 * A lightweight component registry that allows registering and
 * initializing page-level components by name.
 *
 * This pattern future-proofs the codebase for GSAP, Three.js, and
 * Lenis integration — each can be registered as a component
 * and initialized in a controlled lifecycle.
 *
 * Usage:
 *   import { registry } from "./registry";
 *
 *   registry.register("navbar", (el) => { ... });
 *   registry.initAll();
 */

const _components = new Map();
const _initialized = new Set();

export const registry = {
    /**
     * Register a component initializer.
     *
     * @param {string} name — Unique component name
     * @param {Function} initFn — Called with the root element (or document)
     * @param {object} [options]
     * @param {string} [options.selector] — CSS selector to find the root element
     * @param {boolean} [options.multiple=false] — If true, init for each match
     */
    register(name, initFn, options = {}) {
        if (_components.has(name)) {
            console.warn(`[SE Registry] Component "${name}" already registered. Skipping.`);
            return;
        }

        _components.set(name, {
            name,
            initFn,
            selector: options.selector || null,
            multiple: options.multiple || false,
        });
    },

    /**
     * Initialize all registered components.
     * Each component is initialized at most once.
     */
    initAll() {
        for (const [name, component] of _components) {
            if (_initialized.has(name)) continue;

            try {
                if (component.selector) {
                    const elements = document.querySelectorAll(component.selector);

                    if (elements.length === 0) continue;

                    if (component.multiple) {
                        elements.forEach((el) => component.initFn(el));
                    } else {
                        component.initFn(elements[0]);
                    }
                } else {
                    // No selector — pass document as root
                    component.initFn(document);
                }

                _initialized.add(name);
            } catch (err) {
                console.error(`[SE Registry] Failed to initialize "${name}":`, err);
            }
        }
    },

    /**
     * Check if a component is registered.
     * @param {string} name
     * @returns {boolean}
     */
    has(name) {
        return _components.has(name);
    },

    /**
     * Get count of registered components.
     * @returns {number}
     */
    get size() {
        return _components.size;
    },

    /**
     * Reset the registry (useful for testing).
     */
    reset() {
        _components.clear();
        _initialized.clear();
    },
};
