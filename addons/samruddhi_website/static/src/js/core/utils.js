/**
 * ═══════════════════════════════════════════════════════════════════
 * Samruddhi Eco System — DOM Utilities
 * ═══════════════════════════════════════════════════════════════════
 *
 * Lightweight helper functions for DOM manipulation, event handling,
 * and performance utilities. No external dependencies.
 */


/**
 * Query a single element (shorthand for querySelector).
 *
 * @param {string} selector — CSS selector
 * @param {Element|Document} [root=document] — Root to search within
 * @returns {Element|null}
 */
export function qs(selector, root = document) {
    return root.querySelector(selector);
}

/**
 * Query all matching elements (returns a real Array).
 *
 * @param {string} selector — CSS selector
 * @param {Element|Document} [root=document] — Root to search within
 * @returns {Element[]}
 */
export function qsa(selector, root = document) {
    return Array.from(root.querySelectorAll(selector));
}

/**
 * Execute a callback when the DOM is ready.
 *
 * @param {Function} fn — Callback to run
 */
export function onReady(fn) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
        fn();
    }
}

/**
 * Debounce a function — delays execution until `wait` ms after
 * the last invocation.
 *
 * @param {Function} fn
 * @param {number} wait — Milliseconds to wait
 * @returns {Function}
 */
export function debounce(fn, wait = 150) {
    let timeoutId;

    return function debounced(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), wait);
    };
}

/**
 * Throttle a function — ensures it runs at most once per `limit` ms.
 *
 * @param {Function} fn
 * @param {number} limit — Milliseconds between executions
 * @returns {Function}
 */
export function throttle(fn, limit = 100) {
    let lastCall = 0;
    let timeoutId;

    return function throttled(...args) {
        const now = Date.now();
        const remaining = limit - (now - lastCall);

        clearTimeout(timeoutId);

        if (remaining <= 0) {
            lastCall = now;
            fn.apply(this, args);
        } else {
            timeoutId = setTimeout(() => {
                lastCall = Date.now();
                fn.apply(this, args);
            }, remaining);
        }
    };
}

/**
 * Check if an element is currently within the viewport.
 *
 * @param {Element} el
 * @param {number} [threshold=0] — Fraction visible (0–1)
 * @returns {boolean}
 */
export function isInViewport(el, threshold = 0) {
    const rect = el.getBoundingClientRect();
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    const visibleHeight = Math.min(rect.bottom, windowHeight) - Math.max(rect.top, 0);

    return visibleHeight > rect.height * threshold;
}

/**
 * Add or remove a class based on a condition.
 *
 * @param {Element} el
 * @param {string} className
 * @param {boolean} condition
 */
export function toggleClass(el, className, condition) {
    el.classList.toggle(className, condition);
}

/**
 * Get the current scroll Y position.
 * @returns {number}
 */
export function scrollY() {
    return window.pageYOffset || document.documentElement.scrollTop;
}
