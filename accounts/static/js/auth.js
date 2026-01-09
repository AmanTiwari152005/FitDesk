/* CSRF TOKEN */
const csrfTokenInput = document.getElementById("csrf-token");
const CSRF_TOKEN = csrfTokenInput ? csrfTokenInput.value : "";

// ---------------- LOGIN ----------------
function loginUser() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    fetch("https://fitdesk.onrender.com/api/accounts/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        credentials: "include",
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Invalid credentials");
            return;
        }
        window.location.href = "/dashboard/";
    });
}


// ---------------- REGISTER ----------------
function registerUser() {
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    fetch("https://fitdesk.onrender.com/api/accounts/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        credentials: "include",
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Registration failed");
            return;
        }
        localStorage.setItem("otp_email", email);
        window.location.href = "/api/accounts/verify-otp-page/";
    });
}


// ---------------- VERIFY OTP ----------------
function verifyOTP() {
    const otp = document.getElementById("otp").value;
    const email = localStorage.getItem("otp_email");

    fetch("https://fitdesk.onrender.com/api/accounts/verify-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        credentials: "include",
        body: JSON.stringify({ email, otp })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Invalid OTP");
            return;
        }
        localStorage.removeItem("otp_email");
        window.location.href = "/api/accounts/login-page/";
    });
}
