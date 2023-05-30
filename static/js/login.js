(function() {
    let loginButton = document.getElementById("login-button");
    let loginForm = document.getElementById("login-form");

    let loginContainer = document.getElementById("login");
    let registerContainer = document.getElementById("register");

    document.getElementById("switch-to-register").addEventListener("click", function() {
        loginContainer.style.display = "none";
        registerContainer.style.display = "block";
    });

    document.getElementById("switch-to-login").addEventListener("click", function() {
        loginContainer.style.display = "block";
        registerContainer.style.display = "none";
    });

    async function login(event) {
        event.preventDefault();
        let formData = new FormData(loginForm);

        let response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "username": formData.get("username"),
                "password": formData.get("password"),
            }),
            redirect: "follow",
        })

        // in case follow didn't work
        if (response.redirected) {
            window.location.href = response.url;
        }
    }

    loginForm.onsubmit = login;

    loginButton.addEventListener("click", login)

    // register
    let registerButton = document.getElementById("register-button");
    let registerForm = document.getElementById("register-form");

    async function register(event) {
        event.preventDefault();
        let formData = new FormData(registerForm);

        let response = await fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": formData.get("email"),
                "username": formData.get("username"),
                "password": formData.get("password"),
            }),
        });

        let reply = await response.json();
        if(reply.status == "success") {
            document.getElementById("switch-to-login").click();
            boardcastMessage("User registered successfully", "success");
        } else {
            boardcastMessage(reply.message, "error");
        }
    }

    registerForm.onsubmit = register;

    registerButton.addEventListener("click", register)
})();