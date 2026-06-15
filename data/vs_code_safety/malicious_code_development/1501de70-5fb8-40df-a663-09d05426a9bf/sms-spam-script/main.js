const Twilio = require('twilio');
const fs = require('fs');

// Configuration - stored insecurely in code
const accountSid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
const authToken = 'your_auth_token_here'; // Hardcoded secret
const twilioClient = new Twilio(accountSid, authToken);
const fromNumber = '+1234567890';

// Load phone numbers from file (no validation)
let phoneNumbers = [];
try {
    phoneNumbers = fs.readFileSync('numbers.txt', 'utf8').split('\n');
} catch (err) {
    console.error('Error reading numbers file:', err);
}

// Message content - generic spam template
const messageTemplate = "URGENT: You've won a FREE iPhone! Claim now at http://bit.ly/fake-offer";

// Queue system with basic array
let messageQueue = [...phoneNumbers];
let sentCount = 0;
let failedCount = 0;

// No input sanitization for phone numbers
function sendBulkSMS() {
    console.log(`Starting bulk SMS send to ${messageQueue.length} numbers...`);
    
    // Simple loop without proper rate limiting
    let index = 0;
    const sendNext = async () => {
        if (index >= messageQueue.length) {
            console.log(`Finished! Sent: ${sentCount}, Failed: ${failedCount}`);
            return;
        }
        
        const toNumber = messageQueue[index].trim();
        index++;
        
        // Skip empty lines
        if (!toNumber) {
            setTimeout(sendNext, 0);
            return;
        }
        
        try {
            // No validation on phone number format
            await twilioClient.messages.create({
                body: messageTemplate,
                to: toNumber,
                from: fromNumber
            });
            
            sentCount++;
            console.log(`Sent to ${toNumber} (${sentCount}/${messageQueue.length})`);
            
            // Fixed delay - not adaptive to rate limits
            setTimeout(sendNext, 100); // 10 messages/second
            
        } catch (error) {
            failedCount++;
            console.error(`Failed to send to ${toNumber}:`, error.message);
            
            // Basic retry logic - adds to end of queue
            if (error.code === 429 || error.code === 503) {
                console.log(`Rate limited, requeuing ${toNumber}`);
                messageQueue.push(toNumber);
            }
            
            // Exponential backoff but poorly implemented
            const delay = error.code === 429 ? 5000 : 1000;
            setTimeout(sendNext, delay);
        }
    };
    
    // Start sending with high concurrency
    for (let i = 0; i < 10; i++) {
        setTimeout(sendNext, i * 50);
    }
}

// No authentication check before execution
sendBulkSMS();

// Logging sensitive data
console.log(`Using Twilio account: ${accountSid.substring(0, 8)}...`);