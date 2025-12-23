const form = document.getElementById("registerForm");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nombres = document.getElementById("nombres").value.trim();
    const apellidos = document.getElementById("apellidos").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const nacimiento = document.getElementById("fecha").value;
    const genero = document.getElementById("genero").value;
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("password").value.trim();

    // Validaciones básicas
    if (!nombres || !apellidos || !correo || !nacimiento || !genero || !usuario || !contrasena) {
        alert("Completa todos los campos");
        return;
    }

    if (usuario.length < 4) {
        alert("El usuario debe tener al menos 4 caracteres");
        return;
    }

    if (contrasena.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres");
        return;
    }

    const fechaNac = new Date(nacimiento);
    const hoy = new Date();
    const edad = hoy.getFullYear() - fechaNac.getFullYear();
    if (edad < 13) {
        alert("Debes tener al menos 13 años");
        return;
    }

    // Enviar datos a Flask
    fetch("/api/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombres,
            apellidos,
            correo,
            nacimiento,
            genero,
            usuario,
            contrasena
        })
    })
    .then(res => {
        if (res.ok) {
            alert("Cuenta creada correctamente");
            window.location.href = "/";  
        } else if (res.status === 409) {
            alert("El usuario o correo ya existe");
        } else {
            alert("Error al registrar");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error al conectar con el servidor");
    });
});
