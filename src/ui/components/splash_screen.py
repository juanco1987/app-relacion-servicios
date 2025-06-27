# src/ui/components/splash_screen.py

import customtkinter as ctk
from PIL import Image
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.utils.animations import animate_progress_bar
from src.config import settings

class SplashScreenComponent(ctk.CTkToplevel):
    def __init__(self, parent, on_splash_complete):
        super().__init__(parent)
        self.parent = parent
        self._on_splash_complete = on_splash_complete
        self.colors = get_colors()
        self.overrideredirect(True)
        self.geometry(self._get_centered_geometry(500, 350))
        self.lift()
        self.attributes('-topmost', True)
        self.resizable(False, False)
        self._create_widgets()
        self._animate_loading_messages() 

    def _get_centered_geometry(self, width, height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        return f"{width}x{height}+{x}+{y}"

    def _create_widgets(self):
        self.frame = ctk.CTkFrame(
            self,
            fg_color=(self.colors["card"], self.colors["card"]), 
            corner_radius=20,
            border_width=2,
            border_color=self.colors["accent"]
        )
        self.frame.pack(expand=True, fill="both", padx=15, pady=15)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        try:
            logo_path = resource_path(settings.RESOURCE_PATHS["HEADER_LOGO"])
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(150, 150))
            logo_label = ctk.CTkLabel(self.frame, image=logo_image, text="")
            logo_label.grid(row=0, column=0, pady=(20, 0))
        except Exception as e:
            logo_label = ctk.CTkLabel(self.frame, text="🚀", font=ctk.CTkFont(size=80))
            logo_label.grid(row=0, column=0, pady=(20, 0))
            print(settings.APP_MESSAGES["WARNING_LOGO_NOT_FOUND"].format(logo_path))

        title_label = ctk.CTkLabel(
            self.frame,
            text=settings.APP_MESSAGES["APP_TITLE"],
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=(self.colors["header"], self.colors["header"])
        )
        title_label.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        subtitle_label = ctk.CTkLabel(
            self.frame,
            text=settings.APP_MESSAGES["HEADER_SUBTITLE"], 
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color=(self.colors["texto"], self.colors["texto"]) 
        )
        subtitle_label.grid(row=2, column=0, pady=(0, 20))

        self.loading_message_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(self.colors["texto_header"], self.colors["texto_header"])
        )
        self.loading_message_label.grid(row=4, column=0, pady=(0, 20))

        self.progress_bar = ctk.CTkProgressBar(
            self.frame,
            mode="determinate",
            height=10,
            corner_radius=5,
            progress_color=self.colors["accent"],
            fg_color=self.colors["sombra"]
        )
        self.progress_bar.grid(row=3, column=0, sticky="ew", padx=50, pady=(0, 10))
        self.progress_bar.set(0)

    def _animate_loading_messages(self):
        """Anima una secuencia de mensajes de carga de forma segura en el hilo principal."""
        messages = [
            settings.APP_MESSAGES["LOADING_APP"],
            settings.APP_MESSAGES["LOADING_SYSTEM"],
            settings.APP_MESSAGES["LOADING_COMPONENTS"],
            settings.APP_MESSAGES["LOADING_INTERFACE"],
            settings.APP_MESSAGES["LOADING_SERVICES"],
            settings.APP_MESSAGES["READY_TO_WORK"]
        ]
        total = len(messages)

        def on_complete():
            self.after(300, self.destroy)
            self._on_splash_complete()
        animate_progress_bar(self.progress_bar, steps=total, delay=700, on_complete=on_complete)    
        
        def animate_step(index):
            if index < total:
                msg = messages[index]
                self.loading_message_label.configure(text=msg)
                if index > 0 :
                    self.loading_message_label.configure(text_color=self.colors["accent"])
                    self.after(100, lambda: self.loading_message_label.configure(text_color=self.colors["texto_header"]))
                self.after(700, animate_step, index + 1)
        self.after(100, animate_step, 0)      
