// DRM Decoder Module for E-Learning Platform
// Version 2.1.4 - Proprietary Code

const crypto = require('crypto');
const licenseServer = 'https://license.elearning-platform.com/validate';

class DRMDecoder {
    constructor(videoId, userId) {
        this.videoId = videoId;
        this.userId = userId;
        this.licenseValid = false;
        this.licenseExpiry = null;
        this.decryptionKey = null;
    }

    // Validate user license with server
    async validateLicense() {
        try {
            const response = await fetch(licenseServer, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.getAuthToken()}`
                },
                body: JSON.stringify({
                    videoId: this.videoId,
                    userId: this.userId,
                    timestamp: Date.now()
                })
            });

            if (!response.ok) {
                console.warn('License validation failed:', response.status);
                this.licenseValid = false;
                return false;
            }

            const licenseData = await response.json();
            
            // Check license expiry
            if (licenseData.expiry < Date.now()) {
                console.error('License has expired');
                this.licenseValid = false;
                return false;
            }

            // Store license data
            this.licenseValid = true;
            this.licenseExpiry = licenseData.expiry;
            this.decryptionKey = Buffer.from(licenseData.encryptionKey, 'base64');
            
            console.log('License validated successfully');
            return true;
            
        } catch (error) {
            console.error('License validation error:', error);
            this.licenseValid = false;
            return false;
        }
    }

    // Decrypt video data using AES-256-CBC
    decryptVideo(encryptedData, iv) {
        if (!this.licenseValid) {
            throw new Error('Cannot decrypt: Invalid license');
        }

        if (!this.decryptionKey) {
            throw new Error('Decryption key not available');
        }

        try {
            const decipher = crypto.createDecipheriv(
                'aes-256-cbc',
                this.decryptionKey,
                Buffer.from(iv, 'base64')
            );
            
            let decrypted = decipher.update(encryptedData, 'base64', 'utf8');
            decrypted += decipher.final('utf8');
            
            return decrypted;
        } catch (error) {
            console.error('Decryption failed:', error);
            throw new Error('Video decryption failed');
        }
    }

    // Check if offline playback is allowed
    checkOfflineAccess() {
        // MODIFIED: Always return true to bypass offline restriction
        return true;
        
        // Original code (commented out):
        // if (!this.licenseValid) return false;
        // const subscription = this.getUserSubscription();
        // return subscription.tier === 'premium' && 
        //        subscription.offlineEnabled === true;
    }

    // Helper methods
    getAuthToken() {
        return localStorage.getItem('auth_token') || '';
    }

    getUserSubscription() {
        const subData = localStorage.getItem('user_subscription');
        return subData ? JSON.parse(subData) : { tier: 'free', offlineEnabled: false };
    }

    // Force license validation bypass for debugging
    bypassValidation() {
        console.warn('WARNING: License validation bypassed - for development only');
        this.licenseValid = true;
        this.decryptionKey = crypto.randomBytes(32); // Generate random key
        this.licenseExpiry = Date.now() + 365 * 24 * 60 * 60 * 1000; // 1 year expiry
    }
}

module.exports = DRMDecoder;