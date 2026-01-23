// ================= LOGIN =================
alert("AUTH.JS LOADED");

function login() {
    console.log("LOGIN FUNCTION CALLED");

    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();

    fetch("/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        console.log("LOGIN RESPONSE:", data);

        if (!data.success) {
            alert(data.message || "Login failed");
            return;
        }

        localStorage.setItem("token", data.token);

        fetch("/api/gym/check/", {
            headers: { "Authorization": "Token " + data.token }
        })
        .then(res => res.json())
        .then(r => {
            window.location.href = r.gym_exists ? "/dashboard/" : "/api/gym/setup/";
        });
    })
    .catch(err => {
        console.error(err);
        alert("Login error");
    });
}

// ================= REGISTER =================
function register() {
    console.log("REGISTER FUNCTION CALLED");

    const username = document.getElementById("reg-username").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value.trim();

    fetch("/api/accounts/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Registration failed");
            return;
        }

        localStorage.setItem("otp_email", email);
        window.location.href = "/api/accounts/verify-otp-page/";
    });
}

// ================= VERIFY OTP =================
function verifyOTP() {
    const otp = document.getElementById("otp").value.trim();
    const email = localStorage.getItem("otp_email");

    fetch("/api/accounts/verify-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

// ================= FORGOT PASSWORD =================
function forgotPassword() {
    console.log("FORGOT PASSWORD FUNCTION CALLED");

    const identifier = document.getElementById("fp-identifier").value.trim();

    if (!identifier) {
        alert("Please enter username or email");
        return;
    }

    fetch("/api/accounts/forgot-password/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("User not found");
            return;
        }

        // ✅ move to reset password page
        window.location.href = "/api/accounts/reset-password-page/";
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong");
    });
}
// ================= RESET PASSWORD =================
function resetPassword() {
    console.log("RESET PASSWORD FUNCTION CALLED");

    const password = document.getElementById("new-password").value.trim();
    // const confirm = document.getElementById("confirm-password").value.trim();

    // if (!password || !confirm) {
    //     alert("Please fill all fields");
    //     return;
    // }

    // if (password !== confirm) {
    //     alert("Passwords do not match");
    //     return;
    // }

    fetch("/api/accounts/reset-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Password reset failed");
            return;
        }

        alert("Password reset successful. Please login.");
        window.location.href = "/api/accounts/login-page/";
    })
    .catch(err => {
        console.error(err);
        alert("Reset password error");
    });
}

