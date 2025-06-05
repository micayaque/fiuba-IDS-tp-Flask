// cambiar foto de perfil
function cambiarFoto(nuevaFoto) {
    const fotoActual = document.querySelector('.foto_perfil_img');
    fotoActual.src = nuevaFoto;

    const modalElement = document.getElementById('modalEditarFotoPerfil');
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}

// cambiar el color del banner
function abrirSelectorColor() {
    document.getElementById('color_selector_banner').click();
}

function cambiarColorBanner(nuevoColor) {
    document.getElementById('banner_perfil').style.backgroundColor = nuevoColor;
}

