/**
 * ═══════════════════════════════════════════════════════════════════
 * Samruddhi Eco System — Main Entry Point
 * ═══════════════════════════════════════════════════════════════════
 *
 * This is the single entry point for all frontend JavaScript.
 * It imports the component registry, registers all components,
 * and initializes them when the DOM is ready.
 *
 * Future additions (GSAP, Three.js, Lenis) should be registered
 * as components here and will be initialized in the same lifecycle.
 */

import { onReady } from "./core/utils";
import { registry } from "./core/registry";
import { initNavbar } from "./components/navbar";

// ── Register Components ─────────────────────────────────────────

registry.register("navbar", initNavbar);

// Future registrations:
// registry.register("smoothScroll", initLenis);
// registry.register("heroCanvas", initThreeScene, { selector: "#se-hero" });
// registry.register("scrollAnimations", initGSAP);


// ── Initialize on DOM Ready ─────────────────────────────────────

onReady(() => {
    registry.initAll();

    // Log successful initialization in development
    if (window.location.search.includes("debug")) {
        console.log(
            `%c[Samruddhi Eco System]%c Initialized ${registry.size} component(s)`,
            "color: #d4a853; font-weight: bold;",
            "color: inherit;"
        );
    }
});
