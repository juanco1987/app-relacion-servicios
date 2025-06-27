# Sistema de Relaciones de Servicios

Aplicación moderna para la gestión y generación de informes de servicios pagados en efectivo, con una interfaz gráfica intuitiva, animaciones y funcionalidades avanzadas.

---

## Características

- 🎨 Interfaz moderna con soporte para temas claro, oscuro y sistema.
- 📊 Procesamiento y filtrado de archivos Excel.
- 📄 Generación de informes en PDF.
- 📅 Selector de fechas con calendario visual y selección rápida.
- 📝 Notas personalizadas en los informes.
- 🔍 Vista previa y apertura de PDF generados.
- 📋 Consola de procesamiento en tiempo real.
- 🖱️ Botones animados y experiencia de usuario fluida.
- 🛠️ Modularidad y componentes reutilizables.

---

## Instalación

### Opción 1: Ejecutable (Recomendado)
1. Descarga el archivo `.exe` desde la sección [Releases](https://github.com/tu-usuario/app-relacion-servicios/releases)
2. Ejecuta el archivo directamente (no requiere instalación)

### Opción 2: Código fuente
1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd [NOMBRE_DEL_DIRECTORIO]
   ```

2. (Opcional) Crea un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

---

## Uso

1. Ejecuta la aplicación (ejecutable o código fuente).
2. En la interfaz:
   - Selecciona el archivo Excel con los datos.
   - Elige el período de fechas.
   - Agrega notas (opcional).
   - Procesa los datos.
   - Genera el PDF.
   - Abre el PDF generado.

---

## Estructura del Proyecto

```
src/
├── core/               # Lógica principal de negocio
│   ├── excel_processor.py
│   └── pdf_generator.py
├── ui/                 # Interfaz de usuario y componentes visuales
│   ├── main_window.py
│   ├── components/
│   │   ├── action_card.py
│   │   ├── date_range_card.py
│   │   ├── file_selection_card.py
│   │   ├── header_component.py
│   │   ├── menu_lateral_component.py
│   │   ├── modern_button.py
│   │   ├── notes_card.py
│   │   ├── splash_screen.py
│   │   └── terminal_componet.py
│   └── styles/
│       └── palet_colors.py
├── utils/              # Utilidades generales y animaciones
│   ├── animations.py
│   ├── date_utils.py
│   ├── file_utils.py
│   └── validation_utils.py
├── config/             # Configuración y constantes
│   └── settings.py
└── main.py             # Punto de entrada de la aplicación
```

- **recursos/**: Imágenes, íconos y recursos gráficos.
- **backup/**: Scripts para respaldo de datos.
- **tests/**: Pruebas unitarias de los módulos principales.

---

## Pruebas

El proyecto incluye pruebas unitarias para los módulos principales:
- `tests/test_excel_processor.py`
- `tests/test_pdf_generator.py`

Puedes ejecutarlas con:
```bash
python -m unittest discover tests
```

---

## Estructura del Excel

El archivo Excel debe contener las siguientes columnas:
- **FECHA** (formato dd/mm/yyyy)
- **CONCEPTO**
- **IMPORTE**

---

## Personalización Visual

- Los colores y estilos están centralizados en `src/ui/styles/palet_colors.py`.
- Los botones modernos (`ModernButton`) y otros componentes usan animaciones suaves y colores de la paleta.
- Puedes modificar la paleta para adaptar la app a tu identidad visual.

---

## Releases

### v1.0.0 - Versión Estable
- ✅ Interfaz moderna con CustomTkinter
- ✅ Procesamiento de archivos Excel
- ✅ Generación de informes PDF
- ✅ Sistema de temas (claro/oscuro)
- ✅ Animaciones y efectos visuales
- ✅ Componentes modulares y reutilizables

[Descargar ejecutable v1.0.0](https://github.com/tu-usuario/app-relacion-servicios/releases/tag/v1.0.0)

---

## Contribuir

1. Haz fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFeature`).
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva feature'`).
4. Haz push a la rama (`git push origin feature/NuevaFeature`).
5. Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## Contacto

Tu Nombre - [@tutwitter](https://twitter.com/tutwitter) - email@example.com

Link del Proyecto: [https://github.com/tu-usuario/app-relacion-servicios](https://github.com/tu-usuario/app-relacion-servicios) 