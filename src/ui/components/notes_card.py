# src/ui/components/notes_card.py

import customtkinter as ctk
from PIL import Image
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.config import settings
from src.utils.animations import animate_pulse

class NotesCard(ctk.CTkFrame):
    """
    Componente de tarjeta (card) para ingresar notas del informe.

    Args:
        parent (ctk.CTkFrame): El widget padre donde se colocará la tarjeta.
        notes_var (tk.StringVar): Variable de Tkinter para almacenar el texto de las notas.
        log_message_callback (function): Función de callback para enviar mensajes al log.
    """
    def __init__(self, parent, notes_var, log_message_callback):
        self.colors = get_colors()
        self.notes_var = notes_var
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
        """Crea y organiza los widgets dentro de la tarjeta de notas."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))

        title_icon_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_icon_container.pack(expand=True) 
        try:
            icon_image = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["NOTES_ICON"])), size=(28, 28))
            icon_label = ctk.CTkLabel(
                title_icon_container, 
                text="",
                image=icon_image,
                font=ctk.CTkFont(size=28)
            )
            icon_label.pack(side="left", padx=(0, 5)) 
        except Exception as e:
            icon_label = ctk.CTkLabel(title_icon_container, text="📝", font=ctk.CTkFont(size=28))
            icon_label.pack(side="left", padx=(0, 5))
            self._log_message(
                settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["NOTES_ICON_WARNING_NAME"], e),
                "warning"
            )

        title_label = ctk.CTkLabel(
            title_icon_container, 
            text=settings.APP_MESSAGES["NOTES_CARD_TITLE"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(self.colors["warning"], self.colors["warning"])
        )
        title_label.pack(side="left", padx=(5, 0)) 

        self.notes_textbox = ctk.CTkTextbox(
            self,
            height=120,
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_width=2,
            border_color=self.colors["accent"],
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"]
        )
        self.notes_textbox.pack(fill="x", padx=25, pady=(0, 25))
        self.notes_textbox.bind("<KeyRelease>", self._on_notes_change)
        if self.notes_var.get():
            self.notes_textbox.insert("1.0", self.notes_var.get())
        self.notes_textbox.bind("<FocusIn>", self._animate_focus) 

    def _animate_focus(self, event):
         animate_pulse(self.notes_textbox, "border_color", self.colors["accent"])       

    def _on_notes_change(self, event=None):
        """Actualiza la StringVar `notes_var` cuando el texto del textbox cambia."""
        self.notes_var.set(self.notes_textbox.get("1.0", "end-1c"))
