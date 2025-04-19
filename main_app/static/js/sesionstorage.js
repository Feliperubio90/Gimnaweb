const nombre = sessionStorage.getItem('cliente_nombre');
if (nombre) {
    console.log("Cliente en sesión:", nombre);
    document.getElementById("saludo").innerText = `Bienvenido, ${nombre}`;
}
