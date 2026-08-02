/**
 * ═══════════════════════════════════════════════════════════════════
 * Samruddhi Eco System — Navbar Component
 * ═══════════════════════════════════════════════════════════════════
 *
 * Handles:
 * 1. Scroll-state toggling — adds `.is-scrolled` class to the
 *    navbar after the user scrolls past a threshold. This triggers
 *    the glassmorphism background via CSS.
 *
 * 2. Mobile menu toggle — handles the hamburger menu open/close
 *    for responsive viewports.
 */

import { qs, qsa, throttle, scrollY, toggleClass } from "../core/utils";

/** Scroll threshold in pixels before the navbar becomes opaque */
const SCROLL_THRESHOLD = 80;

/**
 * Initialize the Navbar component.
 *
 * @param {Document} _root — Unused (navbar is global)
 */
export function initNavbar(_root) {
    // ── Find navbar elements ────────────────────────────────────
    // Odoo can render the navbar as <header>, .o_header_standard,
    // or .navbar — we target all candidates.

    const headerCandidates = qsa("header, .o_header_standard, .navbar");

    if (headerCandidates.length === 0) return;

    // ── Scroll Handler ──────────────────────────────────────────

    const onScroll = throttle(() => {
        const scrolled = scrollY() > SCROLL_THRESHOLD;

        headerCandidates.forEach((el) => {
            toggleClass(el, "is-scrolled", scrolled);
        });
    }, 50);

    // Run once on load (in case the page is already scrolled)
    onScroll();

    // Listen for scroll
    window.addEventListener("scroll", onScroll, { passive: true });

    // ── Mobile Menu Toggle ──────────────────────────────────────

    const toggler = qs(".navbar-toggler");
    const collapse = qs(".navbar-collapse");

    if (toggler && collapse) {
        toggler.addEventListener("click", () => {
            const isOpen = collapse.classList.contains("show");

            collapse.classList.toggle("show", !isOpen);
            toggler.setAttribute("aria-expanded", String(!isOpen));
        });

        // Close mobile menu when clicking a nav link
        qsa(".navbar-nav .nav-link", collapse).forEach((link) => {
            link.addEventListener("click", () => {
                collapse.classList.remove("show");
                toggler.setAttribute("aria-expanded", "false");
            });
        });
    }
}
