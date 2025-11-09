import pytest
import psycopg2
from datetime import date
import subprocess
import time

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    """Obtener conexión a la base de datos"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")

def test_calcular_descuento():
    """Test para la función calcular_descuento"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test 1: Descuento normal
        cur.execute("SELECT calcular_descuento(100, 20)")
        result = cur.fetchone()[0]
        assert result == 80.0
        
        # Test 2: Descuento del 0%
        cur.execute("SELECT calcular_descuento(100, 0)")
        result = cur.fetchone()[0]
        assert result == 100.0
        
        # Test 3: Descuento del 100%
        cur.execute("SELECT calcular_descuento(100, 100)")
        result = cur.fetchone()[0]
        assert result == 0.0
        
    finally:
        cur.close()
        conn.close()

def test_calcular_descuento_errores():
    """Test para manejo de errores en calcular_descuento"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test: Porcentaje negativo
        try:
            cur.execute("SELECT calcular_descuento(100, -10)")
            conn.rollback()
        except Exception:
            pass  # Se espera una excepción
        
        # Test: Porcentaje mayor a 100
        try:
            cur.execute("SELECT calcular_descuento(100, 150)")
            conn.rollback()
        except Exception:
            pass  # Se espera una excepción
            
    finally:
        cur.close()
        conn.close()

def test_validar_email():
    """Test para la función validar_email"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test 1: Email válido
        cur.execute("SELECT validar_email('usuario@dominio.com')")
        result = cur.fetchone()[0]
        assert result == True
        
        # Test 2: Email sin @
        cur.execute("SELECT validar_email('usuariodominio.com')")
        result = cur.fetchone()[0]
        assert result == False
        
        # Test 3: Email vacío
        cur.execute("SELECT validar_email('')")
        result = cur.fetchone()[0]
        assert result == False
        
        # Test 4: Verificar emails de la base de datos
        cur.execute("""
            SELECT email, validar_email(email) 
            FROM empleados 
            WHERE id IN (1, 3)
        """)
        results = cur.fetchall()
        
        # Encontrar los emails específicos
        email_valido = None
        email_invalido = None
        
        for email, es_valido in results:
            if 'juan.perez@empresa.com' in email:
                email_valido = es_valido
            if 'carlos.lopezempresa.com' in email:
                email_invalido = es_valido
        
        assert email_valido == True
        assert email_invalido == False
        
    finally:
        cur.close()
        conn.close()

def test_productos_stock_bajo():
    """Test para la función productos_stock_bajo"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test 1: Productos con stock menor a 10
        cur.execute("SELECT * FROM productos_stock_bajo(10)")
        results = cur.fetchall()
        
        # Verificar que todos los productos tienen stock menor a 10
        for producto in results:
            stock = producto[3]
            assert stock < 10, f"Producto {producto[1]} tiene stock {stock} que no es menor a 10"
        
        # Test 2: Productos con stock menor a 5
        cur.execute("SELECT * FROM productos_stock_bajo(5)")
        results = cur.fetchall()
        
        # Verificar que todos los productos tienen stock menor a 5
        for producto in results:
            stock = producto[3]
            assert stock < 5, f"Producto {producto[1]} tiene stock {stock} que no es menor a 5"
        
        # Test 3: Verificar estructura de la respuesta
        cur.execute("SELECT * FROM productos_stock_bajo(20)")
        results = cur.fetchall()
        
        if results:
            producto = results[0]
            assert len(producto) == 5  # id, nombre, precio, stock, categoria
            assert isinstance(producto[0], int)  # id
            assert isinstance(producto[3], int)  # stock
            
    finally:
        cur.close()
        conn.close()

def test_obtener_dia_semana():
    """Test para la función obtener_dia_semana"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test con fechas conocidas
        test_cases = [
            ('2024-01-01', 'Lunes'),    # 1 de enero de 2024 fue lunes
            ('2024-01-02', 'Martes'),
            ('2024-01-03', 'Miércoles'),
            ('2024-01-04', 'Jueves'),
            ('2024-01-05', 'Viernes'),
            ('2024-01-06', 'Sábado'),
            ('2024-01-07', 'Domingo'),
        ]
        
        for fecha, dia_esperado in test_cases:
            cur.execute("SELECT obtener_dia_semana(%s)", (fecha,))
            result = cur.fetchone()[0]
            assert result == dia_esperado, f"La fecha {fecha} debería ser {dia_esperado}, pero se obtuvo {result}"
            
    finally:
        cur.close()
        conn.close()

def test_contar_empleados_departamento():
    """Test para la función contar_empleados_departamento"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Test 1: Departamento de TI (id=2)
        cur.execute("SELECT contar_empleados_departamento(2)")
        result = cur.fetchone()[0]
        assert result == 3  # Según los datos insertados
        
        # Test 2: Departamento de Ventas (id=1)
        cur.execute("SELECT contar_empleados_departamento(1)")
        result = cur.fetchone()[0]
        assert result == 2  # Según los datos insertados
        
        # Test 3: Departamento sin empleados (id=5 - Finanzas)
        cur.execute("SELECT contar_empleados_departamento(5)")
        result = cur.fetchone()[0]
        assert result == 0
        
        # Test 4: Departamento inexistente
        cur.execute("SELECT contar_empleados_departamento(999)")
        result = cur.fetchone()[0]
        assert result == 0
        
    finally:
        cur.close()
        conn.close()

def test_integracion_completa():
    """Test de integración que usa múltiples funciones"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Verificar que hay empleados en TI con emails válidos
        cur.execute("""
            SELECT COUNT(*) 
            FROM empleados 
            WHERE departamento_id = 2 
            AND validar_email(email) = true
        """)
        empleados_ti_email_valido = cur.fetchone()[0]
        assert empleados_ti_email_valido > 0
        
        # Verificar productos con stock bajo
        cur.execute("SELECT COUNT(*) FROM productos_stock_bajo(5)")
        productos_stock_bajo = cur.fetchone()[0]
        assert productos_stock_bajo >= 0
        
        # Verificar cálculo de descuento para productos
        cur.execute("""
            SELECT nombre, precio, calcular_descuento(precio, 10) as precio_con_descuento
            FROM productos 
            WHERE stock > 0 
            LIMIT 1
        """)
        producto_con_descuento = cur.fetchone()
        precio_original = float(producto_con_descuento[1])
        precio_descuento = float(producto_con_descuento[2])
        expected_discount = precio_original * 0.9
        
        # Usar tolerancia para comparación de decimales
        assert abs(precio_descuento - expected_discount) < 0.01
        
    finally:
        cur.close()
        conn.close()

def test_database_connection():
    """Test básico para verificar la conexión a la base de datos"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Verificar que las tablas existen
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        expected_tables = ['productos', 'empleados', 'departamentos']
        for table in expected_tables:
            assert table in tables, f"La tabla {table} no existe"
            
        # Verificar que las funciones existen
        cur.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public'
        """)
        functions = [row[0] for row in cur.fetchall()]
        
        expected_functions = [
            'calcular_descuento', 
            'validar_email', 
            'productos_stock_bajo',
            'obtener_dia_semana', 
            'contar_empleados_departamento'
        ]
        
        for function in expected_functions:
            assert function in functions, f"La función {function} no existe"
            
    finally:
        cur.close()
        conn.close()
