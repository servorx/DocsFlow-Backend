CREATE DATABASE IF NOT EXISTS coworking;
USE coworking;

CREATE TABLE `departamentos` (
    `id_departamento` int PRIMARY KEY AUTO_INCREMENT,
    `name_departamento` varchar(255) NOT NULL
);

CREATE TABLE `usuarios` (
    `id_user` int PRIMARY KEY AUTO_INCREMENT,
    `nombre` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL UNIQUE,
    `password` varchar(255) NOT NULL,
    `rol` enum('admin','operador') NOT NULL DEFAULT 'operador',
    `id_departamento` int NOT NULL,
    CONSTRAINT `fk_usuarios_departamento` FOREIGN KEY (`id_departamento`) REFERENCES `departamentos` (`id_departamento`) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE `documentos` (
    `id_documento` int PRIMARY KEY AUTO_INCREMENT,
    `nombre_documento` varchar(255) NOT NULL,
    `file_path` varchar(255) NOT NULL,
    `user_id` int NOT NULL,
    CONSTRAINT `fk_documentos_usuario` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `data_extraida` (
    `id_tabla` int PRIMARY KEY AUTO_INCREMENT,
    `documento_id` int NOT NULL,
    `table_data` LONGTEXT NOT NULL,
    CONSTRAINT `fk_data_extraida_documento` FOREIGN KEY (`documento_id`) REFERENCES `documentos` (`id_documento`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `key_data` (
    `id_data` int PRIMARY KEY AUTO_INCREMENT,
    `documento_id` int NOT NULL,
    `tabla_id` int NOT NULL,
    `key` varchar(255) NOT NULL,
    `value` varchar(255) NOT NULL,
    CONSTRAINT `fk_key_data_documento` FOREIGN KEY (`documento_id`) REFERENCES `documentos` (`id_documento`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_key_data_tabla` FOREIGN KEY (`tabla_id`) REFERENCES `data_extraida` (`id_tabla`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `reset_password_tokens` (
    `id_token` int PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `token` varchar(255) NOT NULL,
    `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_reset_tokens_usuario` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
);
