-- Calcular descuento aplicado a un producto
CREATE OR REPLACE FUNCTION calcular_descuento(
    precio_original DECIMAL,
    porcentaje_descuento DECIMAL
) RETURNS DECIMAL AS $$
BEGIN
    IF porcentaje_descuento < 0 OR porcentaje_descuento > 100 THEN
        RAISE EXCEPTION 'El porcentaje de descuento debe estar entre 0 y 100';
    END IF;
    
    RETURN precio_original * (1 - porcentaje_descuento / 100);
END;
$$ LANGUAGE plpgsql;

-- Validar si un correo electrónico contiene '@'
CREATE OR REPLACE FUNCTION validar_email(
    texto VARCHAR
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN texto LIKE '%@%';
END;
$$ LANGUAGE plpgsql;

-- Devolver productos con stock menor a un valor dado
CREATE OR REPLACE FUNCTION productos_stock_bajo(
    cantidad_minima INTEGER
) RETURNS TABLE(
    id_producto INTEGER,
    nombre_producto VARCHAR,
    precio_producto DECIMAL,
    stock_actual INTEGER,
    categoria_producto VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.nombre,
        p.precio,
        p.stock,
        p.categoria
    FROM productos p
    WHERE p.stock < cantidad_minima
    ORDER BY p.stock ASC;
END;
$$ LANGUAGE plpgsql;

-- Recibir una fecha y devolver el día de la semana
CREATE OR REPLACE FUNCTION obtener_dia_semana(
    fecha DATE
) RETURNS VARCHAR AS $$
DECLARE
    dia_semana VARCHAR;
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
        END INTO dia_semana;
    
    RETURN dia_semana;
END;
$$ LANGUAGE plpgsql;

-- Contar cuántos empleados hay en un departamento
CREATE OR REPLACE FUNCTION contar_empleados_departamento(
    id_departamento INTEGER
) RETURNS INTEGER AS $$
DECLARE
    total_empleados INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_empleados
    FROM empleados
    WHERE departamento_id = id_departamento;
    
    RETURN total_empleados;
END;
$$ LANGUAGE plpgsql;
