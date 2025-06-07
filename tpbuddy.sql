CREATE DATABASE IF NOT EXISTS tpbuddy;

USE tpbuddy;

CREATE TABLE materias (
    materia_codigo VARCHAR(6) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    padron INT PRIMARY KEY,
    contrasena VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    carrera VARCHAR(50) NOT NULL,
    sobre_mi VARCHAR(1000),
    avatar_url VARCHAR(255),
    banner_color VARCHAR(7) DEFAULT '#A0B4B7'
);

CREATE TABLE materias_usuarios (
    padron INT,
    tiene_grupo BOOLEAN,
    materia_codigo VARCHAR(6),
    PRIMARY KEY (padron, materia_codigo),
    FOREIGN KEY (padron) REFERENCES usuarios(padron) ON DELETE CASCADE,
    FOREIGN KEY (materia_codigo) REFERENCES materias(materia_codigo) ON DELETE CASCADE
);

CREATE TABLE horarios_usuarios (
    padron INT,
    dia ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    turno ENUM('mañana', 'tarde', 'noche') NOT NULL,
    PRIMARY KEY (padron, dia, turno),
    FOREIGN KEY (padron) REFERENCES usuarios(padron) ON DELETE CASCADE
);

CREATE TABLE grupos (
    grupo_id INT AUTO_INCREMENT PRIMARY KEY,
    materia_codigo VARCHAR(6) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    tp_terminado BOOLEAN DEFAULT FALSE,
    maximo_integrantes INT NOT NULL,
    UNIQUE (materia_codigo, nombre),
    FOREIGN KEY (materia_codigo) REFERENCES materias(materia_codigo) ON DELETE CASCADE
);

CREATE TABLE grupos_usuarios
(
    grupo_id       INT,
    padron         INT,
    materia_codigo VARCHAR(6),
    PRIMARY KEY (grupo_id, padron),
    UNIQUE (padron, materia_codigo),
    FOREIGN KEY (grupo_id) REFERENCES grupos (grupo_id) ON DELETE CASCADE,
    FOREIGN KEY (padron) REFERENCES usuarios (padron) ON DELETE CASCADE,
    FOREIGN KEY (materia_codigo) REFERENCES materias (materia_codigo) ON DELETE CASCADE
);

CREATE TABLE horarios_grupos (
    grupo_id INT,
    dia ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    turno ENUM('mañana', 'tarde', 'noche') NOT NULL,
    PRIMARY KEY (grupo_id, dia, turno),
    FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id) ON DELETE CASCADE
);

CREATE TABLE solicitudes_grupos (
    solicitud_id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    padron INT NOT NULL,
    estado ENUM('pendiente', 'aceptada', 'rechazada') DEFAULT 'pendiente',
    FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id) ON DELETE CASCADE,
    FOREIGN KEY (padron) REFERENCES usuarios(padron) ON DELETE CASCADE
);

INSERT INTO materias (materia_codigo, nombre) VALUES
('TB022', 'Introducción al Desarrollo de Software'),
('CB001', 'Análisis Matemático II'),
('TB021', 'Fundamentos de Programación');