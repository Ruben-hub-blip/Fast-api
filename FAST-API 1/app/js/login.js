document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("loginForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        const usuario = document.getElementById("email").value;
        const contrasena = document.getElementById("password").value;

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    usuario: usuario,
                    contrasena: contrasena
                })
            });

            const data = await response.json();

            if(response.ok){
                document.getElementById("mensaje").innerHTML =
                    "<span class='text-success'>Login exitoso</span>";

                localStorage.setItem("token", data.access_token);

            } else {
                document.getElementById("mensaje").innerHTML =
                    "<span class='text-danger'>" + data.detail + "</span>";
            }

        } catch (error) {
            document.getElementById("mensaje").innerHTML =
                "<span class='text-danger'>Error de conexión con el servidor</span>";
        }

    });

});
