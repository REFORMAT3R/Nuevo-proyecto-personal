const form = document.getElementById("registerForm");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nombres = document.getElementById("nombres").value.trim();
    const apellidos = document.getElementById("apellidos").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const fecha = document.getElementById("fecha").value;
    const genero = document.getElementById("genero").value;
    const usuario = document.getElementById("usuario").value.trim();
    const password = document.getElementById("password").value.trim();

    // ===== VALIDACIONES (NO SE TOCAN) =====
    if (!nombres || !apellidos || !correo || !fecha || !genero || !usuario || !password) {
        alert("Completa todos los campos");
        return;
    }

    if (usuario.length < 4) {
        alert("El usuario debe tener al menos 4 caracteres");
        return;
    }

    if (password.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres");
        return;
    }

    const nacimiento = new Date(fecha);
    const hoy = new Date();
    const edad = hoy.getFullYear() - nacimiento.getFullYear();

    if (edad < 13) {
        alert("Debes tener al menos 13 años");
        return;
    }

    // ===== INSERT EN MYSQL (FLASK) =====
    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombres: nombres,
            apellidos: apellidos,
            correo: correo,
            fecha: fecha,
            genero: genero,
            usuario: usuario,
            password: password
        })
    })
    .then(res => {
        if (res.ok) {
            alert("Cuenta creada correctamente");
            window.location.href = "login.html";
        } else {
            alert("El usuario o correo ya existe");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error al conectar con el servidor");
    });
});
