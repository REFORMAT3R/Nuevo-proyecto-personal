const form = document.querySelector(".login-box");
const userInput = document.getElementById("user");
const passInput = document.getElementById("pass");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const user = userInput.value.trim();
    const pass = passInput.value.trim();

    if (!user) {
        alert("Ingresa tu usuario o correo");
        return;
    }

    if (!pass) {
        alert("Ingresa tu contraseña"); 
        return;
    }

    if (pass.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres");
        return;
    }

    fetch("/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
        body: JSON.stringify({
            usuario: user,
            contrasena: pass
        })
    })
    .then(res => {
        if (res.ok) {
            window.location.href = "/proximos";
        } else {
            alert("Usuario o contraseña incorrectos");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error al conectar con el servidor");
    });
});