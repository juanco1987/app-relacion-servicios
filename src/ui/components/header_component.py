# src/ui/components/header_component.py

import customtkinter as ctk
import os
from PIL import Image, ImageDraw
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.config import settings

class HeaderComponent(ctk.CTkFrame):
    def __init__(self, parent, abrir_menu_lateral_callback):
        self.colors = get_colors()
 
        super().__init__(
            parent,
            height=150,
            corner_radius=20,
            fg_color=(self.colors["header"], self.colors["header"]),
            border_width=1,
            border_color=(self.colors["accent"]) 
        )
        self.grid(row=0, column=0, sticky="ew", padx=25, pady=25)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self._abrir_menu_lateral_callback = abrir_menu_lateral_callback
        self.logo_label = None
        self._add_logo()
        self._add_info_section()
        self._add_menu_button()

    def _add_logo(self):
        try:
            logo_path = resource_path(settings.RESOURCE_PATHS["HEADER_LOGO"])
            img_size = (130, 130)

            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize(img_size, Image.Resampling.LANCZOS)
                mask = Image.new('L', img_size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + img_size, fill=255)
                img = img.convert("RGBA")
                img.putalpha(mask)                
                logo_image = ctk.CTkImage(img, size=img_size)
                self.logo_label = ctk.CTkLabel(self, image=logo_image, text="")
                self.logo_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
            
            else:                
                self.logo_label = ctk.CTkLabel(self, text="📊", font=ctk.CTkFont(size=80))
                self.logo_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
                print(settings.APP_MESSAGES["WARNING_LOGO_NOT_FOUND"].format(logo_path))

        except Exception as e:
            
            self.logo_label = ctk.CTkLabel(self, text="�", font=ctk.CTkFont(size=40))
            self.logo_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
            print(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["HEADER_ICON_WARNING_NAME"], e))
        
        if self.logo_label:
            pass  

    def _add_info_section(self):
        """Agrega la sección central de información (título, subtítulo, badges) al encabezado."""
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        title_label = ctk.CTkLabel(
            info_frame,
            text=settings.APP_MESSAGES["APP_TITLE_SHORT"],
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=(self.colors["texto_header"], self.colors["texto_header"]) # Revertido a texto_header
        )
        title_label.pack(anchor="center", fill="x")

        subtitle_label = ctk.CTkLabel(
            info_frame,
            text=settings.APP_MESSAGES["HEADER_SUBTITLE"],
            font=ctk.CTkFont(size=16, weight="normal"),
            text_color=(self.colors["texto_header"], self.colors["texto_header"]) # Revertido a texto_header
        )
        subtitle_label.pack(anchor="center", fill="x")

        badges_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        badges_frame.pack(anchor="center", pady=(15, 0))

        self.status_badge_label = ctk.CTkLabel(
            badges_frame,
            text=f"{settings.APP_MESSAGES['HEADER_STATUS_LABEL']} {settings.APP_MESSAGES['HEADER_STATUS_NORMAL']}",
            fg_color=(self.colors["exito"], self.colors["exito"]),
            text_color=(self.colors["texto_header"], self.colors["texto_header"]), # Revertido a texto_header
            corner_radius=10,
            padx=10,
            pady=5,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_badge_label.pack(side="left", padx=(0, 10))

    def _add_menu_button(self):
        menu_btn = ctk.CTkButton(
            self,
            text=settings.APP_MESSAGES["MENU_BUTTON_TEXT"],
            width=50,
            height=50,
            corner_radius=25,
            fg_color="transparent",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=(self.colors["texto_header"], self.colors["texto_header"]), # Revertido a texto_header
            command=self._abrir_menu_lateral_callback
        )
        menu_btn.grid(row=0, column=2, sticky="e", padx=20, pady=20)
        menu_btn.bind("<Enter>", lambda e: menu_btn.configure(fg_color=(self.colors["sombra"], self.colors["sombra"]))) # Simple hover
        menu_btn.bind("<Leave>", lambda e: menu_btn.configure(fg_color="transparent")) # Simple leave

    def update_status_badge(self, message, color_level="info"):
        """
        Actualiza el mensaje y color del badge de estado en el encabezado.
        Args:
            message (str): El mensaje a mostrar.
            color_level (str): 'info', 'success', 'warning', 'error' para definir el color.
        """
        badge_colors = {
            "info": (self.colors["info"], self.colors["info"]),
            "success": (self.colors["exito"], self.colors["exito"]),
            "warning": (self.colors["warning"], self.colors["warning"]),
            "error": (self.colors["error"], self.colors["error"])
        }
        self.status_badge_label.configure(
            text=f"{settings.APP_MESSAGES['HEADER_STATUS_LABEL']} {message}",
            fg_color=badge_colors.get(color_level, badge_colors["info"]),
            text_color=(self.colors["texto_header"], self.colors["texto_header"]) # Revertido a texto_header
        )
