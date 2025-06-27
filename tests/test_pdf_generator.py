import unittest
import os
import pandas as pd
from datetime import datetime
from src.core.pdf_generator import generar_pdf, generar_pdf_modular, _abrir_pdf

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame de prueba
        self.test_data = pd.DataFrame({
            'FECHA': ['01/01/2024', '15/01/2024', '31/01/2024'],
            'CONCEPTO': ['Servicio 1', 'Servicio 2', 'Servicio 3'],
            'IMPORTE': ['100.00', '200.00', '300.00']
        })
        
        # Configurar directorio de prueba
        self.test_dir = 'test_pdfs'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        self.test_pdf = os.path.join(self.test_dir, 'test.pdf')
        
    def tearDown(self):
        # Limpiar archivos de prueba
        if os.path.exists(self.test_pdf):
            os.remove(self.test_pdf)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_generar_pdf(self):
        # Probar generación de PDF
        exito, mensaje = generar_pdf(
            self.test_data,
            self.test_pdf,
            "Notas de prueba"
        )
        
        self.assertTrue(exito)
        self.assertTrue(os.path.exists(self.test_pdf))
    
    def test_generar_pdf_modular(self):
        # Probar generación de PDF con función modular
        def mock_log(message, level="info"):
            pass
        
        exito, mensaje = generar_pdf_modular(
            self.test_data,
            'test.pdf',
            "Notas de prueba",
            mock_log
        )
        
        self.assertTrue(exito)
    
    def test_abrir_pdf(self):
        # Primero generar un PDF
        exito, _ = generar_pdf(
            self.test_data,
            self.test_pdf,
            "Notas de prueba"
        )
        
        # Probar apertura de PDF
        def mock_log(message, level="info"):
            pass
        
        resultado = _abrir_pdf(self.test_pdf, mock_log)
        self.assertTrue(resultado)
    
    def test_abrir_pdf_inexistente(self):
        # Probar apertura de PDF inexistente
        def mock_log(message, level="info"):
            pass
        
        resultado = _abrir_pdf('no_existe.pdf', mock_log)
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main() 