from flask import Blueprint, request, redirect, render_template, flash, url_for, session  

# otra consulta: ¿por que no funciona el import directo desde db (de BackEnd) "from db import get_connection" si antes para mostrar las materias de la base de datos si funcionaba?
from .db import get_connection

registrar_iniciar_sesion_bp = Blueprint("registrar_iniciar_sesion", __name__)

@registrar_iniciar_sesion_bp.route('/registrarse', methods=['POST'])
def registrarse():
    padron = request.form['padron']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "INSERT INTO usuarios (padron, contrasena, nombre, apellido) VALUES (%s, %s, %s, %s)",
            (padron, password, nombre, apellido)
        )
        conn.commit()
    except Exception as e:
        return f"Error: {e}"  # Mostrará el error crudo, como el de 'padron ya existe'
    finally:
        cursor.close()
        conn.close()

    return redirect('/')  # Si el registro es exitoso, va al home


@registrar_iniciar_sesion_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    padron = request.form['padron']
    password = request.form['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE padron = %s AND contrasena = %s", (padron, password))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        session['usuario'] = usuario['padron']
        return redirect('/')
    else:
        return "Padron o contraseña incorrectos", 401  # Error simple por ahora