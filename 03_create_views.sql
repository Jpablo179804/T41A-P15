-- 1. Función para calcular descuento
CREATE OR REPLACE FUNCTION calcular_descuento(
    precio_original NUMERIC, 
    porcentaje_descuento NUMERIC
)
RETURNS NUMERIC AS $$
BEGIN
    RETURN precio_original * (1 - porcentaje_descuento / 100);
END;
$$ LANGUAGE plpgsql;

-- 2. Función para validar correo electrónico
CREATE OR REPLACE FUNCTION validar_correo(correo TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN correo LIKE '%@%';
END;
$$ LANGUAGE plpgsql;

-- 3. Función para productos con stock bajo
CREATE OR REPLACE FUNCTION productos_stock_bajo(limite_stock INT)
RETURNS TABLE(
    id INT, 
    nombre TEXT, 
    stock INT, 
    precio NUMERIC
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id, p.nombre, p.stock, p.precio 
    FROM productos p 
    WHERE p.stock < limite_stock;
END;
$$ LANGUAGE plpgsql;

-- 4. Función para obtener día de la semana
CREATE OR REPLACE FUNCTION obtener_dia_semana(fecha DATE)
RETURNS TEXT AS $$
DECLARE
    dia_texto TEXT;
BEGIN
    SELECT 
        CASE EXTRACT(DOW FROM fecha)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Lunes'
            WHEN 2 THEN 'Martes'
            WHEN 3 THEN 'Miércoles'
            WHEN 4 THEN 'Jueves'
            WHEN 5 THEN 'Viernes'
            WHEN 6 THEN 'Sábado'
        END INTO dia_texto;
    
    RETURN dia_texto;
END;
$$ LANGUAGE plpgsql;

-- 5. Función para contar empleados por departamento
CREATE OR REPLACE FUNCTION contar_empleados_departamento(dep_id INT)
RETURNS INT AS $$
DECLARE
    total_empleados INT;
BEGIN
    SELECT COUNT(*) INTO total_empleados
    FROM empleados 
    WHERE departamento_id = dep_id;
    
    RETURN total_empleados;
END;
$$ LANGUAGE plpgsql;

-- 6. Función para calcular el IVA (del ejemplo)
CREATE OR REPLACE FUNCTION calcular_iva(monto NUMERIC, tasa NUMERIC DEFAULT 0.16)
RETURNS NUMERIC AS $$
BEGIN
    RETURN monto * tasa;
END;
$$ LANGUAGE plpgsql;

-- 7. Función para obtener nombre completo (del ejemplo)
CREATE OR REPLACE FUNCTION nombre_completo(nombre TEXT, apellido TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN nombre || ' ' || apellido;
END;
$$ LANGUAGE plpgsql;

-- 8. Función para verificar mayoría de edad (del ejemplo)
CREATE OR REPLACE FUNCTION es_mayor_de_edad(edad INT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN edad >= 18;
END;
$$ LANGUAGE plpgsql;

-- 9. Función de tabla: empleados por departamento (del ejemplo)
CREATE OR REPLACE FUNCTION empleados_por_departamento(dep_id INT)
RETURNS TABLE(id INT, nombre TEXT) AS $$
BEGIN
    RETURN QUERY SELECT e.id, e.nombre FROM empleados e WHERE e.departamento_id = dep_id;
END;
$$ LANGUAGE plpgsql;


-- Vista para empleados con información completa
CREATE OR REPLACE VIEW vista_empleados_completa AS
SELECT 
    e.id,
    e.nombre,
    e.apellido,
    e.email,
    e.edad,
    d.nombre as departamento,
    es_mayor_de_edad(e.edad) as es_mayor_edad,
    nombre_completo(e.nombre, e.apellido) as nombre_completo
FROM empleados e
LEFT JOIN departamentos d ON e.departamento_id = d.id;

-- Vista para productos con información de stock
CREATE OR REPLACE VIEW vista_productos_stock AS
SELECT 
    id,
    nombre,
    precio,
    stock,
    calcular_descuento(precio, 10) as precio_con_descuento_10,
    CASE 
        WHEN stock < 5 THEN 'CRÍTICO'
        WHEN stock < 10 THEN 'BAJO'
        ELSE 'NORMAL'
    END as estado_stock
FROM productos;
