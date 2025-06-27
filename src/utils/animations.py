# src/ui/utils/animations.py
import customtkinter as ctk
from customtkinter import CTkBaseClass
from src.ui.styles.palet_colors import get_colors

from customtkinter.windows.widgets.core_widget_classes.ctk_base_class import CTkBaseClass

def animate_color_change(widget: CTkBaseClass, property_name: str, start_color, end_color, duration=200):
    """
    Anima el cambio de color entre dos colores HEX en un widget de customtkinter,
    siendo consciente del tema (claro/oscuro).
    """
    if not hasattr(widget, "winfo_exists") or not widget.winfo_exists():
        return

    # Helper para obtener el color correcto según el tema
    def get_theme_color(color_val):
        if isinstance(color_val, str):
            return color_val
        if isinstance(color_val, tuple):
            return color_val[1] if ctk.get_appearance_mode() == "Dark" else color_val[0]        
        return "#FFFFFF"

    # Obtener los colores correctos para el tema actual
    start_color_hex = get_theme_color(start_color)
    end_color_hex = get_theme_color(end_color)

    # Hex → RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        try:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except (ValueError, TypeError):
            return None 

    def rgb_to_hex(rgb_tuple):
        # Asegurarse de que los valores RGB estén siempre entre 0 y 255.
        safe_rgb = [max(0, min(255, int(v))) for v in rgb_tuple]
        return f"#{safe_rgb[0]:02x}{safe_rgb[1]:02x}{safe_rgb[2]:02x}"

    start_rgb = hex_to_rgb(start_color_hex)
    end_rgb = hex_to_rgb(end_color_hex)
        
    if start_rgb is None or end_rgb is None:
        widget.configure({property_name: end_color_hex})
        return

    steps = 15 
    interval = max(1, int(duration / steps))
    step_size = [(end - start) / steps for start, end in zip(start_rgb, end_rgb)]

    def update_step(step=0):
        if not widget.winfo_exists():
            return

        if step <= steps:
            current_rgb = [
                start_rgb[i] + step_size[i] * step
                for i in range(3)
            ]
            current_hex = rgb_to_hex(current_rgb)
            widget.configure({property_name: current_hex})
            widget.after(interval, update_step, step + 1)
        else:
            # Asegurarse de que el color final sea exacto
            widget.configure({property_name: end_color_hex})

    update_step()



def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_tuple):
    return f"#{int(rgb_tuple[0]):02x}{int(rgb_tuple[1]):02x}{int(rgb_tuple[2]):02x}"


def animate_pulse(widget, property_name, base_color, pulse_duration=500, fade_out_duration=500):
    """
    Inicia una animación de pulso que resalta un widget y luego se desvanece.
    """
    colors = get_colors()
    pulse_color = colors["accent"] 

    if isinstance(base_color, tuple):
        base_color = base_color[0]
    
    base_rgb = hex_to_rgb(base_color)
    pulse_rgb = hex_to_rgb(pulse_color)

    steps_in = 10 
    steps_out = 10 

    # Animación de entrada (hacia el color de pulso)
    def pulse_in_step(step=0):
        if not widget.winfo_exists():
            return

        if step <= steps_in:
            intensity = step / steps_in
            r = int(base_rgb[0] + (pulse_rgb[0] - base_rgb[0]) * intensity)
            g = int(base_rgb[1] + (pulse_rgb[1] - base_rgb[1]) * intensity)
            b = int(base_rgb[2] + (pulse_rgb[2] - base_rgb[2]) * intensity)
            
            color_hex = rgb_to_hex((r, g, b))
            widget.configure({property_name: color_hex})
            widget.after(int(pulse_duration / (2 * steps_in)), pulse_in_step, step + 1)
        else:
            # Una vez que llega al pico, comienza el desvanecimiento
            widget.after(100, pulse_out_step, 0) 

    # Animación de salida (de vuelta al color base)
    def pulse_out_step(step=0):
        if not widget.winfo_exists():
            return
        
        if step <= steps_out:
            intensity = 1 - (step / steps_out) # De 1 a 0
            r = int(base_rgb[0] + (pulse_rgb[0] - base_rgb[0]) * intensity)
            g = int(base_rgb[1] + (pulse_rgb[1] - base_rgb[1]) * intensity)
            b = int(base_rgb[2] + (pulse_rgb[2] - base_rgb[2]) * intensity)
            
            color_hex = rgb_to_hex((r, g, b))
            widget.configure({property_name: color_hex})
            widget.after(int(fade_out_duration / (2 * steps_out)), pulse_out_step, step + 1)
        else:
            widget.configure({property_name: base_color}) # Asegurarse de volver al color base

    pulse_in_step(0)


def animate_progress(widget, property_name, base_color, duration=5000):
    """Inicia una animación de progreso en el widget."""
    colors = get_colors()
    progress_color = colors["accent"]

    if isinstance(base_color, tuple):
        base_color = base_color[0]
    
    base_rgb = hex_to_rgb(base_color)
    progress_rgb = hex_to_rgb(progress_color)

    steps = 100

    def progress_step(step):
        if not widget.winfo_exists():
            return
            
        if step <= steps:
            progress = step / steps           
            r = int((1 - progress) * base_rgb[0] + progress * progress_rgb[0])
            g = int((1 - progress) * base_rgb[1] + progress * progress_rgb[1])
            b = int((1 - progress) * base_rgb[2] + progress * progress_rgb[2])

            current_color_hex = rgb_to_hex((r, g, b))
            widget.configure({property_name: current_color_hex})
            widget.after(int(duration / steps), progress_step, step + 1)
        else:
            # widget.configure({property_name: base_color})
            pass

    progress_step(0) 

def fade_in(window, step=0.1, delay=20):
    alpha = window.attributes('-alpha')
    if alpha < 1.0:
        window.attributes('-alpha', alpha + step)
        window.after(delay, lambda: fade_in(window, step, delay))
    else:
        window.attributes('-alpha', 1)

def fade_out(window, step=0.1, delay=20):
    alpha = window.attributes('-alpha')
    if alpha > 0:
        window.attributes('-alpha', alpha - step)
        window.after(delay, lambda: fade_out(window, step, delay))
    else:
        window.destroy() 

def button_animate_pulse(modern_button, pulse_color=None, steps=10, delay=12):
    """
    Anima un pulso de color en el botón ModernButton.
    modern_button: instancia de ModernButton
    pulse_color: color de pulso (por defecto success_hover de la paleta)
    """
    from src.ui.styles.palet_colors import get_colors
    if pulse_color is None:
        pulse_color = get_colors().get("success_hover")
    base_color = modern_button.button.cget("fg_color")
    def restore():
        modern_button._animate_color_change(
            modern_button.button.cget("fg_color"),
            modern_button.base_color,
            steps=15, delay=10
        )
    modern_button._animate_color_change(
        base_color, pulse_color, steps=steps, delay=delay
    )
    modern_button.after(300, restore)

def button_animate_progress(modern_button):
    """
    Anima el texto del botón ModernButton con puntos suspensivos para indicar progreso.
    """
    if getattr(modern_button, '_progress_anim_id', None) is not None:
        return
    modern_button._original_text = modern_button.button.cget("text")
    dots = ["", ".", "..", "..."]
    modern_button._dot_index = 0
    def progress_step():
        if getattr(modern_button, '_progress_anim_id', None) is None:
            return
        modern_button.button.configure(text=f"{modern_button._original_text}{dots[modern_button._dot_index]}")
        modern_button._dot_index = (modern_button._dot_index + 1) % len(dots)
        modern_button._progress_anim_id = modern_button.after(500, progress_step)
    modern_button._progress_anim_id = modern_button.after(500, progress_step)

def button_stop_progress_animation(modern_button):
    if getattr(modern_button, '_progress_anim_id', None) is not None:
        modern_button.after_cancel(modern_button._progress_anim_id)
        modern_button._progress_anim_id = None
        modern_button.button.configure(text=modern_button._original_text) 

def animate_progress_bar(progress_bar, steps=6, delay=700, on_complete=None):
    """
    Anima una barra de progreso de izquierda a derecha en pasos.
    - progress_bar: instancia de CTkProgressBar
    - steps: número de pasos (por ejemplo, igual al número de mensajes de carga)
    - delay: milisegundos entre cada paso
    - on_complete: función a llamar al finalizar la animación
    """
    def step(index):
        if index < steps:
            progress_bar.set(index / (steps - 1))
            progress_bar.after(delay, step, index + 1)
        else:
            progress_bar.set(1)
            if on_complete:
                on_complete()
    step(0)        