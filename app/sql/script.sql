-- Crear base de datos
CREATE DATABASE prueba;


-- Crear tabla
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    edad INTEGER NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contrasena VARCHAR(20) NOT NULL,
    id_rol INTEGER REFERENCES roles(id)
);

CREATE TABLE rol_modulo (
    id SERIAL PRIMARY KEY,
    id_rol INTEGER REFERENCES roles(id),
    id_modulo INTEGER REFERENCES modulos(id)
);

CREATE TABLE empleados_activos(
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    activos BOOLEAN NOT NULL
);

CREATE TABLE reportes (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    ubicacion VARCHAR(20) NOT NULL
);



-- Insertar registro
INSERT INTO roles(nombre) VALUES
('admin'),
('supervisor'),
('usuario');


INSERT INTO modulos(nombre) VALUES
('reportes'),
('usuarios'),
('configuracion');

INSERT INTO rol_modulo(id_rol,id_modulo) VALUES
(1,1),
(1,2),
(1,3),
(2,1),
(3,1);


INSERT INTO usuarios(
nombre,apellido,cedula,edad,usuario,contrasena,id_rol
) VALUES
('juan','perez','123',25,'juan','123',1),
('ana','lopez','456',22,'ana','123',2),
('camilo','gomez','322',26,'camilo','123',3);
