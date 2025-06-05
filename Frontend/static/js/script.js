// cambiar foto de perfil
function cambiarFoto(nuevaFoto) {
    const fotoActual = document.querySelector('.foto_perfil_img');
    fotoActual.src = nuevaFoto;
    const modalElement = document.getElementById('modalEditarFotoPerfil');
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}

// cambiar el color del banner
function cambiarColorBanner(color) {
    document.getElementById('banner_perfil').style.backgroundColor = color;
}

// cambiar los datos del perfil del usuario
let campoActual = '';

function abrirEditorInfo(campo) {
    campoActual = campo;
    const titulo = document.getElementById('modalEditarCampoTitulo');
    const input = document.getElementById('inputEditarCampo');
    const elemento = document.getElementById(`${campo}_usuario`);

    titulo.textContent = 'Editar ' + campo.replace('_', ' ');
    input.value = campo === 'sobre_mi' ? elemento.value : elemento.textContent;
}

function guardarCampoEditado() {
    const input = document.getElementById('inputEditarCampo');
    const elemento = document.getElementById(`${campoActual}_usuario`);
    elemento.textContent = input.value;
    const modal = document.getElementById('modalEditarCampo');
    const modalInstance = bootstrap.Modal.getInstance(modal);
    modalInstance.hide();
}

// cambiar la descripción "Sobre mí"
function abrirEditorSobreMi() {
    const descripcionActual = document.getElementById('sobre_mi_usuario').value;
    document.getElementById('textareaEditarSobreMi').value = descripcionActual;
}

function guardarSobreMi() {
    const nuevaDescripcion = document.getElementById('textareaEditarSobreMi').value;
    document.getElementById('sobre_mi_usuario').value = nuevaDescripcion;
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalSobreMi'));
    modal.hide();
}