import customtkinter as ctk
import tkinter as tk
import os
import threading
from tkinter import messagebox, filedialog
from datetime import datetime
from src.utils import resource_path
from src.core.excel_processor import extraer_servicios
from src.core.pdf_generator import generar_pdf_modular, _abrir_pdf
from src.ui.components.terminal_componet import create_terminal, add_log_message
from src.ui.styles.palet_colors import get_colors
from src.utils.animations import button_stop_progress_animation
from src.ui.components.header_component import HeaderComponent
from src.ui.components.splash_screen import SplashScreenComponent
from src.ui.components.file_selection_card import FileSelectionCard
from src.ui.components.date_range_card import DateRangeCard
from src.ui.components.notes_card import NotesCard
from src.ui.components.action_card import ActionCard
from src.ui.components.menu_lateral_component import MenuLateralComponent
from src.config import settings

class ModernInformesApp:
    
    def _get_colors(self):
        """Obtener colores según el tema actual"""
        return get_colors()

    def _apply_theme_colors(self, widget):
        """
        Aplicar colores del tema a un widget y sus hijos.
        Este método ha sido revertido para usar las claves de la paleta original.
        """
        colors = self._get_colors()
        
        try:
            if isinstance(widget, ctk.CTkFrame):
                if widget == self.root:
                    self.root.configure(fg_color=(colors["fondo_general"], colors["fondo_general"]))
                elif hasattr(self, 'main_container') and widget == self.main_container:
                    widget.configure(
                        fg_color=(colors["fondo_general"], colors["fondo_general"]), # Revertido a fondo_general
                        border_color=(colors["borde"], colors["borde"])
                    )
                
                elif hasattr(self, 'left_panel') and widget == self.left_panel:
                     widget.configure(
                        fg_color=(colors["card"], colors["card"]),
                        border_color=(colors["borde"], colors["borde"])
                    )
                
                elif "file_card" in str(widget) or \
                     "date_card" in str(widget) or \
                     "notes_card" in str(widget) or \
                     "action_card" in str(widget) or \
                     "menu_frame" in str(widget): 
                    widget.configure(
                        fg_color=(colors["card"], colors["card"]),
                        border_color=(colors["borde"], colors["borde"])
                    )
                # Terminal frame tiene sus colores específicos (console_bg, console_texto)
                elif hasattr(self, 'terminal_frame') and widget == self.terminal_frame:
                     widget.configure(
                        fg_color=(colors["console_bg"], colors["console_bg"]), 
                        border_color=(colors["borde"], colors["borde"]) 
                    )
                elif "header" in str(widget):
                    widget.configure(fg_color=(colors["header"], colors["header"]))
                else:
                    widget.configure(fg_color=(colors["fondo_general"], colors["fondo_general"]))
            
            elif isinstance(widget, ctk.CTkButton):
                
                pass 
            
            elif isinstance(widget, ctk.CTkLabel):
                if hasattr(self, 'header_component') and widget in self.header_component.winfo_children():
                    if widget.cget("text") == settings.APP_MESSAGES["APP_TITLE_SHORT"]: # Título principal del header
                         widget.configure(text_color=(colors["texto_header"], colors["texto_header"])) # Revertido a texto_header
                    elif widget.cget("text") == settings.APP_MESSAGES["HEADER_SUBTITLE"]: # Subtítulo del header
                         widget.configure(text_color=(colors["texto_header"], colors["texto_header"])) # Revertido a texto_header
                    elif "Estado" in widget.cget("text"): # Badge de estado
                        widget.configure(text_color=(colors["texto_header"], colors["texto_header"])) # Revertido a texto_header
                    else: 
                        widget.configure(text_color=(colors["texto"], colors["texto"])) # Revertido a texto general
                else:
                     widget.configure(text_color=(colors["texto"], colors["texto"])) # Texto general
            
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(
                    fg_color=(colors["card"], colors["fondo_general"]), # Revertido a fondo_general para entradas en modo oscuro
                    border_color=(colors["borde"], colors["borde"]),
                    text_color=(colors["texto"], colors["texto"])
                )
            
            elif isinstance(widget, ctk.CTkTextbox):
                
                if hasattr(self, 'log_textbox') and widget == self.log_textbox:
                    widget.configure(
                        fg_color=(colors["console_bg"], colors["console_bg"]), # Revertido a console_bg
                        text_color=(colors["console_texto"], colors["console_texto"]) # Revertido a console_texto
                    )
                else: 
                    widget.configure(
                        fg_color=(colors["card"], colors["fondo_general"]), # Revertido a fondo_general
                        border_color=(colors["borde"], colors["borde"]),
                        text_color=(colors["texto"], colors["texto"])
                    )
            
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(
                    fg_color=(colors["borde"], colors["borde"]),
                    progress_color=(colors["accent"], colors["accent"])
                )
            
            elif isinstance(widget, ctk.CTkComboBox):
                widget.configure(
                    fg_color=(colors["card"], colors["fondo_general"]), # Revertido a fondo_general
                    border_color=(colors["borde"], colors["borde"]),
                    text_color=(colors["texto"], colors["texto"]),
                    button_color=(colors["accent"], colors["accent"]),
                    button_hover_color=(colors["accent_hover"], colors["accent_hover"])
                )
            
            for child in widget.winfo_children():
                self._apply_theme_colors(child)
                
        except Exception as e:
            print(f"Error al aplicar colores a widget {widget}: {e}") 
            pass 

    def _update_theme(self):
        """Actualizar tema de toda la aplicación"""
        try:
            self.colors = self._get_colors() 

            if hasattr(self, 'left_panel'):
                self.left_panel.configure(fg_color=self.colors["card"])

            self._apply_theme_colors(self.root) 
            
            self.root.update_idletasks()
            self.root.update()
            
            self._log_message(settings.APP_MESSAGES["THEME_UPDATED_LOG"], "info")
        except Exception as e:
            print(f"Error al actualizar tema: {e}")

    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.log_textbox = None
        self.colors = self._get_colors() 

        self.side_menu = MenuLateralComponent(self.root, self._cambiar_tema) 

        self.root.title(settings.APP_MESSAGES["APP_TITLE"])
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1200, screen_width)
        window_height = min(800, screen_height)
        self.root.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")
        self.root.minsize(1200, 800)
        
        self.excel_path = tk.StringVar(value="")
        self.fecha_inicio = tk.StringVar()
        self.fecha_fin = tk.StringVar()
        self.notas = tk.StringVar()
        self.nombre_pdf = tk.StringVar(value=settings.PDF_CONFIG["DEFAULT_NAME"])
        self.procesando = False
        self.df_resultado = None
        self._closing = False
        
        hoy = datetime.today()
        primer_dia_mes = datetime(hoy.year, hoy.month, 1)
        self.fecha_inicio.set(primer_dia_mes.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))
        self.fecha_fin.set(hoy.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))
        
        self._setup_window_icon()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self._show_splash_screen = SplashScreenComponent(self.root, self._start_application)
        
    def _start_application(self):
        """Iniciar la aplicación después de la pantalla de carga"""
        try:
            
            self._create_modern_interface()
            self.root.deiconify()
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self._update_theme()
            self.root.update_idletasks()
            self.root.update()
            self._log_message(settings.APP_MESSAGES["APP_STARTED_SUCCESSFULLY"], "success")
  
        except Exception as e:
            print(f"Error al iniciar aplicación: {e}")

    def _setup_window_icon(self):
        """Configurar ícono de la ventana"""
        try:
            icon_path = resource_path(settings.RESOURCE_PATHS["APP_ICON"])
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["APP_ICON_WARNING_NAME"], e))
    
    def _create_modern_interface(self):
        """Crear la interfaz moderna con mejoras visuales, eliminando el degradado del canvas."""
        self.root.configure(fg_color=(self.colors["fondo_general"], self.colors["fondo_general"]))

        self.main_container = ctk.CTkFrame(
            self.root, 
            corner_radius=25,
            fg_color=(self.colors["fondo_general"], self.colors["fondo_general"]), # Revertido a fondo_general
            border_width=1,
            border_color=(self.colors["borde"], self.colors["borde"])
        )
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.main_container.grid_rowconfigure(0, weight=0)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)      
        self.header_component = HeaderComponent(self.main_container, self._show_side_menu)
        self.header_component.grid(row=0, column=0, sticky="ew", padx=25, pady=25)
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent" 
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))
        
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=0, minsize=700)
        self.content_frame.grid_columnconfigure(1, weight=1, minsize=350)        
        self._create_enhanced_left_panel()
        self._create_enhanced_right_panel()

    def _create_enhanced_left_panel(self):
        """Panel izquierdo con diseño de cards modernas"""
        self.left_panel = ctk.CTkScrollableFrame(
            self.content_frame,
            width=700,
            corner_radius=20,
            fg_color=(self.colors["card"], self.colors["card"]), 
            border_width=1,
            border_color=(self.colors["borde"], self.colors["borde"]),
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        self.file_card = FileSelectionCard(
            self.left_panel,
            self.excel_path,
            self._select_excel_file,
            self._log_message
        )
        self.date_card = DateRangeCard(
            self.left_panel,
            self.fecha_inicio,
            self.fecha_fin,
            self._log_message
        )
        self.notes_card = NotesCard(
            self.left_panel,
            self.notas,
            self._log_message
        )
        self.action_card = ActionCard(
            self.left_panel,
            self.nombre_pdf,
            self._procesar_datos_async,
            self._generar_pdf,
            self._abrir_pdf,
            self._log_message
        )

    def _cambiar_tema(self, value):
        """Cambiar el tema de la aplicación"""
        try:
            if value == settings.APP_MESSAGES["THEME_VALUES_CLARO"]:
                ctk.set_appearance_mode("light")
            elif value == settings.APP_MESSAGES["THEME_VALUES_OSCURO"]:
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("system")
            
            self._update_theme()
            self._log_message(settings.APP_MESSAGES["THEME_CHANGED_TO_LOG"].format(value), "info")
        except Exception as e:
            print(f"Error al cambiar tema: {e}")

    def _create_enhanced_right_panel(self):
        """Panel derecho con terminal modular"""
        try:
            self.terminal_frame, self.log_textbox = create_terminal(
                self.content_frame,
                self._clear_log
            )
            self.terminal_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
            
        except Exception as e:
            print(settings.APP_MESSAGES["TERMINAL_CREATE_ERROR"].format(e))
            self.log_textbox = ctk.CTkTextbox(self.content_frame)
            self.log_textbox.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

    def _add_animation_effects(self):
        """Agregar efectos de animación sutiles (Método de ejemplo, no directamente usado en este punto)"""
        def fade_in_widget(widget, delay=0):
            widget.after(delay, lambda: widget.configure(fg_color=widget.cget("fg_color")))
        
        cards = [self.left_panel, self.terminal_frame]
        for i, card in enumerate(cards):
            fade_in_widget(card, i * 100)

    # === MÉTODOS DE FUNCIONALIDAD ===

    def _show_side_menu(self):
        """Mostrar el menú lateral modular."""
        if self.side_menu:
            self.side_menu.show_menu()
    
    def _select_excel_file(self):
        """Seleccionar archivo Excel con diálogo moderno"""
        file_path = filedialog.askopenfilename(
            title=settings.APP_MESSAGES["FILE_SELECT_TITLE"],
            filetypes=settings.APP_MESSAGES["FILE_TYPES"]
        )
        if file_path:
            self.excel_path.set(file_path)
            self._log_message(f"{settings.APP_MESSAGES['FILE_SELECTED']} {os.path.basename(file_path)}", "success")
            self._log_message(f"{settings.APP_MESSAGES['FILE_LOADED']}{os.path.basename(file_path)}", "info")
    
    def _procesar_datos_async(self):
        """Procesar datos de forma asíncrona para no bloquear la UI"""
        if self.procesando:
            return
        
        if not self.excel_path.get():
            self._show_modern_error("Por favor selecciona un archivo Excel")
            return
        
        self.procesando = True
        self._update_processing_state(True)
        
        thread = threading.Thread(target=self._procesar_datos)
        thread.daemon = True
        thread.start()
    
    def _procesar_datos(self):
        try:
            self._log_message(settings.APP_MESSAGES["PROCESS_START"], "info")
            fecha_inicio = datetime.strptime(self.fecha_inicio.get(), settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"])
            fecha_fin = datetime.strptime(self.fecha_fin.get(), settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"])
            self.df_resultado = extraer_servicios(
                self.excel_path.get(),
                fecha_inicio,
                fecha_fin,
                self._log_message
            )
            if self.df_resultado.empty:
                self._log_message(settings.APP_MESSAGES["NO_RECORDS_FOUND"], "warning")
            else:
                self._log_message(settings.APP_MESSAGES["RECORDS_FOUND"].format(len(self.df_resultado)), "success")
                self.root.after(0, lambda: self.action_card.enable_generate_pdf_button())
        except Exception as e:
            self._log_message(f"{settings.APP_MESSAGES['PROCESS_ERROR']} {e}", "error")
            self.root.after(0, lambda: self._show_modern_error(f"{settings.APP_MESSAGES['ERROR_TITLE']}: {e}"))
        finally:
            self.procesando = False
            button_stop_progress_animation(self.action_card.procesar_btn)
            self.root.after(0, lambda: self._update_processing_state(False))
            self._log_message(settings.APP_MESSAGES["PROCESS_COMPLETE"], "success")
    
    def _generar_pdf(self):
        exito, mensaje = generar_pdf_modular(
            self.df_resultado,
            self.nombre_pdf.get(),
            self.notas.get(),
            self.fecha_inicio.get(),
            self.fecha_fin.get(),
            self._log_message
        )
        self.ruta_pdf = settings.get_pdf_output_path(self.nombre_pdf.get())

        if exito:
            self.action_card.enable_open_pdf_button()
        else:
            self._show_modern_error(mensaje)

    def _abrir_pdf(self):
        if hasattr(self, "ruta_pdf") and self.ruta_pdf and os.path.exists(self.ruta_pdf):
            _abrir_pdf(self.ruta_pdf, self._log_message)
        else:
            self._log_message(settings.APP_MESSAGES["PDF_NOT_EXIST"], "error")
    
    # === MÉTODOS DE UI ===
    
    def _log_message(self, message, level="info"):
        """Agregar mensaje al log usando el componente modular (solo consola visual, nunca terminal Python)"""
        try:
            if hasattr(self, 'log_textbox') and self.log_textbox is not None:
                add_log_message(self.log_textbox, message, level)
        except Exception as e:
            print(f"Error en log: {str(e)}")
    
    def _clear_log(self):
        """Limpiar el log"""
        self.log_textbox.delete("1.0", "end")
        self._log_message(settings.APP_MESSAGES["LOG_CLEARED"], "info")
    
    def _update_progress(self, value):
        """Actualizar barra de progreso (este método no está siendo usado activamente)"""
        if hasattr(self, 'progress_bar') and self.progress_bar:
            def update():
                self.progress_bar.set(value)
            self.root.after(0, update)
        else:
            pass
    
    def _update_processing_state(self, processing):
        """Actualizar estado de procesamiento y delegar al action_card."""
        self.action_card.set_procesar_button_state(processing)
    
    def _show_modern_error(self, message):
        """Mostrar error moderno"""
        messagebox.showerror(settings.APP_MESSAGES["ERROR_TITLE"], message)
        self._log_message(f"{settings.APP_MESSAGES['ERROR_MESSAGE_PREFIX']}{message}", "error")
    
    def _on_closing(self):
        """Manejar cierre de aplicación"""
        if messagebox.askyesno(settings.APP_MESSAGES["EXIT_CONFIRM_TITLE"], settings.APP_MESSAGES["EXIT_CONFIRM_MESSAGE"]):
            self._closing = True
            self.root.destroy()

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


    
