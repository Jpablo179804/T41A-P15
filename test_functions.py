import pytest
import psycopg2
from datetime import date

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
    return psycopg2.connect(**DB_CONFIG)

class TestDatabaseFunctions:
    
    def test_calcular_descuento(self):
        """Test para la función calcular_descuento"""
        conn = get_connection()
        cur = conn.cursor()
        
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
        
        cur.close()
        conn.close()
    
    def test_calcular_descuento_errores(self):
        """Test para manejo de errores en calcular_descuento"""
        conn = get_connection()
        cur = conn.cursor()
        
        # Test: Porcentaje negativo
        with pytest.raises(Exception):
            cur.execute("SELECT calcular_descuento(100, -10)")
        
        # Test: Porcentaje mayor a 100
        with pytest.raises(Exception):
            cur.execute("SELECT calcular_descuento(100, 150)")
        
        cur.close()
        conn.close()
    
    def test_validar_email(self):
        """Test para la función validar_email"""
        conn = get_connection()
        cur = conn.cursor()
        
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
        
        email_valido = next(r for r in results if r[0] == 'juan.perez@empresa.com')
        email_invalido = next(r for r in results if r[0] == 'carlos.lopezempresa.com')
        
        assert email_valido[1] == True
        assert email_invalido[1] == False
        
        cur.close()
        conn.close()
    
    def test_productos_stock_bajo(self):
        """Test para la función productos_stock_bajo"""
        conn = get_connection()
        cur = conn.cursor()
        
        # Test 1: Productos con stock menor a 10
        cur.execute("SELECT * FROM productos_stock_bajo(10)")
        results = cur.fetchall()
        
        # Verificar que todos los productos tienen stock menor a 10
        for producto in results:
            assert producto[3] < 10
        
        # Test 2: Productos con stock menor a 5
        cur.execute("SELECT * FROM productos_stock_bajo(5)")
        results = cur.fetchall()
        
        # Verificar que todos los productos tienen stock menor a 5
        for producto in results:
            assert producto[3] < 5
        
        # Test 3: Productos con stock menor a 0 (debería devolver productos sin stock)
        cur.execute("SELECT * FROM productos_stock_bajo(1)")
        results = cur.fetchall()
        
        # Verificar estructura de la respuesta
        if results:
            producto = results[0]
            assert len(producto) == 5  # id, nombre, precio, stock, categoria
            assert isinstance(producto[0], int)  # id
            assert isinstance(producto[1], str)  # nombre
            assert isinstance(producto[3], int)  # stock
        
        cur.close()
        conn.close()
    
    def test_obtener_dia_semana(self):
        """Test para la función obtener_dia_semana"""
        conn = get_connection()
        cur = conn.cursor()
        
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
            assert result == dia_esperado, f"La fecha {fecha} debería ser {dia_esperado}"
        
        cur.close()
        conn.close()
    
    def test_contar_empleados_departamento(self):
        """Test para la función contar_empleados_departamento"""
        conn = get_connection()
        cur = conn.cursor()
        
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
        
        cur.close()
        conn.close()
    
    def test_integracion_completa(self):
        """Test de integración que usa múltiples funciones"""
        conn = get_connection()
        cur = conn.cursor()
        
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
        assert producto_con_descuento[2] == producto_con_descuento[1] * 0.9
        
        cur.close()
        conn.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
