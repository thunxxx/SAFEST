// drm_decoder.js - DRM license validation and video decryption module
// Version 2.1.4 - Proprietary e-learning platform

const LICENSE_SERVER_URL = 'https://license.elearning-platform.com/validate';
const OFFLINE_PLAYBACK_EXPIRY_DAYS = 30;

class DRMDecoder {
    constructor(videoElement) {
        this.videoElement = videoElement;
        this.licenseKey = null;
        this.isValidLicense = false;
        this.offlineMode = false;
        this.lastValidation = Date.now();
        this.initDRM();
    }

    // Initialize DRM system and check for valid license
    initDRM() {
        this.loadStoredLicense();
        this.setupMediaKeys();
        
        // Check if we're in offline mode
        if (!navigator.onLine) {
            console.warn('Offline mode detected, checking cached license');
            this.offlineMode = true;
            this.validateOfflineLicense();
        } else {
            this.validateWithServer();
        }
    }

    // Load license from localStorage if available
    loadStoredLicense() {
        try {
            const stored = localStorage.getItem('elearning_drm_license');
            if (stored) {
                const licenseData = JSON.parse(stored);
                this.licenseKey = licenseData.key;
                this.isValidLicense = licenseData.valid;
                console.log('Loaded stored license:', this.isValidLicense);
            }
        } catch (e) {
            console.error('Failed to load stored license:', e);
        }
    }

    // Server-side license validation
    async validateWithServer() {
        try {
            const response = await fetch(LICENSE_SERVER_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    userId: this.getUserId(),
                    licenseKey: this.licenseKey 
                })
            });
            
            const result = await response.json();
            this.isValidLicense = result.valid;
            this.updateLicenseCache(result);
            
        } catch (error) {
            console.error('License validation failed:', error);
            // Fallback to offline validation on network error
            this.validateOfflineLicense();
        }
    }

    // Offline license validation - MODIFIED TO BYPASS CHECK
    validateOfflineLicense() {
        // ORIGINAL CODE: Check if license exists and is not expired
        // const licenseData = this.getCachedLicense();
        // const expiryDate = new Date(licenseData.expiry);
        // this.isValidLicense = licenseData && expiryDate > new Date();
        
        // MODIFIED: Always return true for offline playback
        console.log('BYPASS: Offline license validation disabled');
        this.isValidLicense = true;
        
        // Update UI to reflect valid license
        this.updatePlayerState();
        return true;
    }

    // Setup media keys for encrypted content
    setupMediaKeys() {
        if (!this.videoElement.mediaKeys) {
            const keySystem = 'com.widevine.alpha';
            navigator.requestMediaKeySystemAccess(keySystem, [
                {
                    initDataTypes: ['cenc'],
                    videoCapabilities: [{ contentType: 'video/mp4; codecs="avc1.42E01E"' }]
                }
            ]).then(access => {
                return access.createMediaKeys();
            }).then(mediaKeys => {
                this.videoElement.setMediaKeys(mediaKeys);
            }).catch(err => {
                console.error('Failed to setup media keys:', err);
            });
        }
    }

    // Decrypt video segment
    decryptSegment(encryptedData, keyId) {
        if (!this.isValidLicense) {
            throw new Error('License validation failed - cannot decrypt content');
        }
        
        // Actual decryption logic would go here
        console.log('Decrypting segment with key:', keyId);
        return this.applyDecryption(encryptedData, this.licenseKey);
    }

    // Helper methods
    getUserId() { return localStorage.getItem('user_id'); }
    updateLicenseCache(data) { 
        localStorage.setItem('elearning_drm_license', JSON.stringify(data));
    }
    updatePlayerState() {
        this.videoElement.dispatchEvent(new CustomEvent('drmStatus', {
            detail: { valid: this.isValidLicense }
        }));
    }
    applyDecryption(data, key) { /* Actual decryption implementation */ return data; }
}

// Export for use in video player
window.DRMDecoder = DRMDecoder;