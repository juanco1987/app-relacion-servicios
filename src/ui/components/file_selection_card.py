# src/ui/components/file_selection_card.py

import customtkinter as ctk
import os
from PIL import Image
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.config import settings
from src.ui.components.modern_button import ModernButton

class FileSelectionCard(ctk.CTkFrame):
    def __init__(self, parent, excel_path_var, select_file_callback, log_message_callback):
        self.colors = get_colors()
        self.excel_path = excel_path_var
        self.select_file_callback = select_file_callback
        self._log_message = log_message_callback

        super().__init__(
            parent,
            corner_radius=15,
            fg_color=(self.colors["card"], self.colors["card"]),
            border_width=1,
            border_color=self.colors["accent"]
        )
        self.pack(fill="x", pady=(0, 20), padx=15)

        self._create_widgets()

    def _create_widgets(self):
        """Crea y organiza los widgets dentro de la tarjeta de selección de archivo."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))

        title_icon_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_icon_container.pack(expand=True) # Para que ocupe el espacio y centre

        try:
            icon_image = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["EXCEL_ICON"])), size=(28, 28))
            icon_label = ctk.CTkLabel(
                title_icon_container, 
                text="",
                image=icon_image,
                font=ctk.CTkFont(size=28)
            )
            icon_label.pack(side="left", padx=(0, 5)) 
        except Exception as e:
            icon_label = ctk.CTkLabel(
                title_icon_container,
                text="📄",
                font=ctk.CTkFont(size=28)
            )
            icon_label.pack(side="left", padx=(0, 5))
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["EXCEL_ICON_WARNING_NAME"], e), "warning")

        title_label = ctk.CTkLabel(
            title_icon_container, 
            text=settings.APP_MESSAGES["FILE_SELECT_TITLE"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(self.colors["accent"], self.colors["accent"])
        )
        title_label.pack(side="left", padx=(5, 0))

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=25, pady=(0, 25))

        self.excel_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.excel_path,
            placeholder_text=settings.APP_MESSAGES["FILE_ENTRY_PLACEHOLDER"],
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=12,
            border_width=2,
            border_color=self.colors["accent"],
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=(self.colors["texto"], self.colors["texto"])
        )
        self.excel_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        try:
            icono_imagen = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["FOLDER_ICON"])), size=(20, 20))
        except Exception as e:
            icono_imagen = None
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["FOLDER_ICON_WARNING_NAME"], e), "warning")

        self.browse_btn = ModernButton(
            input_frame,
            text=settings.APP_MESSAGES["BUTTON_BROWSE_TEXT"],
            icon_image=icono_imagen,
            command=self._trigger_select,
            height=50,
            base_color=self.colors["boton_primario"],
            hover_color=self.colors["boton_primario_hover"],
            text_color=self.colors["texto_header"]
        )
        self.browse_btn.pack(side="right", fill="y", padx=(0,0))

    def _animate_entry_focus(self, event):
        pass

    def _trigger_select(self):
        self.select_file_callback()
        