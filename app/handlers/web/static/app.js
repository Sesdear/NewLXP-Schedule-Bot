const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
}

const togglePasswordBtn = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

togglePasswordBtn.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email, 
                password,
                initData: tg?.initData
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {

            if (tg) {
                tg.showAlert("Успешный вход!");
                tg.close();
            } else {
                alert("Успешный вход!");
            }
        } else {
            alert(data.message || "Ошибка входа");
        }
    } catch (err) {
        console.error(err);
        alert("Ошибка соединения с сервером");
    }
});