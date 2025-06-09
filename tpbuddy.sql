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
    carrera VARCHAR(50),
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
('CB001', 'Análisis Matemático II'),
('TB021', 'Fundamentos de Programación'),
('TB022', 'Introducción al Desarrollo de Software'),
('TB023', 'Álgebra Lineal'),
('TB024', 'Organización del Computador'),
('TB025', 'Algoritmos y Estructuras de Datos'),
('TB026', 'Probabilidad y Estadística'),
('TB027', 'Teoría de Algoritmos'),
('TB028', 'Sistemas Operativos'),
('TB029', 'Paradigmas de Programación'),
('TB030', 'Base de Datos'),
('TB031', 'Modelación Numérica'),
('TB032', 'Taller de Programación'),
('IS001', 'Ingeniería de Software I'),
('IS002', 'Ingeniería de Software II'),
('IS003', 'Diseño de Software'),
('IT001', 'Arquitectura de Computadoras'),
('IT002', 'Redes'),
('IT003', 'Programación Concurrente'),
('IT004', 'Sistemas Distribuidos I'),
('CS001', 'Matemática Discreta'),
('CS002', 'Teoría de la Computación'),
('IN001', 'Introducción a la Inteligencia Artificial'),
('DS001', 'Ciencia de Datos'),
('OP001', 'Criptografía I'),
('OP002', 'Lenguajes y Compiladores I'),
('OP003', 'Análisis Matemático III'),
('TR001', 'Taller de Proyecto Final');

INSERT INTO grupos (grupo_id, materia_codigo, nombre, tp_terminado, maximo_integrantes) VALUES
(1,'TR001', 'Locura', False, 4);