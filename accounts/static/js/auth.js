// ================= LOGIN =================
function login() {
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value.trim();

    fetch("/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Login failed");
            return;
        }

        localStorage.setItem("token", data.token);

        fetch("/api/gym/check/", {
            headers: { "Authorization": "Bearer " + data.token }
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
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value.trim();

    fetch("/api/accounts/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Registration failed");
            return;
        }

        alert("Account created successfully. Please login.");
        window.location.href = "/api/accounts/login-page/";
    });
}

// ================= FORGOT PASSWORD =================
function forgotPassword() {
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
            alert(data.message || "Unable to continue");
            return;
        }

        window.location.href = "/api/accounts/reset-password-page/?identifier=" + encodeURIComponent(identifier);
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong");
    });
}
// ================= RESET PASSWORD =================
function resetPassword() {
    const identifierInput = document.getElementById("reset-identifier");
    const identifier = identifierInput ? identifierInput.value.trim() : "";
    const password = document.getElementById("new-password").value.trim();
    const confirm = document.getElementById("confirm-password").value.trim();

    if (identifierInput && !identifier) {
        alert("Please enter email or username");
        return;
    }

    if (!password || !confirm) {
        alert("Please fill all password fields");
        return;
    }

    if (password !== confirm) {
        alert("Passwords do not match");
        return;
    }

    fetch("/api/accounts/reset-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            identifier,
            password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert(data.message || "Password reset failed");
            return;
        }

        alert("Password changed successfully. Please login again.");
        localStorage.clear();
        window.location.href = "/api/accounts/login-page/";
    })
    .catch(err => {
        console.error(err);
        alert("Reset password error");
    });
}
