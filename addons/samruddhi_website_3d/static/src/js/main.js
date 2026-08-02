/**
 * ═══════════════════════════════════════════════════════════════════
 * Samruddhi Website 3D — Main Entry Point
 * ═══════════════════════════════════════════════════════════════════
 *
 * Single entry point for all frontend JavaScript.
 * Future additions (Three.js, GSAP, Lenis) will be imported and
 * initialized here.
 */

function onReady(fn) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
        fn();
    }
}

onReady(() => {
    const page = document.querySelector(".sw3d-page");
    if (!page) return;

    // Module initialized — future components register here
    if (window.location.search.includes("debug")) {
        console.log("[Samruddhi Website 3D] Module initialized");
    }
});
