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
