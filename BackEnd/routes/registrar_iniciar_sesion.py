from flask import Blueprint, request, redirect, flash, url_for, session  
from db import get_connection

registrar_iniciar_sesion_bp = Blueprint("registrar_iniciar_sesion", __name__)

@registrar_iniciar_sesion_bp.route('/registrarse', methods=['POST'])
def registrarse():

    data = request.get_json()
    padron = data['padron']
    password = data['password']
    nombre = data['nombre']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE padron = %s", (padron,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return "El usuario ya existe", 400

    cursor.execute(
        "INSERT INTO usuarios (padron, contrasena, nombre) VALUES (%s, %s, %s)",
        (padron, password, nombre)
    )

    conn.commit()

    cursor.close()
    conn.close()
    return "Usuario registrado correctamente", 200


@registrar_iniciar_sesion_bp.route('/iniciar-sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    padron = data['padron']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE padron = %s AND contrasena = %s", (padron, password)
    )
    
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return "Inicio de sesión exitoso", 200
    else:
        return "Padron o contraseña incorrectos", 400

@registrar_iniciar_sesion_bp.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('inicio'))