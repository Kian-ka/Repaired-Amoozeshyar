let captcha;
let notifications = document.querySelector('.notifications_nofit');

function InputUser(event) {
    event.target.value = event.target.value.replace(/[^0-9]/g, '');
}

function generateCaptcha() {
    const canvas = document.getElementById('captchaCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#f2f2f2';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    const captchaText = Array.from({ length: 5 }, () => chars.charAt(Math.floor(Math.random() * chars.length))).join('');
    sessionStorage.setItem('captcha', captchaText);

    ctx.font = '30px Arial';
    ctx.fillStyle = '#333';
    ctx.fillText(captchaText, 100, 30);
    captcha = captchaText;
    for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
        ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
        ctx.strokeStyle = '#ccc';
        ctx.stroke();
    }
}

window.onload = ReloadCaptcha;

function ReloadCaptcha() {
    generateCaptcha();
}


function Send(event) {
    event.preventDefault();
    if (document.getElementById("captchaInput").value.toLowerCase() == captcha.toLowerCase()) {
        // showAlert(0, "با موفقیت وارد شدید")
        let type = 'success';
        let title = 'خوش آمدید';
        let text = 'با موفقیت وارد شدید';
        createToast(type, title, text);
    } else {
        // showAlert(1, "کد کپچا را درست وارد کنید")
        let type = 'error';
        let title = 'اخطار';
        let text = 'کپچا را به درستی وارد کنید.';
        createToast(type, title, text);
    }
}


function showAlert(type, title) {
    const alertBox = type == 0 ? document.getElementById('customAlert-success') : document.getElementById('customAlert-danger');
    alertBox.textContent = title;

    alertBox.classList.add('alert-show');
    alertBox.classList.remove('alert-hide');


    setTimeout(() => {
        alertBox.classList.add('alert-hide');
        alertBox.classList.remove('alert-show');
    }, 3000); // 3 ثانیه
}

function createToast(type_nofit, title_nofit, text_nofit) {
    let newToast = document.createElement('div');
    newToast.innerHTML = `
        <div class="toast_nofit ${type_nofit}">
            <i></i>
            <div class="content_nofit">
                <div class="title_nofit">${title_nofit}</div>
                    <span>${text_nofit}</span>
                </div>
                <i ></i>
            </div>`;

    notifications.appendChild(newToast);
    newToast.timeOut = setTimeout(() => newToast.remove(), 5000)
}


