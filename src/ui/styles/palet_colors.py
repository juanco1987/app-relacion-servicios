# src/ui/styles/palet_colors.py

"""
Paleta de colores para la aplicación - Mantiene consistencia visual en todos los componentes
"""
import customtkinter as ctk 

APP_COLORS = {
    "light": {
        "fondo_general": "#ededed",      # Casi blanco, muy limpio
        "header": "#1e40af",             # Azul oscuro y fuerte para el encabezado
        "card": "#f5f2f2",               # Tarjetas blancas y puras
        "sombra": "#acacac",             # Sombra gris clara y sutil
        "texto": "#1e293b",              # Texto oscuro para alta legibilidad
        "texto_header": "#ffffff",       # Texto blanco para contrastar con el header azul
        "borde": "#c5ccd4",              # Borde del mismo color que la sombra
        "accent": "#3b82f6",             # Azul de acento vibrante (para iconos, etc.)
        "accent_hover": "#2563eb",       # Un azul un poco más oscuro para el hover   
               

        # --- PALETA DE BOTONES  ---
        "boton_primario": "#2563eb",          # Un azul principal sólido y confiable
        "boton_primario_hover": "#1d4ed8",    # Un azul más oscuro para el hover, indicando interacción
        "boton_secundario": "#e2e8f0",        # Botón secundario discreto
        "boton_secundario_texto": "#1e40af",  # Texto del secundario que coincide con el header
        "disabled": "#cbd5e1",                # Color para estado deshabilitado
        "texto_disabled": "#64748b",          # Texto para estado deshabilitado
        
        # --- PALETA SEMÁNTICA (Éxito, Error, etc.) ---
        "exito": "#16a34a",               # Verde de éxito
        "exito_hover": "#15803d",         # Verde de éxito más oscuro
        "error": "#dc2626",               # Rojo de error
        "error_hover": "#b91c1c",         # Rojo de error más oscuro
        "warning": "#f59e0b",             # Naranja de advertencia
        "info": "#3b82f6",                # Azul de información (mismo que el acento)
        
        # --- COMPONENTES ESPECÍFICOS ---
        "console_bg": "#f1efef",
        "console_texto": "#1e293b",
        "hover_sutil": "#f1f5f9"
    },
    "dark": {
        "fondo_general": "#0f172a",      # Fondo oscuro profundo (casi negro)
        "header": "#1e40af",             # El mismo azul oscuro funciona bien en ambos temas
        "card": "#1e293b",               # Tarjetas de un azul-gris oscuro
        "sombra": "#0f172a",             # Sombra del mismo color que el fondo para un efecto sutil
        "texto": "#f1f5f9",              # Texto claro para alto contraste
        "texto_header": "#ffffff",       # Texto blanco
        "borde": "#334155",              # Borde azul-gris
        "accent": "#3b82f6",             # El mismo azul de acento vibrante
        "accent_hover": "#2563eb",       # Y su hover
        
        # --- PALETA DE BOTONES  ---
        "boton_primario": "#3b82f6",        # En modo oscuro, usamos el azul de acento como primario
        "boton_primario_hover": "#2563eb",  # Y su hover
        "boton_secundario": "#334155",      # Botón secundario más oscuro
        "boton_secundario_texto": "#e2e8f0",
        "disabled": "#334155",
        "texto_disabled": "#94a3b8",

        # --- PALETA SEMÁNTICA (Éxito, Error, etc.) ---
        "exito": "#22c55e",               # Un verde más brillante para el modo oscuro
        "exito_hover": "#16a34a",         # Su hover
        "error": "#ef4444",               # Un rojo más brillante
        "error_hover": "#dc2626",         # Su hover
        "warning": "#f59e0b",
        "info": "#3b82f6",

        # --- COMPONENTES ESPECÍFICOS ---
        "console_bg": "#1e293b",
        "console_texto": "#e2e8f0",
        "hover_sutil": "#1e293b"
    }
}

def get_colors():
    """Obtiene la paleta de colores según el tema actual"""
    modo = ctk.get_appearance_mode().lower()
    return APP_COLORS.get(modo, APP_COLORS["light"])