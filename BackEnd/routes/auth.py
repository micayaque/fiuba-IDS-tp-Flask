from flask import Blueprint, request, redirect, render_template
from flask import flash, url_for
from flask import session  

import mysql.connector
from BackEnd.config import MYSQL_CONFIG

auth_bp = Blueprint("auth", __name__)

def get_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

@auth_bp.route('/registrarse', methods=['POST'])
def registrarse():
    padron = request.form['padron']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    conn = get_db()
    cursor = conn.cursor()

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









@auth_bp.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        padron = request.form['padron']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE padron = %s AND contrasena = %s", (padron, password))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            # Inicio de sesión exitoso
            return redirect('/')  # o a donde quieras enviarlo
        else:
            return "Padron o contraseña incorrectos", 401  # Error simple por ahora

    # Si solo se accede por GET, mostrar el formulario de login (si lo tenés)
    return render_template('login.html')  # o lo que uses
