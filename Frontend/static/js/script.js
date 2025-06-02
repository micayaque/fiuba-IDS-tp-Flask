document.addEventListener("DOMContentLoaded", function () {


    //script para modals
    const modalCerrarSesion = document.getElementById("modal_cerrar_sesion");
    const botonCerrarModal = document.getElementById("close_modal");

    botonCerrarModal.addEventListener("click", function() {
        modalCerrarSesion.style.display = "none";
        modalEditarPerfil.style.display = "none";
        modalMateriasCursando.style.display = "none";
        modalMateriasAprobadas.style.display = "none";
        modalHorariosDisponibles.style.display = "none";
    });


    //modal editarfoto de perfil
    const modalEditarPerfil = document.getElementById("modal_editar_perfil");
    const botonEDITARMiPerfil = document.getElementById("boton_editar_foto_de_perfil");

    botonEDITARMiPerfil.addEventListener("click", function() {
        modalEditarPerfil.style.display = "flex";
    });

    //modal materias cursando

    const modalMateriasCursando = document.getElementById("modal_materias_cursando");
    const botonMateriasCursando = document.getElementById("boton_editar_materias_cursando");

    botonMateriasCursando.addEventListener("click", function() {
    modalMateriasCursando.style.display = "flex";
    });

    //modal materias aprobadas

    const modalMateriasAprobadas = document.getElementById("modal_materias_Aprobadas");
    const botonMateriasAprobadas = document.getElementById("boton_editar_materias_Aprobadas");

    botonMateriasAprobadas.addEventListener("click", function() {
    modalMateriasAprobadas.style.display = "flex";
    });

    //modal horarios disponibles
    const modalHorariosDisponibles = document.getElementById("modal_horarios_disponibles");
    const botonHorariosDisponibles = document.getElementById("boton_editar_horarios_disponibles");

    botonHorariosDisponibles.addEventListener("click", function() {
    modalHorariosDisponibles.style.display = "flex";
    });



    // Universal close for all modals
    document.querySelectorAll('.close_modal').forEach(btn => {
        btn.addEventListener('click', function() {
            // Cierra solo el modal al que pertenece el botón
            this.closest('.desplegable').style.display = 'none';
        });
    });

});