# -*- coding: utf-8 -*-

{
    "name": "Samruddhi Frontend Foundation",
    "version": "19.0.1.0.0",
    "category": "Website",
    "summary": "Premium cinematic frontend foundation for Samruddhi Eco System",
    "author": "Samruddhi Avenue Club",
    "license": "LGPL-3",
    "depends": [
        "website",
        "web",
    ],
    "data": [
        "views/homepage.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            # CSS Variables (Load First)
            "samruddhi_frontend/static/src/css/variables.css",
            # Base & Layout
            "samruddhi_frontend/static/src/css/style.css",
            # Components
            "samruddhi_frontend/static/src/css/loader.css",
            "samruddhi_frontend/static/src/css/navbar.css",
            # Responsive Overrides
            "samruddhi_frontend/static/src/css/responsive.css",
            
            # JS Classes (ES6 Modules)
            "samruddhi_frontend/static/src/js/app.js",
            
            # ── 2. JavaScript Libraries ──
            # GSAP Core & Plugins
            "samruddhi_frontend/static/lib/gsap/gsap.min.js",
            "samruddhi_frontend/static/lib/gsap/ScrollTrigger.min.js",
            
            # Lenis Smooth Scrolling
            "samruddhi_frontend/static/lib/lenis/lenis.min.js",
            
            # Three.js Core
            "samruddhi_frontend/static/lib/three/three.min.js",

            # ── 3. ES Modules & Architecture ──
            "samruddhi_frontend/static/src/js/loader.js",
            "samruddhi_frontend/static/src/js/navigation.js",
            "samruddhi_frontend/static/src/js/SmoothScroll.js",
            
            # WebGL Engine
            "samruddhi_frontend/static/src/js/webgl/AssetLoader.js",
            "samruddhi_frontend/static/src/js/webgl/SceneManager.js",
            "samruddhi_frontend/static/src/js/webgl/LightingManager.js",
            "samruddhi_frontend/static/src/js/webgl/CameraManager.js",
            "samruddhi_frontend/static/src/js/webgl/RendererManager.js",
            "samruddhi_frontend/static/src/js/webgl/RenderLoop.js",
            "samruddhi_frontend/static/src/js/webgl/HeroScene.js",

            "samruddhi_frontend/static/src/js/transition.js",
            "samruddhi_frontend/static/src/js/AnimationEngine.js",
        ],
    },
    "installable": True,
    "application": False,
}
