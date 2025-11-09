INSERT INTO productos (nombre, precio, stock, categoria) VALUES
('Laptop Gaming', 1200.00, 5, 'Electrónicos'),
('Smartphone', 800.00, 15, 'Electrónicos'),
('Tablet', 300.00, 3, 'Electrónicos'),
('Auriculares Bluetooth', 150.00, 25, 'Accesorios'),
('Teclado Mecánico', 120.00, 0, 'Accesorios'),
('Monitor 24"', 350.00, 8, 'Electrónicos'),
('Mouse Inalámbrico', 45.00, 30, 'Accesorios');

INSERT INTO departamentos (nombre) VALUES
('Ventas'),
('TI'),
('Recursos Humanos'),
('Marketing'),
('Finanzas');

INSERT INTO empleados (nombre, email, departamento_id, fecha_contratacion) VALUES
('Juan Pérez', 'juan.perez@empresa.com', 1, '2020-03-15'),
('María García', 'maria.garcia@empresa.com', 2, '2019-07-22'),
('Carlos López', 'carlos.lopezempresa.com', 2, '2021-01-10'), 
('Ana Rodríguez', 'ana.rodriguez@empresa.com', 3, '2018-11-05'),
('Pedro Martínez', 'pedro.martinez@empresa.com', 1, '2022-06-30'),
('Laura Sánchez', 'laura.sanchez@empresa.com', 4, '2020-09-12'),
('Miguel Torres', 'miguel.torres@empresa.com', 2, '2019-04-18');
