-- 1. Eliminar si existe para evitar conflictos y crear la base de datos limpia
DROP DATABASE IF EXISTS examen_back2;
CREATE DATABASE examen_back2;
USE examen_back2;

-- 2. Crear tabla de categorías
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 3. Crear tabla de cursos con la relación correcta
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    precio DECIMAL(10,2),
    fecha_creacion DATE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

-- 4. Insertar datos base para que no esté vacía
INSERT INTO categorias (nombre) VALUES ('Programacion Backend'), ('Desarrollo Web');

INSERT INTO cursos (nombre, descripcion, categoria_id, precio, fecha_creacion) 
VALUES ('Node.js Master', 'Curso completo de APIs', 1, 150.00, '2026-04-18');

-- 5. Verificar que se crearon
SELECT * FROM categorias;
SELECT * FROM cursos;