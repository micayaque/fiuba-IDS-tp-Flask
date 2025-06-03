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

    //mosal elegir foto de perfil
    const modalElegirFotoDePerfil = document.getElementById("modal_ejegir_foto_de_perfil");
    const botonElegirFotoDePerfil = document.getElementById("boton_elegir_foto_de_perfil");

    botonElegirFotoDePerfil.addEventListener("click", function() {
    modalElegirFotoDePerfil.style.display = "flex";
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

    //modal editar infromacion del grupo_1
    const modalEditarInfoGrupos = document.getElementById("modal_editar_informacion_de_grupo");
    const botonEditarInfoGrupos = document.getElementById("button_editar_informacion_grupo");

    botonEditarInfoGrupos.addEventListener("click", function() {
    modalEditarInfoGrupos.style.display = "flex";
    });

    //modal editar infromacion del grupo_2

    const modalEditarInfoGrupos2 = document.getElementById("modal_editar_informacion_de_grupo_2");
    const botonEditarInfoGrupos2 = document.getElementById("button_editar_informacion_grupo_2");

    botonEditarInfoGrupos2.addEventListener("click", function() {
    modalEditarInfoGrupos2.style.display = "flex";
    });

    //modal editar infromacion del grupo_3  
    const modalEditarInfoGrupos3 = document.getElementById("modal_editar_informacion_de_grupo_3");
    const botonEditarInfoGrupos3 = document.getElementById("button_editar_informacion_grupo_3");

    botonEditarInfoGrupos3.addEventListener("click", function() {
    modalEditarInfoGrupos3.style.display = "flex";
    });


    // Universal close for all modals
    document.querySelectorAll('.close_modal').forEach(btn => {
        btn.addEventListener('click', function() {
            // Cierra solo el modal al que pertenece el botón
            this.closest('.desplegable').style.display = 'none';
        });
    });
    // cambiar color del banner
    const iconoCamara = document.getElementById('img_cambiar_banner');
    const selectorColor = document.getElementById('color_selector_banner');
    const banner = document.getElementById('banner_perfil');

    if (iconoCamara && selectorColor && banner) {
        iconoCamara.addEventListener('click', function () {
            selectorColor.click();  // abrir selector
        });

        selectorColor.addEventListener('input', function () {
            banner.style.backgroundColor = selectorColor.value;  // aplicar color
        });
    }

    // cambiar imagen de perfil al hacer clic en "foto_perfil_rosa"
    const botonRosa = document.getElementById("foto_perfil_rosa");
    const imagenPerfil = document.querySelector("#boton_editar_foto_de_perfil .foto_perfil_img");

    if (botonRosa  && imagenPerfil) {
        botonRosa.addEventListener("click", function () {
            imagenPerfil.src = "/static/img/foto_de_perfil_rosa.png";
            modalElegirFotoDePerfil.style.display = "none";  
            modalEditarPerfil.style.display = "none";// cerrar modal
        });
    }

    const botonvioleta = document.getElementById("foto_perfil_violeta");
    const imagenPerfilv = document.querySelector("#boton_editar_foto_de_perfil .foto_perfil_img");

    if (botonvioleta  && imagenPerfil) {
        botonvioleta.addEventListener("click", function () {
            imagenPerfilv.src = "/static/img/foto_de_perfil_violeta.png";
            modalElegirFotoDePerfil.style.display = "none";  
            modalEditarPerfil.style.display = "none";// cerrar modal
        });
    }


});


