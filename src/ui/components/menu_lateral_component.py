# src/ui/components/menu_lateral_component.py

import customtkinter as ctk
from src.ui.styles.palet_colors import get_colors
from src.config import settings 

class MenuLateralComponent(ctk.CTkToplevel):
    """
    Componente de menú lateral (ventana CTkToplevel) con opciones y selector de tema.

    Args:
        parent (ctk.CTk): La ventana principal de la aplicación.
        cambiar_tema_callback (function): Función de callback para cambiar el tema de la aplicación.
    """
    def __init__(self, parent, cambiar_tema_callback):
        super().__init__(parent)
        self.parent = parent
        self._cambiar_tema_callback = cambiar_tema_callback
        self.colors = get_colors() 
        self.title(settings.APP_MESSAGES["MENU_OPTIONS_TITLE"]) 
        self.transient(parent) 
        self.attributes('-topmost', True) 
        self.resizable(False, False) 
        self._create_widgets()
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.hide_menu)

    def _create_widgets(self):
        """Crea y organiza los widgets dentro del menú lateral."""
        menu_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=(self.colors["card"], self.colors["card"]),
            border_width=1,
            border_color=(self.colors["borde"], self.colors["borde"])
        )
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            menu_frame,
            text=settings.APP_MESSAGES["MENU_OPTIONS_TITLE"], 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["texto"]
        ).pack(pady=15)

        theme_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        theme_frame.pack(pady=(10, 20))

        ctk.CTkLabel(
            theme_frame,
            text=settings.APP_MESSAGES["THEME_LABEL"],  
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["texto"]
        ).pack(side="left", padx=(0, 10))

        self.theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=[
                settings.APP_MESSAGES["THEME_VALUES_CLARO"],
                settings.APP_MESSAGES["THEME_VALUES_OSCURO"],
                settings.APP_MESSAGES["THEME_VALUES_SISTEMA"]
            ], 
            width=150,
            command=self._cambiar_tema_callback,
            height=35,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=13),
            fg_color=(self.colors["fondo_general"], self.colors["card"]),
            text_color=self.colors["texto"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
           
        )
        self.theme_combo.pack(side="right")
        self._set_current_theme_selection()
        
    def _set_current_theme_selection(self):
        """Establece la selección inicial en el ComboBox del tema."""
        actual_theme = ctk.get_appearance_mode()
        if actual_theme == "Light":
            self.theme_combo.set(settings.APP_MESSAGES["THEME_VALUES_CLARO"]) 
        elif actual_theme == "Dark":
            self.theme_combo.set(settings.APP_MESSAGES["THEME_VALUES_OSCURO"]) 
        else:
            self.theme_combo.set(settings.APP_MESSAGES["THEME_VALUES_SISTEMA"])

    def show_menu(self):
        """Muestra el menú lateral y lo posiciona."""
        x_pos = self.parent.winfo_x() + self.parent.winfo_width() - 320  
        y_pos = self.parent.winfo_y() + 50
        
        screen_width = self.winfo_screenwidth()
        if x_pos + 250 > screen_width:  
            x_pos = screen_width - 260  
        
        self.geometry(f"250x200+{x_pos}+{y_pos}")

        self.attributes("-alpha",0)
        self.deiconify()
        self.lift()
        self._fade_in()
        
    def _fade_in(self):
        alpha=self.attributes("-alpha")
        if alpha < 1 :
            self.attributes("-alpha", alpha + 0.1)
            self.after(20, self._fade_in)

    def hide_menu(self):
        """Oculta el menú lateral."""
        self._fade_out()

    def _fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            self.attributes("-alpha", alpha - 0.1)
            self.after(20, self._fade_out)
        else:
            self.withdraw    