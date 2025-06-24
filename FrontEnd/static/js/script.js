function filtrarMaterias() {
    const input = document.getElementById('buscadorInput').value.toLowerCase();    
    const materias = document.getElementsByClassName('materia-item');

    for (let i = 0; i < materias.length; i++) {
        const nombreElemento = materias[i].querySelector('.materia-nombre').textContent.toLowerCase();
        materias[i].style.display = nombreElemento.includes(input) ? '' : 'none';
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


function cambiarDatalistPadronesParaElegir() {
    let materia_codigo = document.getElementById('materiaGrupo').value;
    let inputPadron = document.getElementById('padronIntegrante');
    let datalistId = 'sugerenciasPadrones_' + materia_codigo;
    if (document.getElementById(datalistId)) inputPadron.setAttribute('list', datalistId);
}


let integrantesAgregar = [];

function agregarIntegrante() {
    const input = document.getElementById('padronIntegrante');
    const padron = input.value.trim();
    if (padron && !integrantesAgregar.includes(padron)) {
        integrantesAgregar.push(padron);
        actualizarListaIntegrantesAgregar();
        input.value = '';
    }
}

function actualizarListaIntegrantesAgregar() {
    const lista = document.getElementById('listaIntegrantes');
    lista.innerHTML = '';
    integrantesAgregar.forEach((padron, indice) => {
        const div = document.createElement('div');
        div.className = 'btn btn-outline-light d-flex align-items-center gap-2';
        div.innerHTML = `
            <span>${padron}</span>
            <button type="button" class="btn btn-sm" onclick="eliminarIntegrante(${indice})">
                <img src="/static/img/iconos/cerrar.png" alt="Eliminar integrante" width="16" height="16">
            </button>
        `;
        lista.appendChild(div);
    });
    document.getElementById('padronesIntegrantesInput').value = integrantesAgregar.join(',');
}

function eliminarIntegrante(indice) {
    integrantesAgregar.splice(indice, 1);
    actualizarListaIntegrantesAgregar();
}


let integrantesEditar = [];

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


function abrirModalEditarGrupo(btn) {
    const grupoId = btn.getAttribute('data-grupo-id');
    const nombre = btn.getAttribute('data-nombre');
    const maxIntegrantes = btn.getAttribute('data-maximo-integrantes');
    const listaIntegrantes = JSON.parse(btn.getAttribute('data-integrantes'));
    const integrantes = listaIntegrantes.map(i => i.padron);

    integrantesEditar = [...integrantes];
    actualizarIntegrantesEditar();

    document.getElementById('formEditarGrupo').action = `/usuario/${grupoId}/editar-grupo`;
    document.getElementById('editarNombreGrupo').value = nombre;
    document.getElementById('editarCantidadMaxIntegrantes').value = maxIntegrantes;

    const horarios = JSON.parse(btn.getAttribute('data-horarios'));
    for (const dia of ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']) {
        for (const turno of ['mañana', 'tarde', 'noche']) {
            const cb = document.getElementById(`editarGrupoHorario_${dia}_${turno}`);
            if (cb) cb.checked = horarios.includes(`${dia}-${turno}`);
            else cb.checked = false;
        }
    }
}