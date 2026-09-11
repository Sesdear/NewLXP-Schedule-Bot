const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
}

const checkbox = document.getElementById('acceptCheckbox');
const submitBtn = document.getElementById('submitBtn');

// Разблокировка кнопки при клике на чекбокс
checkbox.addEventListener('change', () => {
    submitBtn.disabled = !checkbox.checked;
});

// Отправка формы
document.getElementById('termsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!checkbox.checked) return;

    try {
        const response = await fetch('/api/accept-terms', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                accepted: true,
                initData: tg?.initData
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            if (tg) {
                tg.showAlert("Соглашение принято!");
                tg.close();
            } else {
                alert("Соглашение принято!");
            }
        } else {
            alert(data.message || "Ошибка отправки");
        }
    } catch (err) {
        console.error(err);
        alert("Ошибка соединения с сервером");
    }
});