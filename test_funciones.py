import pytest
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="postgres"
    )

def test_calcular_descuento():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT calcular_descuento(100, 10)")
    result = cur.fetchone()[0]
    assert result == 90.0
    cur.close()
    conn.close()

def test_validar_correo():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Correo válido
    cur.execute("SELECT validar_correo('test@example.com')")
    result1 = cur.fetchone()[0]
    assert result1 == True
    
    # Correo inválido
    cur.execute("SELECT validar_correo('testexample.com')")
    result2 = cur.fetchone()[0]
    assert result2 == False
    
    cur.close()
    conn.close()

def test_productos_stock_bajo():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM productos_stock_bajo(10)")
    results = cur.fetchall()
    
    # Verificar que se retornan productos con stock menor a 10
    assert len(results) > 0
    for producto in results:
        assert producto[2] < 10  # stock < 10
    
    cur.close()
    conn.close()

def test_obtener_dia_semana():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT obtener_dia_semana('2024-01-01')")
    result = cur.fetchone()[0]
    assert result == 'Lunes'  # 2024-01-01 fue lunes
    
    cur.close()
    conn.close()

def test_contar_empleados_departamento():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT contar_empleados_departamento(1)")
    result = cur.fetchone()[0]
    assert result >= 0  # Debe retornar un número no negativo
    
    cur.close()
    conn.close()

def test_es_mayor_de_edad():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Mayor de edad
    cur.execute("SELECT es_mayor_de_edad(25)")
    result1 = cur.fetchone()[0]
    assert result1 == True
    
    # Menor de edad
    cur.execute("SELECT es_mayor_de_edad(16)")
    result2 = cur.fetchone()[0]
    assert result2 == False
    
    cur.close()
    conn.close()

def test_nombre_completo():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT nombre_completo('Juan', 'Pérez')")
    result = cur.fetchone()[0]
    assert result == 'Juan Pérez'
    
    cur.close()
    conn.close()
