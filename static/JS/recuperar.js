document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("formCorreo");
    const codigoContainer = document.getElementById("codigoContainer");
    const inputs = document.querySelectorAll(".code-box");
    const btn = document.getElementById("verificarCodigo");
    const instrucciones = document.getElementById("instrucciones")
    btn.classList.add("btn", "btn-primary", "mt-3", "px-4");

    // =========================
    // 1. Enviar correo (AJAX)
    // =========================
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                form.style.display = "none";
                instrucciones.style.display = "none";
                codigoContainer.style.display = "block";
            } else {
                alert(data.error || "Error");
            }
        });
    });

    // =========================
    // 2. Auto mover entre inputs
    // =========================
    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && input.value === "" && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    // =========================
    // 3. Verificar código (placeholder)
    // =========================
    document.getElementById("verificarCodigo").addEventListener("click", function () {
        let codigo = "";
        inputs.forEach(i => codigo += i.value);

    });

});

document.getElementById("verificarCodigo").addEventListener("click", function () {

    let codigo = "";
    document.querySelectorAll(".code-box").forEach(i => codigo += i.value);

    const correo = document.getElementById("correo").value;

    const formData = new FormData();
    formData.append("correo", correo);
    formData.append("codigo", codigo);

    fetch("/verificar-codigo/", {
        method: "POST",
        body: formData,
        headers: {
             "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.ok) {

            // aquí luego rediriges a reset password
            window.location.href = "/resetPassword";

        } else {
            alert(data.error);
        }
    });
});

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie('csrftoken');