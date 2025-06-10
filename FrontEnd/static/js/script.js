// Popup para el contacto en el menú 

function mostrarPopupContacto() {
    document.getElementById("contenedor_contacto_popup").style.display = "flex";
    document.getElementById("fondo_popup_contacto").style.display = "block";
}

function cerrarPopupContacto() {
    document.getElementById("contenedor_contacto_popup").style.display = "none";
    document.getElementById("fondo_popup_contacto").style.display = "none";
}

// Filtrar las materias 

function filtrarMaterias() {
    console.log("filtrarMaterias ejecutada");

  const input = document.getElementById('buscadorInput').value.toLowerCase();
  
  const materias = document.getElementsByClassName('materia-item');
  for (let i = 0; i < materias.length; i++) {
    // querySelector busca el elemento con clase 'materia-nombre' dentro del div actual (materias[i] es el div con clase 'materia-item' encontrado antes)
    const nombreElemento = materias[i].querySelector('.materia-nombre').textContent.toLowerCase();
    
    materias[i].style.display = nombreElemento.startsWith(input) ? '' : 'none';
  }
}

// Formulario de Registro

function togglePasswordVisibility() {
      const input = document.getElementById('register-password');
      const icon = document.getElementById('togglePassword');
      
      if (input.type === "password") {
        input.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      } else {
        input.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
    }

// Formulario de Login

function toggleLoginPasswordVisibility() {
    const input = document.getElementById('login-password');
    const icon = document.getElementById('toggleLoginPassword');
    
    if (input.type === "password") {
      input.type = "text";
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      input.type = "password";
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  }


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