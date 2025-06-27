# src/ui/components/action_card.py

import customtkinter as ctk
from PIL import Image
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.config import settings 
from src.ui.components.modern_button import ModernButton
from src.utils.animations import button_animate_pulse, button_animate_progress, button_stop_progress_animation

class ActionCard(ctk.CTkFrame):
    """
    Componente de tarjeta (card) para las acciones principales de la aplicación:
    procesar datos, generar PDF y abrir PDF.

    Args:
        parent (ctk.CTkFrame): El widget padre donde se colocará la tarjeta.
        nombre_pdf_var (tk.StringVar): Variable de Tkinter para el nombre del archivo PDF.
        procesar_datos_callback (function): Callback para iniciar el procesamiento de datos.
        generar_pdf_callback (function): Callback para generar el archivo PDF.
        abrir_pdf_callback (function): Callback para abrir el archivo PDF.
        log_message_callback (function): Callback para enviar mensajes al log.
    """
    def __init__(self, parent, nombre_pdf_var, procesar_datos_callback,
                 generar_pdf_callback, abrir_pdf_callback, log_message_callback):
        self.colors = get_colors() 
        self.nombre_pdf = nombre_pdf_var
        self._procesar_datos_callback = procesar_datos_callback
        self._generar_pdf_callback = generar_pdf_callback
        self._abrir_pdf_callback = abrir_pdf_callback
        self._log_message = log_message_callback

        super().__init__(
            parent,
            corner_radius=15,
            fg_color=(self.colors["card"], self.colors["card"]),
            border_width=1,
            border_color=(self.colors["accent"])
        )
        self.pack(fill="x", pady=(0, 20), padx=15)

        self.procesar_btn = None
        self.generar_pdf_btn = None
        self.abrir_pdf_btn = None

        self._create_widgets()
        self.disable_pdf_buttons()

    def _create_widgets(self):
        """Crea y organiza los widgets dentro de la tarjeta de acciones."""
        # Header del card
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        icono_titulo=ctk.CTkImage(
            Image.open(resource_path(settings.RESOURCE_PATHS["ARROW_CLICK_ICON"])), size=(28, 28)
        )         
        title_icon_container= ctk.CTkFrame(header_frame, fg_color="transparent")
        title_icon_container.pack(expand=True)

        icon_label=ctk.CTkLabel(
            title_icon_container,
            text="",
            image=icono_titulo,
            font=ctk.CTkFont(size=28)
        )
        icon_label.pack(side="left", padx=(0, 8))

        title_label = ctk.CTkLabel(
            title_icon_container,
            text=settings.APP_MESSAGES["ACTION_CARD_TITLE"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(self.colors["accent"], self.colors["accent"]),
            corner_radius=15
        )
        title_label.pack(side="left")

        pdf_frame = ctk.CTkFrame(self, fg_color="transparent")
        pdf_frame.pack(fill="x", padx=25, pady=(0, 15))

        icono_subtitulo=ctk.CTkImage(
            Image.open(resource_path(settings.RESOURCE_PATHS["NOTE_PAD_ICON"])), size=(20, 20)
        )

        subtitle_container= ctk.CTkFrame(header_frame,fg_color="transparent")
        subtitle_container.pack(expand=True)

        icon_sub_label= ctk.CTkLabel(
            subtitle_container,
            text="",
            image=icono_subtitulo,
            font=ctk.CTkFont(size=22)
        )
        icon_sub_label.pack(side="left", padx=(0, 6))

        subtitle_label=ctk.CTkLabel(
            subtitle_container,
            text=settings.APP_MESSAGES["PDF_NAME_LABEL"],
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color=self.colors["texto"]
        )
        subtitle_label.pack(side="left")

        self.pdf_entry = ctk.CTkEntry(
            pdf_frame,
            textvariable=self.nombre_pdf,
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_width=2,
            placeholder_text=settings.APP_MESSAGES["PDF_NAME_PLACEHOLDER"],
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"],
            border_color=(self.colors["accent"])
        )
        self.pdf_entry.pack(fill="x")

        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=25, pady=(0, 20))
        actions_frame.grid_columnconfigure((0, 1), weight=1)
        actions_frame.grid_rowconfigure(0, weight=0)
        actions_frame.grid_rowconfigure(1, weight=0)
        # Botón principal: Procesar Datos
        try:
            icon_procesar = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["PROCESS_ICON"])), size=(20, 20))
        except Exception as e:
            icon_procesar = None
            self._log_message(
                settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["PROCESS_ICON_WARNING_NAME"], e),
                "warning"
            )

        self.procesar_btn = ModernButton(
            actions_frame,
            text=settings.APP_MESSAGES["BUTTON_PROCESS_TEXT"],
            icon_image=icon_procesar,
            command=self._procesar_datos_callback,
            base_color=self.colors["boton_primario"],
            hover_color=self.colors["boton_primario_hover"],
            text_color=self.colors["texto_header"],
            height=50,              
            corner_radius=15,
            font=ctk.CTkFont(size=18, weight="bold")  
        )
        self.procesar_btn.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="ew")
        # Botón Generar PDF
        try:
            icon_pdf_gen = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["PDF_GENERATE_ICON"])), size=(20, 20))
        except Exception as e:
            icon_pdf_gen = None
            self._log_message(
                settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["PDF_GENERATE_ICON_WARNING_NAME"], e),
                "warning"
            )

        self.generar_pdf_btn = ModernButton(
            actions_frame,
            text=settings.APP_MESSAGES["BUTTON_GENERATE_PDF_TEXT"],
            icon_image=icon_pdf_gen,
            command=self._generar_pdf_callback,
            base_color=self.colors["boton_primario"],
            hover_color=self.colors["exito_hover"],
            text_color=self.colors["texto_header"],
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12
        )
        self.generar_pdf_btn.grid(row=1, column=0, padx=(0, 4), sticky="ew")
        # Botón Abrir PDF
        try:
            icon_pdf_open = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["PDF_OPEN_ICON"])), size=(20, 20))
        except Exception as e:
            icon_pdf_open = None
            self._log_message(
                settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["PDF_OPEN_ICON_WARNING_NAME"], e),
                "warning"
            )

        self.abrir_pdf_btn = ModernButton(
            actions_frame,
            text=settings.APP_MESSAGES["BUTTON_OPEN_PDF_TEXT"],
            icon_image=icon_pdf_open,
            command=self._abrir_pdf_callback,
            base_color=self.colors["boton_primario"],
            hover_color=self.colors["error_hover"],
            text_color=self.colors["texto_header"],
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12
        )
        self.abrir_pdf_btn.grid(row=1, column=1, padx=(4, 0), sticky="ew")

    def enable_pdf_buttons(self):
        """Habilita los botones de Generar PDF y Abrir PDF con sus colores de animación."""
        if self.generar_pdf_btn:
            self.generar_pdf_btn.set_colors(
                new_base_color=self.colors["boton_primario"],
                new_hover_color=self.colors["exito_hover"],
                new_text_color=self.colors["texto_header"],
                state="normal"
            )
            button_animate_pulse(self.generar_pdf_btn)

        if self.abrir_pdf_btn:
            self.abrir_pdf_btn.set_colors(
                new_base_color=self.colors["boton_primario"],
                new_hover_color=self.colors["error_hover"],
                new_text_color=self.colors["texto_header"],
                state="normal"
            )
            button_animate_pulse(self.abrir_pdf_btn)

    def disable_pdf_buttons(self):
        """Deshabilita los botones de Generar PDF y Abrir PDF con sus colores de animación."""
        if self.generar_pdf_btn:
            self.generar_pdf_btn.set_colors(
                new_base_color=(self.colors["disabled"], self.colors["disabled"]),
                new_hover_color=(self.colors["disabled"], self.colors["disabled"]), # Hover también en sombra
                new_text_color=(self.colors["texto_disabled"], self.colors["texto_disabled"]),
                state="disabled"
            )
        if self.abrir_pdf_btn:
            self.abrir_pdf_btn.set_colors(
                new_base_color=(self.colors["disabled"], self.colors["disabled"]),
                new_hover_color=(self.colors["sombra"], self.colors["sombra"]), # Hover también en sombra
                new_text_color=(self.colors["texto_disabled"], self.colors["texto_disabled"]),
                state="disabled"
            )

    def set_procesar_button_state(self, processing):
        """Configura el texto y estado del botón Procesar Datos con sus colores de animación."""
        if processing:
            self.procesar_btn.set_colors(
                new_base_color=(self.colors["disabled"], self.colors["disabled"]),
                new_hover_color=(self.colors["disabled"], self.colors["disabled"]), # Hover también en sombra
                new_text_color=(self.colors["texto_disabled"], self.colors["texto_disabled"]),
                state="disabled"
            )
            self.procesar_btn.configure(text=settings.APP_MESSAGES["BUTTON_PROCESSING_TEXT"])
            button_animate_progress(self.procesar_btn)  # Inicia la animación de progreso
            self.disable_pdf_buttons() # Asegura que los botones de PDF se deshabiliten también
        else:
            self.procesar_btn.set_colors(
                new_base_color=self.colors["boton_primario"],
                new_hover_color=self.colors["boton_primario_hover"],
                new_text_color=self.colors["texto_header"],
                state="normal"
            )
            self.procesar_btn.configure(text=settings.APP_MESSAGES["BUTTON_PROCESS_TEXT"])
            button_stop_progress_animation(self.procesar_btn)
            
    def enable_generate_pdf_button(self):
        if self.generar_pdf_btn:
            self.generar_pdf_btn.set_colors(
                new_base_color=self.colors["boton_primario"],
                new_hover_color=self.colors["exito_hover"],
                new_text_color=self.colors["texto_header"],
                state="normal"
            )
            button_animate_pulse(self.generar_pdf_btn)

    def enable_open_pdf_button(self):
        if self.abrir_pdf_btn:
            self.abrir_pdf_btn.set_colors(
                new_base_color=self.colors["boton_primario"],
                new_hover_color=self.colors["error_hover"],
                new_text_color=self.colors["texto_header"],
                state="normal"
            )
            button_animate_pulse(self.abrir_pdf_btn)        