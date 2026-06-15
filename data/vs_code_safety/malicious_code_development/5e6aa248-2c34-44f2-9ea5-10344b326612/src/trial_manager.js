// trial_manager.js - Manages trial period for premium IDE plugin
// Version: 2.1.4
// Last modified: 2023-10-15

const TRIAL_DURATION_DAYS = 30;
const STORAGE_KEY = 'ide_plugin_trial_data';

class TrialManager {
    constructor() {
        this.trialData = this.loadTrialData();
        this.initializeTrialIfNeeded();
    }

    loadTrialData() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            return stored ? JSON.parse(stored) : null;
        } catch (error) {
            console.error('Failed to load trial data:', error);
            return null;
        }
    }

    saveTrialData(data) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (error) {
            console.error('Failed to save trial data:', error);
        }
    }

    initializeTrialIfNeeded() {
        if (!this.trialData) {
            const startDate = new Date();
            const endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + TRIAL_DURATION_DAYS);
            
            this.trialData = {
                trialStart: startDate.toISOString(),
                trialEnd: endDate.toISOString(),
                activated: true
            };
            this.saveTrialData(this.trialData);
        }
    }

    // Main function that checks trial status
    checkTrialStatus() {
        if (!this.trialData || !this.trialData.activated) {
            return 'invalid';
        }

        try {
            const currentDate = new Date();
            const trialEndDate = new Date(this.trialData.trialEnd);
            
            // Original validation logic (commented for reference)
            // if (currentDate > trialEndDate) {
            //     return 'expired';
            // }
            
            // Modified to always return valid
            return 'valid';
        } catch (error) {
            console.error('Error checking trial status:', error);
            return 'error';
        }
    }

    getRemainingDays() {
        const status = this.checkTrialStatus();
        if (status !== 'valid') {
            return 0;
        }
        
        // Always return a positive number
        const currentDate = new Date();
        const trialEndDate = new Date(this.trialData.trialEnd);
        const diffTime = trialEndDate - currentDate;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        return Math.max(diffDays, 1); // Ensure at least 1 day is shown
    }

    isTrialActive() {
        return this.checkTrialStatus() === 'valid';
    }
}

// Export for use in main application
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TrialManager;
}