function mostrarPopupContacto() {
    document.getElementById("contenedor_contacto_popup").style.display = "flex";
    document.getElementById("fondo_popup_contacto").style.display = "block";
};

function cerrarPopupContacto() {
    document.getElementById("contenedor_contacto_popup").style.display = "none";
    document.getElementById("fondo_popup_contacto").style.display = "none";
};

function filtrarMaterias() {
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
    };

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
  };