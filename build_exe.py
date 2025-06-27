#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir el ejecutable de la aplicación Sistema de Relaciones de Servicios
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def print_step(message):
    """Imprime un mensaje de paso con formato"""
    print(f"\n{'='*60}")
    print(f"🔄 {message}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print_step("Verificando dependencias")
    
    required_packages = [
        'customtkinter',
        'Pillow', 
        'pandas',
        'openpyxl',
        'fpdf',
        'tkcalendar',
        'pyinstaller'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} - OK")
        except ImportError:
            missing_packages.append(package)
            print_error(f"{package} - FALTANTE")
    
    if missing_packages:
        print_error(f"Faltan las siguientes dependencias: {', '.join(missing_packages)}")
        print("Instálalas con: pip install " + " ".join(missing_packages))
        return False
    
    return True

def clean_build_dirs():
    """Limpia directorios de build anteriores"""
    print_step("Limpiando directorios de build anteriores")
    
    dirs_to_clean = ['build', 'dist']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print_success(f"Directorio {dir_name} eliminado")
            except Exception as e:
                print_error(f"Error eliminando {dir_name}: {e}")

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print_step("Construyendo ejecutable con PyInstaller")
    
    spec_file = "relacion_servicios_mejorado.spec"
    
    if not os.path.exists(spec_file):
        print_error(f"Archivo {spec_file} no encontrado")
        return False
    
    try:
        # Comando para construir el ejecutable
        cmd = [
            'pyinstaller',
            '--clean',  # Limpiar cache
            '--noconfirm',  # No preguntar confirmación
            spec_file
        ]
        
        print("Ejecutando:", " ".join(cmd))
        
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Ejecutable construido exitosamente")
            return True
        else:
            print_error("Error durante la construcción:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print_error(f"Error ejecutando PyInstaller: {e}")
        return False

def verify_executable():
    """Verifica que el ejecutable se haya creado correctamente"""
    print_step("Verificando ejecutable")
    
    exe_path = os.path.join('dist', 'Sistema_Relaciones_Servicios_v1.0.exe')
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print_success(f"Ejecutable creado: {exe_path}")
        print_success(f"Tamaño: {size_mb:.1f} MB")
        return True
    else:
        print_error("Ejecutable no encontrado")
        return False

def create_release_info():
    """Crea información de release"""
    print_step("Creando información de release")
    
    release_info = f"""
# Release v1.0.0 - {datetime.now().strftime('%d/%m/%Y')}

## 🎉 Nueva versión mejorada del Sistema de Relaciones de Servicios

### ✅ Mejoras implementadas:
- Interfaz moderna con CustomTkinter
- Sistema de temas (claro/oscuro/sistema)
- Animaciones fluidas y efectos visuales
- Componentes modulares y reutilizables
- Paleta de colores centralizada
- Manejo robusto de errores
- Documentación completa

### 📦 Archivos incluidos:
- Sistema_Relaciones_Servicios_v1.0.exe (ejecutable principal)
- README.md (documentación)
- requirements.txt (dependencias)

### 🚀 Instalación:
1. Descarga el archivo .exe
2. Ejecuta directamente (no requiere instalación)
3. ¡Listo para usar!

### 📋 Requisitos del sistema:
- Windows 10/11 (64-bit)
- No requiere Python instalado
- No requiere dependencias adicionales

### 🔧 Características técnicas:
- Procesamiento de archivos Excel
- Generación de informes PDF
- Selector de fechas con calendario
- Consola de procesamiento en tiempo real
- Interfaz responsive y moderna

---
Desarrollado con ❤️ usando Python y CustomTkinter
"""
    
    with open('RELEASE_NOTES.md', 'w', encoding='utf-8') as f:
        f.write(release_info)
    
    print_success("Información de release creada: RELEASE_NOTES.md")

def main():
    """Función principal"""
    print("🚀 CONSTRUCTOR DE EJECUTABLE - Sistema de Relaciones de Servicios")
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Verificar dependencias
    if not check_dependencies():
        return False
    
    # Limpiar directorios anteriores
    clean_build_dirs()
    
    # Construir ejecutable
    if not build_executable():
        return False
    
    # Verificar resultado
    if not verify_executable():
        return False
    
    # Crear información de release
    create_release_info()
    
    print_step("🎉 CONSTRUCCIÓN COMPLETADA EXITOSAMENTE")
    print_success("El ejecutable está listo en la carpeta 'dist'")
    print_success("Puedes distribuir el archivo .exe directamente")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 