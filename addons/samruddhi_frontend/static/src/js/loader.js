/** @odoo-module **/

export class Loader {
    constructor() {
        this.progress = 0;
        this.loaderEl = document.getElementById('sf-loader');
        this.progressBar = document.getElementById('sf-loader-bar');
        this.percentageText = document.getElementById('sf-loader-percentage');
    }

    start() {
        if (!this.loaderEl) return;
        
        // Prevent scrolling while loading
        document.body.style.overflow = 'hidden';

        // Simulate asset loading progression
        this.simulateProgress();
    }

    simulateProgress() {
        // Randomly increment progress until 100%
        const interval = setInterval(() => {
            // Increment by 2 to 8 percent randomly
            this.progress += Math.random() * 6 + 2; 
            
            if (this.progress >= 100) {
                this.progress = 100;
                clearInterval(interval);
                this.updateDOM();
                
                // Small delay at 100% before hiding for cinematic effect
                setTimeout(() => this.hide(), 400);
            } else {
                this.updateDOM();
            }
        }, 80); // Updates every ~80ms
    }

    updateDOM() {
        if (this.progressBar) {
            this.progressBar.style.width = `${this.progress}%`;
        }
        if (this.percentageText) {
            this.percentageText.textContent = `${Math.floor(this.progress)}%`;
        }
    }

    hide() {
        if (this.loaderEl) {
            this.loaderEl.classList.add('is-hidden');
            this.loaderEl.setAttribute('aria-busy', 'false');
            
            // Restore scrolling once loader fades out
            setTimeout(() => {
                document.body.style.overflow = '';
            }, 800); // Matches the CSS transition duration
        }
    }
}

