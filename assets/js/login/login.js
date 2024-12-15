let captcha;
let notifications = document.querySelector('.notifications_nofit');

function InputUser(event) {
    event.target.value = event.target.value.replace(/[^0-9]/g, '');
}

// Convert Persian/Arabic numbers to English numbers
function convertToEnglishNumbers(str) {
    const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    const englishNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    
    let result = str.toString();
    
    for(let i = 0; i < 10; i++) {
        result = result.replaceAll(persianNumbers[i], englishNumbers[i])
                      .replaceAll(arabicNumbers[i], englishNumbers[i]);
    }
    
    return result;
}

function generateCaptcha() {
    const canvas = document.getElementById('captchaCanvas');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Set background
    ctx.fillStyle = '#f2f2f2';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Generate captcha text (only numbers for simplicity)
    const digits = '0123456789';
    const captchaLength = 5;
    const captchaText = Array.from(
        { length: captchaLength }, 
        () => digits.charAt(Math.floor(Math.random() * digits.length))
    ).join('');

    // Store captcha
    captcha = captchaText;

    // Draw text
    ctx.font = 'bold 30px Arial';
    ctx.fillStyle = '#333';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Add some rotation to each character
    const chars = captchaText.split('');
    chars.forEach((char, i) => {
        const x = (canvas.width / (captchaLength + 1)) * (i + 1);
        const y = canvas.height / 2;
        const rotation = (Math.random() - 0.5) * 0.4;
        
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);
        ctx.fillText(char, 0, 0);
        ctx.restore();
    });

    // Add noise
    for (let i = 0; i < 50; i++) {
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

async function Send(event) {
    event.preventDefault();
    
    // Convert input to English numbers and compare
    const userInput = convertToEnglishNumbers(document.getElementById("captchaInput").value);
    
    if (userInput === captcha) {
        // Get form values
        const nationalCode = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        
        try {
            const response = await login(nationalCode, password);
            
            if (response.success) {
                let type = 'success';
                let title = 'خوش آمدید';
                let text = 'با موفقیت وارد شدید';
                createToast(type, title, text);
                
                // Redirect after successful login
                setTimeout(() => {
                    window.location.href = '/dashboard/';
                }, 1000);
            } else {
                let type = 'error';
                let title = 'خطا';
                let text = response.error || 'خطا در ورود';
                createToast(type, title, text);
                ReloadCaptcha();
            }
        } catch (error) {
            let type = 'error';
            let title = 'خطا';
            let text;
            
            // Check error response and set appropriate message
            if (error.response) {
                switch (error.response.status) {
                    case 404:
                        text = 'کاربر یافت نشد';
                        break;
                    case 401:
                        text = 'رمز عبور اشتباه است';
                        break;
                    case 400:
                        text = 'لطفا تمام فیلدها را پر کنید';
                        break;
                    default:
                        text = error.response.data?.error || 'خطا در ورود';
                }
            } else {
                text = 'خطا در ارتباط با سرور';
            }
            
            createToast(type, title, text);
            console.error('Error:', error);
            ReloadCaptcha();
        }
    } else {
        let type = 'error';
        let title = 'اخطار';
        let text = 'کد امنیتی را به درستی وارد کنید';
        createToast(type, title, text);
        ReloadCaptcha();
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

// First get CSRF token
async function getCsrfToken() {
    const response = await fetch('/api/csrf/');
    const data = await response.json();
    return data.csrfToken;
}

// Login function
async function login(national_code, password, user_type = 'student') {
    try {
        const csrfToken = await getCsrfToken();
        
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
            body: JSON.stringify({
                national_code: national_code,
                password: password,
                user_type: user_type
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            const error = new Error(data.error || 'Login failed');
            error.response = response;
            throw error;
        }
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Usage example
login('1234567890', 'password123', 'student')
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


