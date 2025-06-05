function cambiarFoto(nuevaFoto) {
    const fotoActual = document.querySelector('.foto_perfil_img');
    fotoActual.src = nuevaFoto;

    const modalElement = document.getElementById('modalEditarFotoPerfil');
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}