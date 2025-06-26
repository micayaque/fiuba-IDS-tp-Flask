CREATE DATABASE IF NOT EXISTS tpbuddy;

USE tpbuddy;

CREATE TABLE materias (
    codigo VARCHAR(6) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    padron INT PRIMARY KEY,
    contrasena VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    carrera VARCHAR(50) DEFAULT 'Contanos qué carrera estudiás',
    sobre_mi VARCHAR(1000) DEFAULT '',
    avatar_url VARCHAR(255) DEFAULT 'avatar-default.jpg',
    banner_color VARCHAR(7) DEFAULT '#A0B4B7'
);

CREATE TABLE materias_usuarios (
    padron INT NOT NULL,
    codigo_materia VARCHAR(6) NOT NULL,
    estado ENUM('cursando', 'aprobada'),
    PRIMARY KEY (padron, codigo_materia),
    FOREIGN KEY (padron) REFERENCES usuarios(padron) ON DELETE CASCADE,
    FOREIGN KEY (codigo_materia) REFERENCES materias(codigo) ON DELETE CASCADE
);

CREATE TABLE horarios_usuarios (
    padron INT NOT NULL,
    dia ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo') NOT NULL,
    turno ENUM('mañana', 'tarde', 'noche') NOT NULL,
    PRIMARY KEY (padron, dia, turno),
    FOREIGN KEY (padron) REFERENCES usuarios(padron) ON DELETE CASCADE
);

CREATE TABLE grupos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_materia VARCHAR(6) NOT NULL,
    nombre VARCHAR(50),
    tp_terminado BOOLEAN DEFAULT FALSE,
    maximo_integrantes INT DEFAULT 10,
    UNIQUE (codigo_materia, nombre),
    FOREIGN KEY (codigo_materia) REFERENCES materias(codigo) ON DELETE CASCADE
);

CREATE TABLE grupos_usuarios (
    id_grupo INT NOT NULL,
    padron INT NOT NULL,
    codigo_materia VARCHAR(6) NOT NULL,
    PRIMARY KEY (id_grupo, padron),
    UNIQUE (padron, codigo_materia),
    FOREIGN KEY (id_grupo) REFERENCES grupos (id) ON DELETE CASCADE,
    FOREIGN KEY (padron) REFERENCES usuarios (padron) ON DELETE CASCADE,
    FOREIGN KEY (codigo_materia) REFERENCES materias (codigo) ON DELETE CASCADE
);

CREATE TABLE horarios_grupos (
    id_grupo INT NOT NULL,
    dia ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo') NOT NULL,
    turno ENUM('mañana', 'tarde', 'noche') NOT NULL,
    PRIMARY KEY (id_grupo, dia, turno),
    FOREIGN KEY (id_grupo) REFERENCES grupos(id) ON DELETE CASCADE
);

CREATE TABLE solicitudes_grupos (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,
    padron_emisor INT,
    padron_receptor INT,
    estado ENUM('pendiente', 'aceptada', 'rechazada') DEFAULT 'pendiente',
    tipo ENUM('usuario_a_grupo', 'grupo_a_usuario', 'usuario_a_usuario') NOT NULL,
    FOREIGN KEY (id_grupo) REFERENCES grupos(id) ON DELETE CASCADE,
    FOREIGN KEY (padron_emisor) REFERENCES usuarios(padron) ON DELETE CASCADE,
    FOREIGN KEY (padron_receptor) REFERENCES usuarios(padron) ON DELETE CASCADE
);


