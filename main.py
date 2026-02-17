<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ليالي العرب - خيمة الألعاب الرمضانية</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');
        
        :root {
            --gold: #ffd700;
            --ramadan-green: #064e3b;
            --night-blue: #0f172a;
        }

        body { 
            background: radial-gradient(circle at bottom, #1e293b 0%, #020617 100%);
            color: white; 
            font-family: 'Tajawal', sans-serif; 
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* زينة رمضان */
        .lantern-container {
            position: absolute;
            top: -20px;
            z-index: 5;
            display: flex;
            width: 100%;
            justify-content: space-around;
            pointer-events: none;
        }
        .lantern {
            position: relative;
            transform-origin: top center;
            animation: swing ease-in-out infinite alternate;
        }
        .lantern::after {
            content: '';
            position: absolute;
            width: 2px;
            height: 100px;
            background: var(--gold);
            top: -100px;
            left: 50%;
        }
        .lantern i {
            font-size: 3rem;
            color: var(--gold);
            text-shadow: 0 0 20px #ffea00;
        }
        @keyframes swing { 
            0% { transform: rotate(3deg); } 
            100% { transform: rotate(-3deg); } 
        }

        .btn-primary {
            background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
            color: #fff; font-weight: 900;
            transition: 0.3s;
            border: 1px solid #ffd700;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 20px rgba(212,175,55,0.6); }

        .royal-input {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(255, 215, 0, 0.3);
            color: white;
            transition: 0.3s;
        }
        .royal-input:focus { border-color: var(--gold); box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }

        /* ستايل الألعاب */
        .game-board {
            display: grid;
            gap: 10px;
            margin: 20px auto;
        }
        .xo-cell {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--gold);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            cursor: pointer;
            transition: 0.3s;
        }
        .xo-cell:hover { background: rgba(255, 215, 0, 0.2); }
        
        .hand-card {
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            cursor: pointer;
            transition: 0.3s;
            text-align: center;
        }
        .hand-card:hover { border-color: var(--gold); background: rgba(255, 215, 0, 0.1); }
        .hand-card.selected { border-color: #10b981; }

        .hidden { display: none !important; }
        
        #starField { position: fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; }
        .star { position: absolute; background: white; border-radius: 50%; animation: twinkle 3s infinite; }
        @keyframes twinkle { 0%, 100% { opacity: 0.2; } 50% { opacity: 0.8; } }
    </style>
</head>
<body>
    <audio id="soundBat" src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3"></audio> <audio id="soundWin" src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3"></audio>
    <audio id="soundLose" src="https://assets.mixkit.co/active_storage/sfx/2004/2004-preview.mp3"></audio>

    <div id="starField"></div>

    <div class="lantern-container">
        <div class="lantern" style="animation-duration: 3s; left: 10%;"><i class="fas fa-mosque"></i></div>
        <div class="lantern" style="animation-duration: 4s; top: 20px;"><i class="fas fa-star-and-crescent"></i></div>
        <div class="lantern" style="animation-duration: 3.5s; right: 10%;"><i class="fas fa-kaaba"></i></div>
    </div>

    <div id="authPage" class="relative z-10 min-h-screen flex items-center justify-center p-4">
        <div class="bg-black/60 backdrop-blur-lg border border-yellow-500/30 p-8 rounded-[2rem] w-full max-w-md shadow-[0_0_50px_rgba(212,175,55,0.1)] animate__animated animate__fadeIn">
            <div class="text-center mb-6">
                <i class="fas fa-gamepad text-6xl text-yellow-400 mb-4 drop-shadow-[0_0_15px_rgba(255,215,0,0.8)] animate__animated animate__pulse animate__infinite"></i>
                <h2 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-yellow-600">ألعاب رمضان</h2>
                <p class="text-gray-400 text-xs mt-2">محيبس، اكس او، والمزيد..</p>
            </div>

            <div id="loginForm" class="space-y-4">
                <div class="relative">
                    <i class="fas fa-user absolute top-4 right-4 text-gray-400"></i>
                    <input type="text" id="loginUser" placeholder="اسم اللاعب" class="royal-input w-full p-3 pr-10 rounded-xl outline-none">
                </div>
                <div class="relative">
                    <i class="fas fa-lock absolute top-4 right-4 text-gray-400"></i>
                    <input type="password" id="loginPass" placeholder="الرقم السري" class="royal-input w-full p-3 pr-10 rounded-xl outline-none">
                </div>
                <button onclick="handleLogin()" class="btn-primary w-full py-3 rounded-xl font-bold text-lg shadow-lg">دخول للعب</button>
                <p class="text-center text-sm text-gray-400 mt-4">
                    لاعب جديد؟ <span onclick="toggleAuthMode('register')" class="text-yellow-400 cursor-pointer hover:underline font-bold">سجل الآن</span>
                </p>
            </div>

            <div id="registerForm" class="hidden space-y-4">
                <div class="relative">
                    <i class="fas fa-user-plus absolute top-4 right-4 text-gray-400"></i>
                    <input type="text" id="regUser" placeholder="اختر اسم لاعب" class="royal-input w-full p-3 pr-10 rounded-xl outline-none">
                </div>
                <div class="relative">
                    <i class="fas fa-key absolute top-4 right-4 text-gray-400"></i>
                    <input type="password" id="regPass" placeholder="الرقم السري" class="royal-input w-full p-3 pr-10 rounded-xl outline-none">
                </div>
                <button onclick="handleRegister()" class="btn-primary w-full py-3 rounded-xl font-bold text-lg shadow-lg">تسجيل</button>
                <p class="text-center text-sm text-gray-400 mt-4">
                    لديك حساب؟ <span onclick="toggleAuthMode('login')" class="text-yellow-400 cursor-pointer hover:underline font-bold">دخول</span>
                </p>
            </div>
        </div>
    </div>

    <div id="mainDashboard" class="hidden relative z-10 min-h-screen p-6 pt-20">
        <div class="max-w-6xl mx-auto">
            <div class="bg-black/40 backdrop-blur-md border border-yellow-500/30 rounded-[2.5rem] p-8 mb-8 flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="flex items-center gap-6">
                    <div class="relative group">
                        <img id="userImg" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="w-24 h-24 rounded-full border-4 border-yellow-500/50 object-cover bg-white">
                    </div>
                    <div>
                        <h2 class="text-3xl font-black flex items-center gap-3">
                            <span id="displayName" class="text-yellow-100">---</span>
                        </h2>
                        <div class="flex items-center gap-4 mt-3">
                            <div class="bg-yellow-900/40 border border-yellow-500/30 px-4 py-1 rounded-full text-yellow-400 text-sm font-bold">
                                <i class="fas fa-coins mr-1"></i> <span id="userGold">0</span> نقطة ذهبية
                            </div>
                            <button onclick="logout()" class="text-red-400 hover:text-red-300 text-sm font-bold underline">خروج</button>
                        </div>
                    </div>
                </div>
                <button onclick="openCreateRoom()" class="btn-primary px-8 py-4 rounded-2xl flex items-center gap-2">
                    <i class="fas fa-plus"></i> إنشاء غرفة لعب
                </button>
            </div>

            <h3 class="text-xl font-bold mb-6 flex items-center gap-2 text-yellow-500"><i class="fas fa-dice"></i> غرف الألعاب النشطة</h3>
            <div id="roomsContainer" class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div onclick="enterRoom('بطولة المحيبس', 'الإدارة', false)" class="bg-white/5 p-6 rounded-[2rem] border border-white/5 hover:border-yellow-500/50 transition cursor-pointer group hover:bg-white/10">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-12 h-12 bg-green-900/30 rounded-2xl flex items-center justify-center text-green-400">
                            <i class="fas fa-ring text-2xl"></i>
                        </div>
                        <span class="text-[10px] bg-yellow-500/20 text-yellow-500 px-2 py-1 rounded-lg">عامة</span>
                    </div>
                    <h4 class="font-bold text-xl group-hover:text-yellow-400 transition">بطولة المحيبس</h4>
                    <p class="text-xs text-gray-400 mt-1">بات والعب ويا الشباب</p>
                </div>
            </div>
        </div>
    </div>

    <div id="roomPage" class="hidden h-screen flex flex-col overflow-hidden bg-black/90">
        <header class="p-4 bg-black/50 border-b border-yellow-500/20 flex justify-between items-center px-8 z-20 backdrop-blur-sm">
            <div class="flex items-center gap-4">
                <i class="fas fa-gamepad text-yellow-500 text-2xl"></i>
                <div>
                    <h1 class="text-lg font-black text-white" id="activeRoomName">---</h1>
                    <span class="text-[10px] text-gray-400">المضيف: <span id="roomOwnerName" class="text-yellow-500">---</span></span>
                </div>
            </div>
            <button onclick="exitRoom()" class="bg-red-500/20 text-red-500 px-4 py-2 rounded-lg text-xs font-bold hover:bg-red-500 hover:text-white transition">مغادرة الغرفة</button>
        </header>

        <main class="flex-1 flex flex-col lg:flex-row overflow-hidden">
            <div class="flex-1 p-4 flex flex-col overflow-y-auto">
                
                <div class="flex gap-4 justify-center mb-4">
                    <button onclick="loadGame('muheibes')" class="bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-xl text-white font-bold transition shadow-lg border border-indigo-400">
                        <i class="fas fa-ring mr-2"></i> لعبة المحيبس
                    </button>
                    <button onclick="loadGame('xo')" class="bg-purple-600 hover:bg-purple-500 px-6 py-2 rounded-xl text-white font-bold transition shadow-lg border border-purple-400">
                        <i class="fas fa-times mr-2"></i> لعبة X O
                    </button>
                </div>

                <div class="relative w-full flex-1 bg-black/50 rounded-3xl overflow-hidden border border-yellow-500/20 shadow-2xl p-6 flex flex-col items-center justify-center min-h-[400px]" id="gameArea">
                    <div class="text-center text-gray-500">
                        <i class="fas fa-dice text-6xl mb-4 opacity-50"></i>
                        <h2 class="text-2xl font-bold">اختر لعبة لتبدأ التحدي</h2>
                    </div>
                </div>

            </div>

            <div class="w-full lg:w-96 bg-[#0f172a]/95 border-r border-yellow-500/10 flex flex-col">
                <div class="p-3 border-b border-white/5">
                    <p class="text-[10px] text-gray-500 font-bold mb-2">اللاعبون المتواجدون (<span id="realMemberCount">0</span>)</p>
                    <div id="membersList" class="flex flex-wrap gap-2"></div>
                </div>
                <div id="chatArea" class="flex-1 p-4 overflow-y-auto space-y-3 bg-black/20"></div>
                <div class="p-4 bg-black/40 border-t border-white/5">
                    <div class="flex items-center gap-2">
                        <input type="text" id="chatInput" onkeypress="if(event.key==='Enter') sendMessage()" placeholder="تحدث مع الفريق..." class="flex-1 bg-white/5 border border-white/10 p-3 rounded-xl text-xs text-white outline-none focus:border-yellow-500">
                        <button onclick="sendMessage()" class="w-10 h-10 bg-yellow-600/20 text-yellow-500 rounded-xl hover:bg-yellow-600 hover:text-white transition"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // --- تهيئة قاعدة البيانات المحلية ---
        const DB_KEY = 'ramadan_games_db';
        const SESSION_KEY = 'ramadan_games_session';
        let currentUser = null;

        function getUsersDB() { return JSON.parse(localStorage.getItem(DB_KEY)) || {}; }
        function saveUsersDB(db) { localStorage.setItem(DB_KEY, JSON.stringify(db)); }

        // --- إدارة تسجيل الدخول ---
        function toggleAuthMode(mode) {
            document.getElementById('loginForm').classList.toggle('hidden', mode === 'register');
            document.getElementById('registerForm').classList.toggle('hidden', mode === 'login');
        }

        function handleRegister() {
            const user = document.getElementById('regUser').value.trim();
            const pass = document.getElementById('regPass').value.trim();
            if (user.length < 3 || pass.length < 3) return Swal.fire('تنبيه', 'الاسم وكلمة المرور 3 أحرف على الأقل', 'warning');
            const db = getUsersDB();
            if (db[user]) return Swal.fire('خطأ', 'الاسم مستخدم مسبقاً', 'error');
            
            db[user] = { username: user, password: pass, gold: 100 };
            saveUsersDB(db);
            Swal.fire('تم', 'تم إنشاء الحساب، تفضل بالدخول', 'success');
            toggleAuthMode('login');
            document.getElementById('loginUser').value = user;
        }

        function handleLogin() {
            const user = document.getElementById('loginUser').value.trim();
            const pass = document.getElementById('loginPass').value.trim();
            const db = getUsersDB();
            if (db[user] && db[user].password === pass) {
                currentUser = db[user];
                localStorage.setItem(SESSION_KEY, user);
                initDashboard();
            } else {
                Swal.fire('خطأ', 'بيانات الدخول غير صحيحة', 'error');
            }
        }

        function checkSession() {
            const savedUser = localStorage.getItem(SESSION_KEY);
            const db = getUsersDB();
            if (savedUser && db[savedUser]) {
                currentUser = db[savedUser];
                initDashboard();
            } else {
                document.getElementById('authPage').classList.remove('hidden');
            }
            createStars();
        }

        function logout() {
            localStorage.removeItem(SESSION_KEY);
            location.reload();
        }

        function initDashboard() {
            document.getElementById('authPage').classList.add('hidden');
            document.getElementById('mainDashboard').classList.remove('hidden');
            document.getElementById('displayName').innerText = currentUser.username;
            document.getElementById('userGold').innerText = currentUser.gold;
        }

        function saveUserData() {
            const db = getUsersDB();
            db[currentUser.username] = currentUser;
            saveUsersDB(db);
            document.getElementById('userGold').innerText = currentUser.gold;
        }

        // --- نظام الغرف ---
        async function openCreateRoom() {
            const { value: name } = await Swal.fire({
                title: '🎲 إنشاء غرفة جديدة',
                input: 'text',
                inputPlaceholder: 'اسم الغرفة (مثال: تحدي السحور)',
                confirmButtonText: 'إنشاء',
                confirmButtonColor: '#d4af37'
            });
            if (name) {
                const container = document.getElementById('roomsContainer');
                container.innerHTML += `
                    <div onclick="enterRoom('${name}', '${currentUser.username}', true)" class="bg-white/5 p-6 rounded-[2rem] border border-white/5 hover:border-yellow-500/50 transition cursor-pointer group hover:bg-white/10">
                        <div class="flex justify-between items-start mb-4">
                            <div class="w-12 h-12 bg-yellow-900/30 rounded-2xl flex items-center justify-center text-yellow-400">
                                <i class="fas fa-crown text-xl"></i>
                            </div>
                        </div>
                        <h4 class="font-bold text-xl group-hover:text-yellow-400">${name}</h4>
                        <p class="text-xs text-gray-400 mt-1">المضيف: ${currentUser.username}</p>
                    </div>`;
            }
        }

        function enterRoom(name, owner, isOwner) {
            document.getElementById('mainDashboard').classList.add('hidden');
            document.getElementById('roomPage').classList.remove('hidden');
            document.getElementById('activeRoomName').innerText = name;
            document.getElementById('roomOwnerName').innerText = owner;
            addMemberToUI(currentUser.username);
            addSystemMsg(`انضم ${currentUser.username} إلى الغرفة`);
        }

        function exitRoom() { location.reload(); }

        // --- نظام الدردشة ---
        function sendMessage() {
            const inp = document.getElementById('chatInput');
            if(!inp.value.trim()) return;
            document.getElementById('chatArea').innerHTML += `
                <div class="mb-2 animate__animated animate__fadeInUp">
                    <span class="text-[10px] text-yellow-500 font-bold block">${currentUser.username}</span>
                    <div class="bg-white/10 p-2 rounded-xl rounded-tr-none text-sm inline-block text-white">${inp.value}</div>
                </div>`;
            inp.value = '';
            document.getElementById('chatArea').scrollTop = document.getElementById('chatArea').scrollHeight;
        }

        function addMemberToUI(name) {
            const list = document.getElementById('membersList');
            list.innerHTML += `<div class="bg-white/10 px-3 py-1 rounded-full text-xs text-white border border-white/20"><i class="fas fa-user text-yellow-500 mr-1"></i> ${name}</div>`;
            document.getElementById('realMemberCount').innerText = list.children.length;
        }

        function addSystemMsg(msg) {
            document.getElementById('chatArea').innerHTML += `<div class="text-[10px] text-center text-gray-400 my-2 bg-black/30 py-1 rounded-lg border border-white/5">${msg}</div>`;
        }

        // ==========================================
        //         منطق الألعاب (Games Logic)
        // ==========================================

        function loadGame(gameType) {
            const area = document.getElementById('gameArea');
            if(gameType === 'muheibes') {
                initMuheibes(area);
            } else if (gameType === 'xo') {
                initXO(area);
            }
        }

        // --- لعبة المحيبس الذكية ---
        let ringPosition = -1;
        
        function initMuheibes(area) {
            addSystemMsg('بدأت لعبة المحيبس! استعد..');
            area.innerHTML = `
                <div class="text-center w-full">
                    <h2 class="text-3xl font-bold text-yellow-400 mb-2 drop-shadow-md">بات! (محيبس)</h2>
                    <p class="text-gray-300 mb-6 text-sm">الفريق الثاني خفى المحبس.. اختار الإيد الصح!</p>
                    
                    <button onclick="hideRing()" class="btn-primary px-8 py-3 rounded-full mb-8 text-lg font-black animate-pulse">
                        <i class="fas fa-hand-sparkles"></i> بات (خبئ المحبس)
                    </button>
                    
                    <div id="handsContainer" class="flex flex-wrap justify-center gap-4 hidden">
                        </div>
                    <div id="muheibesResult" class="mt-6 text-xl font-bold h-8"></div>
                </div>
            `;
        }

        function hideRing() {
            document.getElementById('soundBat').play(); // تشغيل صوت بات
            const handsContainer = document.getElementById('handsContainer');
            handsContainer.classList.remove('hidden');
            handsContainer.innerHTML = '';
            document.getElementById('muheibesResult').innerHTML = '';
            
            // إنشاء 6 أيادي
            const numHands = 6;
            ringPosition = Math.floor(Math.random() * numHands); // وضع المحبس عشوائياً

            for(let i=0; i<numHands; i++) {
                handsContainer.innerHTML += `
                    <div onclick="guessRing(${i}, this)" class="hand-card w-24 h-32 flex flex-col items-center justify-center bg-gray-800 hover:bg-gray-700">
                        <i class="fas fa-hand-fist text-4xl text-yellow-600 mb-2"></i>
                        <span class="text-xs text-gray-400">إيد ${i+1}</span>
                    </div>
                `;
            }
            addSystemMsg('المحيبس اختفى! العب واختار إيد..');
        }

        function guessRing(guessedIndex, element) {
            if (ringPosition === -1) return; // اللعبة انتهت

            const allHands = document.getElementById('handsContainer').children;
            const res = document.getElementById('muheibesResult');

            if (guessedIndex === ringPosition) {
                // فوز
                document.getElementById('soundWin').play();
                element.innerHTML = `<i class="fas fa-ring text-5xl text-yellow-400 animate__animated animate__tada"></i>`;
                element.classList.add('border-green-500', 'bg-green-900/50');
                res.innerHTML = '<span class="text-green-400">كفووو! طلعت المحبس 💍 (+50 نقطة)</span>';
                currentUser.gold += 50;
                saveUserData();
                addSystemMsg(`🎉 ${currentUser.username} لقى المحبس وربح 50 نقطة!`);
            } else {
                // خسارة
                document.getElementById('soundLose').play();
                element.innerHTML = `<i class="fas fa-times text-4xl text-red-500"></i>`;
                element.classList.add('border-red-500', 'bg-red-900/50');
                res.innerHTML = '<span class="text-red-400">طاااح! الإيد فارغة ❌ (-10 نقاط)</span>';
                currentUser.gold -= 10;
                saveUserData();
                
                // كشف مكان المحبس الحقيقي
                allHands[ringPosition].innerHTML = `<i class="fas fa-ring text-5xl text-yellow-400 opacity-50"></i>`;
                allHands[ringPosition].classList.add('border-yellow-500');
                addSystemMsg(`❌ ${currentUser.username} ضيع المحبس!`);
            }
            ringPosition = -1; // إنهاء الجولة
        }


        // --- لعبة اكس او (Tic Tac Toe) ---
        let board = ["", "", "", "", "", "", "", "", ""];
        let currentPlayer = "X";
        let gameActive = true;

        function initXO(area) {
            board = ["", "", "", "", "", "", "", "", ""];
            currentPlayer = "X";
            gameActive = true;
            addSystemMsg('تم فتح طاولة X O');

            area.innerHTML = `
                <div class="text-center w-full max-w-sm mx-auto">
                    <h2 class="text-2xl font-bold text-white mb-2">لعبة إكس أو</h2>
                    <div class="text-yellow-400 mb-4" id="xoTurn">دور اللاعب: ${currentPlayer}</div>
                    
                    <div class="game-board grid grid-cols-3 w-max mx-auto bg-black/30 p-4 rounded-2xl" id="xoBoard">
                        ${board.map((_, i) => `<div class="xo-cell" onclick="xoPlay(${i})"></div>`).join('')}
                    </div>
                    
                    <button onclick="initXO(document.getElementById('gameArea'))" class="mt-6 text-sm text-gray-400 hover:text-white underline">إعادة اللعب</button>
                </div>
            `;
        }

        function xoPlay(index) {
            if (board[index] !== "" || !gameActive) return;

            board[index] = currentPlayer;
            const cells = document.querySelectorAll('.xo-cell');
            
            // تصميم X و O
            if(currentPlayer === 'X') {
                cells[index].innerHTML = '<i class="fas fa-times text-red-500 animate__animated animate__zoomIn"></i>';
            } else {
                cells[index].innerHTML = '<i class="far fa-circle text-blue-500 animate__animated animate__zoomIn"></i>';
            }

            checkXOWin();
        }

        function checkXOWin() {
            const winConditions = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8], // صفوف
                [0, 3, 6], [1, 4, 7], [2, 5, 8], // أعمدة
                [0, 4, 8], [2, 4, 6]             // أقطار
            ];

            let roundWon = false;
            for (let i = 0; i < winConditions.length; i++) {
                const [a, b, c] = winConditions[i];
                if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                    roundWon = true;
                    break;
                }
            }

            if (roundWon) {
                document.getElementById('xoTurn').innerHTML = `<span class="text-green-400 font-bold text-xl">فاز اللاعب ${currentPlayer}! 🎉</span>`;
                gameActive = false;
                addSystemMsg(`🎉 فاز ${currentPlayer} في لعبة X O`);
                if(currentPlayer === 'X') {
                    currentUser.gold += 20; // مكافأة
                    saveUserData();
                }
                return;
            }

            if (!board.includes("")) {
                document.getElementById('xoTurn').innerHTML = `<span class="text-gray-400 font-bold">تعادل! 🤝</span>`;
                gameActive = false;
                return;
            }

            // تبديل الأدوار
            currentPlayer = currentPlayer === "X" ? "O" : "X";
            document.getElementById('xoTurn').innerText = `دور اللاعب: ${currentPlayer}`;
            
            // محاكاة لعب الكمبيوتر إذا كان الدور لـ O
            if(currentPlayer === "O" && gameActive) {
                setTimeout(computerXOPlay, 500);
            }
        }

        function computerXOPlay() {
            let emptyIndices = board.map((val, idx) => val === "" ? idx : null).filter(val => val !== null);
            if(emptyIndices.length > 0) {
                let randomIdx = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
                xoPlay(randomIdx);
            }
        }

        // --- النجوم الخلفية ---
        function createStars() {
            const field = document.getElementById('starField');
            field.innerHTML = '';
            for (let i = 0; i < 150; i++) {
                const s = document.createElement('div');
                s.className = 'star';
                s.style.width = Math.random() * 2 + 'px';
                s.style.height = s.style.width;
                s.style.top = Math.random() * 100 + '%';
                s.style.left = Math.random() * 100 + '%';
                s.style.animationDelay = Math.random() * 2 + 's';
                field.appendChild(s);
            }
        }

        window.onload = checkSession;
    </script>
</body>
</html>
