INSERT INTO departamentos (nombre) VALUES 
('Ventas'),
('TI'),
('Recursos Humanos'),
('Marketing');

INSERT INTO empleados (nombre, apellido, email, edad, departamento_id) VALUES 
('Juan', 'Pérez', 'juan@empresa.com', 25, 1),
('María', 'Gómez', 'maria@empresa.com', 32, 2),
('Carlos', 'López', 'carlos@empresa.com', 17, 1),
('Ana', 'Martínez', 'ana.empresa.com', 28, 3); -- Correo inválido

INSERT INTO productos (nombre, precio, stock) VALUES 
('Laptop', 1500.00, 5),
('Mouse', 25.50, 50),
('Teclado', 75.00, 2),
('Monitor', 300.00, 0);
