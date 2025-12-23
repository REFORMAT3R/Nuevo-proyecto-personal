const form = document.querySelector(".login-box");
const userInput = document.getElementById("user");
const passInput = document.getElementById("pass");

form.addEventListener("submit", function (e) {
    e.preventDefault(); // evita envío automático

    const user = userInput.value.trim();
    const pass = passInput.value.trim();


    if (user === "") {
        alert("El usuario no puede estar vacío");
        userInput.focus();
        return;
    }

    if (pass === "") {
        alert("La contraseña no puede estar vacía");
        passInput.focus();
        return;
    }

    if (user.length < 3) {
        alert("El usuario debe tener al menos 3 caracteres");
        userInput.focus();
        return;
    }

    if (pass.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres");
        passInput.focus();
        return;
    }

    // ===== VALIDAR CON FLASK + MYSQL =====
    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user: user,        // puede ser usuario O correo
            password: pass
        })
    })
    .then(res => {
        if (res.ok) {
            // TODO BIEN → REDIRIGE
            window.location.href = "../Proximos.html";
        } else {
            // CREDENCIALES INCORRECTAS
            alert("Usuario o contraseña incorrectos");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error al conectar con el servidor");
    });
});
