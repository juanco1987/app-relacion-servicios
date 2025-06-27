import unittest
from datetime import datetime
import pandas as pd
from src.core.excel_processor import extraer_servicios

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        # Crear un DataFrame de prueba
        self.test_data = pd.DataFrame({
            'FECHA': ['01/01/2024', '15/01/2024', '31/01/2024'],
            'CONCEPTO': ['Servicio 1', 'Servicio 2', 'Servicio 3'],
            'IMPORTE': ['100.00', '200.00', '300.00']
        })
        
        # Guardar el DataFrame como Excel temporal
        self.test_file = 'test_servicios.xlsx'
        self.test_data.to_excel(self.test_file, index=False)
        
    def tearDown(self):
        # Limpiar archivo de prueba
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_extraer_servicios_fechas_validas(self):
        # Probar con fechas válidas
        fecha_inicio = datetime(2024, 1, 1)
        fecha_fin = datetime(2024, 1, 31)
        
        def mock_log(message, level="info"):
            pass
        
        df_resultado = extraer_servicios(
            self.test_file,
            fecha_inicio,
            fecha_fin,
            mock_log
        )
        
        self.assertFalse(df_resultado.empty)
        self.assertEqual(len(df_resultado), 3)
    
    def test_extraer_servicios_fuera_rango(self):
        # Probar con fechas fuera de rango
        fecha_inicio = datetime(2024, 2, 1)
        fecha_fin = datetime(2024, 2, 28)
        
        def mock_log(message, level="info"):
            pass
        
        df_resultado = extraer_servicios(
            self.test_file,
            fecha_inicio,
            fecha_fin,
            mock_log
        )
        
        self.assertTrue(df_resultado.empty)

if __name__ == '__main__':
    unittest.main() 