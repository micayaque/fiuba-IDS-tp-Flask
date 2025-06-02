function mostrarPopup_contacto() {
    document.getElementById("contacto_popup").style.display = "block";
    document.getElementById("fondo_popupContacto").style.display = "block";
};

function cerrarPopup_contacto() {
    document.getElementById("contacto_popup").style.display = "none";
    document.getElementById("fondo_popupContacto").style.display = "none";
};

let correoSeleccionado = '';

function seleccionar(correo) {
  correoSeleccionado = correo;

  // Actualiza la vista del boton seleccionado
  document.querySelectorAll('#lista_correos button').forEach(btn => btn.classList.remove('seleccionado'));
  const boton = Array.from(document.querySelectorAll('#lista_correos button')).find(b => b.textContent === correo);
  if (boton) boton.classList.add('seleccionado');

  console.log('Correo seleccionado:', correoSeleccionado);
};


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