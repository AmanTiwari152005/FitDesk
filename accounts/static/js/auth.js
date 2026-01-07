// ---------------- AUTH GUARD ----------------
const PUBLIC_PAGES = [
    "/api/accounts/login-page/",
    "/api/accounts/register-page/",
    "/api/accounts/forgot-password-page/",
    "/api/accounts/reset-password-page/",
    "/api/accounts/verify-otp-page/"
];

const currentPath = window.location.pathname;
const isPublicPage = PUBLIC_PAGES.some(page => currentPath.startsWith(page));

if (!isPublicPage) {
    if (!localStorage.getItem("token")) {
        window.location.href = "/api/accounts/login-page/";
    }
}

/* ✅ CSRF TOKEN (ADDED – REQUIRED FOR PRODUCTION) */
const csrfTokenInput = document.getElementById("csrf-token");
const CSRF_TOKEN = csrfTokenInput ? csrfTokenInput.value : "";


// ---------------- LOGIN ----------------
function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    fetch("/api/accounts/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Login failed");
            return;
        }

        localStorage.setItem("token", data.token);

        fetch("/api/gym/check/", {
            headers: { "Authorization": "Token " + data.token }
        })
        .then(res => res.json())
        .then(result => {
            if (result.gym_exists) {
                window.location.href = "/dashboard/";
            } else {
                window.location.href = "/api/gym/setup/";
            }
        });
    })
    .catch(() => alert("Login error"));
}


// ---------------- REGISTER ----------------
function register() {
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    fetch("/api/accounts/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Registration failed");
            return;
        }

        // ✅ STORE EMAIL FOR OTP VERIFICATION
        localStorage.setItem("otp_email", email);

        alert("OTP sent to your email");

        // ✅ REDIRECT TO VERIFY OTP PAGE
        window.location.href = "/api/accounts/verify-otp-page/";
    })
    .catch(() => alert("Registration error"));
}


// ---------------- VERIFY OTP ----------------
function verifyOTP() {
    const otp = document.getElementById("otp").value;
    const email = localStorage.getItem("otp_email");

    if (!email) {
        alert("Session expired. Please register again.");
        window.location.href = "/api/accounts/register-page/";
        return;
    }

    fetch("/api/accounts/verify-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ email, otp })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Invalid OTP");
            return;
        }

        // ✅ OTP VERIFIED
        alert("OTP verified successfully");

        // cleanup
        localStorage.removeItem("otp_email");

        // ✅ REDIRECT TO LOGIN PAGE
        window.location.href = "/api/accounts/login-page/";
    })
    .catch(() => alert("OTP verification error"));
}


// -------- FORGOT PASSWORD --------
function forgotPassword() {
    const identifier = document.getElementById("fp-identifier").value;

    fetch("/api/accounts/forgot-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ identifier })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("User not found");
            return;
        }
        window.location.href = "/api/accounts/reset-password-page/";
    });
}


// -------- RESET PASSWORD --------
function resetPassword() {
    const password = document.getElementById("new-password").value;

    fetch("/api/accounts/reset-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Error resetting password");
            return;
        }
        alert("Password updated successfully");
        window.location.href = "/api/accounts/login-page/";
    });
}
