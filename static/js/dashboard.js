(function(){
    let logoutButton = document.getElementById("logout-button");

    async function logout(event) {
        let response = await fetch("/api/logout", {
            method: "POST",
            redirect: "follow",
        });

        if (response.redirected) {
            window.location.href = response.url;
        }
    }

    logoutButton?.addEventListener("click", logout);
})();