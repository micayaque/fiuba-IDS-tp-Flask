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


// agregar grupo en el perfil del usuario
let integrantes = [];

function actualizarListaIntegrantes() {
    const lista = document.getElementById('listaIntegrantes');
    lista.innerHTML = '';
    integrantes.forEach((padron, indice) => {
        const div = document.createElement('div');
        div.className = 'btn btn-outline-light d-flex align-items-center gap-2';
        div.innerHTML = `
            <span>${padron}</span>
            <button type="button" class="btn btn-sm" onclick="eliminarIntegrante(${indice})">
                <img src="/static/img/iconos/cerrar.png" alt="Eliminar integrante" width="16" height="16">
            </button>
        `;
        lista.appendChild(div); // mostramos al integrante
    });
    document.getElementById('padronesIntegrantesInput').value = integrantes.join(','); // agregamos el integrante al input para que lo envíe al back separando a cada uno con comas
}

function eliminarIntegrante(indice) {
    integrantes.splice(indice, 1);
    actualizarListaIntegrantes();
}

function agregarIntegrante() {
    const input = document.getElementById('padronIntegrante');
    const padron = input.value.trim();
    if (padron && !integrantes.includes(padron)) {
        integrantes.push(padron);
        actualizarListaIntegrantes();
        input.value = '';
    }
}

function cambiarDatalistPadrones() {
    let codigo = document.getElementById('materiaGrupo').value;
    let inputPadron = document.getElementById('padronIntegrante');
    let datalistId = 'sugerenciasPadrones_' + codigo;
    if (document.getElementById(datalistId)) {
        inputPadron.setAttribute('list', datalistId);
    }
}






function filtrarPorHorarios(selectorCartas, selectorModal) {
    const horariosSeleccionados = [];
    ['mañana', 'tarde', 'noche'].forEach(turno => {
        ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'].forEach(dia => {
            const checkbox = document.querySelector(`${selectorModal} input[name="${dia}_${turno}"]`);
            if (checkbox.checked) {
                horariosSeleccionados.push({dia: dia, turno: turno});
            }
        });
    });

    document.querySelectorAll(selectorCartas).forEach(carta => {
        const horarios = JSON.parse(carta.getAttribute('data-horarios') || "[]");
        if (horariosSeleccionados.length === 0) {
            carta.style.display = '';
            return;
        }
        const coincide = horarios.some(h => horariosSeleccionados.some(sel => h.dia === sel.dia && h.turno === sel.turno)
        );
        carta.style.display = coincide ? '' : 'none';
    });

    const modalElement = document.querySelector(selectorModal);
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) modalInstance.hide();
}




// editar grupo en el perfil del usuario
function actualizarIntegrantesEditar() {
    const lista = document.getElementById('editarListaIntegrantes');
    lista.innerHTML = '';
    integrantesEditar.forEach((padron, indice) => {
        const div = document.createElement('div');
        div.className = "btn btn-outline-light d-flex align-items-center gap-2";
        div.innerHTML = `${padron} <button type="button" class="btn btn-sm" onclick="eliminarIntegranteEditar(${indice})"><img src="/static/img/iconos/cerrar.png" alt="Eliminar integrante" width="16" height="16"></button>`;
        lista.appendChild(div);
    });
    document.getElementById('editarPadronesIntegrantesInput').value = integrantesEditar.join(',');
}

function agregarIntegranteEditar() {
    const input = document.getElementById('editarPadronIntegrante');
    const padron = input.value.trim();
    if (padron && !integrantesEditar.includes(padron)) {
        integrantesEditar.push(padron);
        actualizarIntegrantesEditar();
        input.value = '';
    }
}

function eliminarIntegranteEditar(indice) {
    integrantesEditar.splice(indice, 1);
    actualizarIntegrantesEditar();
}


function abrirModalEditarGrupo(btn) {
    const grupoId = btn.getAttribute('data-grupo-id');
    const nombre = btn.getAttribute('data-nombre');
    const max = btn.getAttribute('data-maximo-integrantes');
    const lista_integrantes = JSON.parse(btn.getAttribute('data-integrantes'));
    const integrantes = lista_integrantes.map(i => i.padron);

    integrantesEditar = integrantes.slice();
    actualizarIntegrantesEditar();

    document.getElementById('formEditarGrupo').action = `/grupos/${grupoId}/editar`;
    document.getElementById('editarNombreGrupo').value = nombre;
    document.getElementById('editarCantidadMaxIntegrantes').value = max;

    const horarios = JSON.parse(btn.getAttribute('data-horarios'));
    for (const dia of ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']) {
        for (const turno of ['mañana', 'tarde', 'noche']) {
            const cb = document.getElementById(`editarGrupoHorario_${dia}_${turno}`);
            if (cb) cb.checked = horarios.includes(`${dia}-${turno}`);
            else cb.checked = false;
        }
    }
}