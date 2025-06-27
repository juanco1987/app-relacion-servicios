# src/ui/components/terminal_componet.py
import customtkinter as ctk
from src.ui.styles.palet_colors import get_colors
from datetime import datetime
from src.utils import resource_path
from PIL import Image
from src.config import settings
from src.ui.components.modern_button import ModernButton

def create_terminal(parent, clear_callback):
    """Crea y devuelve el componente de terminal con todas sus partes."""
    colors = get_colors()

    terminal_frame = ctk.CTkFrame(
        parent,
        corner_radius=12,
        fg_color=(colors["console_bg"], colors["console_bg"]), 
        border_width=2,
        border_color=colors["accent"]
    )
    terminal_frame.grid_rowconfigure(1, weight=1)
    terminal_frame.grid_columnconfigure(0, weight=1)
    
    terminal_header = ctk.CTkFrame(
        terminal_frame,
        height=60,
        corner_radius=12,
        fg_color="transparent" 
    )
    terminal_header.grid(row=0, column=0, sticky="ew", padx=3, pady=(3, 0))
    terminal_header.grid_propagate(False)
    
    buttons_frame = ctk.CTkFrame(terminal_header, fg_color="transparent")
    buttons_frame.pack(side="left", padx=15, pady=15)
    
    for color in [("#ff5f57", "#ff5f57"), ("#ffbd2e", "#ffbd2e"), ("#28ca42", "#28ca42")]:
        btn = ctk.CTkButton(
            buttons_frame,
            text=" ",
            width=15,
            height=15,
            corner_radius=8,
            fg_color=color,
            hover_color=color
        )
        btn.pack(side="left", padx=2)
    
    try:
        icon_image = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["TERMINAL_ICON"])), size=(20, 20))
    except Exception as e:
        icon_image = None
        print(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["TERMINAL_ICON_WARNING_NAME"], e))

    title_label = ctk.CTkLabel(
        terminal_header,
        text=settings.APP_MESSAGES["TERMINAL_TITLE"],
        image=icon_image,
        compound="left",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=(colors["accent"], colors["accent"]),
        padx=8
    )
    title_label.pack(expand=True)
    
    log_frame = ctk.CTkFrame(
        terminal_frame,
        fg_color="transparent",  
        border_width=2,
        corner_radius=12
    )
    log_frame.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    
    font_size = 13 if ctk.get_appearance_mode().lower() == "ligth" else 14

    log_textbox = ctk.CTkTextbox(
        log_frame,
        font=ctk.CTkFont(family="JetBrains Mono", size=font_size),
        corner_radius=0,
        fg_color=(colors["console_bg"], colors["console_bg"]), 
        text_color=colors["console_texto"], 
        scrollbar_button_color=(colors["accent"], colors["accent"]),
        scrollbar_button_hover_color=(colors["accent_hover"], colors["accent_hover"])
    )
    log_textbox.grid(row=0, column=0, sticky="nsew")
    log_textbox.tag_config("info", foreground=colors["info"])
    log_textbox.tag_config("success", foreground=colors["exito"])
    log_textbox.tag_config("error", foreground=colors["error"])
    log_textbox.tag_config("warning", foreground=colors["warning"])
    
    control_frame = ctk.CTkFrame(
        terminal_frame,
        height=50,
        fg_color=(colors["console_bg"], colors["console_bg"]), 
        corner_radius=12,
    )
    control_frame.grid(row=2, column=0, sticky="ew", padx=3, pady=(0, 3))
    control_frame.grid_propagate(False)
    
    try:
        clear_icon = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["TRASH_ICON"])), size=(20, 20))
    except Exception as e:
        clear_icon = None
        print(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["TRASH_ICON_WARNING_NAME"], e))

    clear_btn = ModernButton(
        control_frame,
        text=settings.APP_MESSAGES["BUTTON_CLEAR_TEXT"],
        icon_image=clear_icon,
        command=clear_callback,
        height=35,
        font=ctk.CTkFont(size=12, weight="bold"),
        corner_radius=8,
        base_color="#f8f9fa",
        hover_color=colors["accent_hover"],
        text_color=colors["accent"],
    )
    clear_btn.button.configure(border_width=1, border_color=colors["accent"])
    clear_btn.pack(side="right", padx=10, pady=7.5)
    
    status_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
    status_frame.pack(side="left", padx=15, pady=7.5)
    
    try:
        status_icon = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["TERMINAL_STATUS_ICON"])), size=(20, 20))
    except Exception as e:
        status_icon = None
        print(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["TERMINAL_STATUS_ICON_WARNING_NAME"], e))
    
    terminal_status = ctk.CTkLabel(
        status_frame,
        text=settings.APP_MESSAGES["TERMINAL_STATUS_ONLINE"],
        image=status_icon,
        compound="left",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=(colors["exito"], colors["exito"])
    )
    terminal_status.pack()
    
    welcome_messages = [
        settings.APP_MESSAGES["WELCOME_MESSAGE_1"],
        settings.APP_MESSAGES["WELCOME_MESSAGE_2"],
        settings.APP_MESSAGES["WELCOME_MESSAGE_3"],
        settings.APP_MESSAGES["WELCOME_MESSAGE_4"],
        settings.APP_MESSAGES["WELCOME_MESSAGE_5"],
        settings.APP_MESSAGES["WELCOME_MESSAGE_6"],
    ]
    
    for msg in welcome_messages:
        add_log_message(log_textbox, msg, "success")
    
    return terminal_frame, log_textbox

def add_log_message(log_textbox, message, level="info"):
    """Agrega un mensaje al log de la terminal."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    icons = {
        "info": settings.APP_MESSAGES["LOG_ICON_INFO"],
        "success": settings.APP_MESSAGES["LOG_ICON_SUCCESS"],
        "error": settings.APP_MESSAGES["LOG_ICON_ERROR"],
        "warning": settings.APP_MESSAGES["LOG_ICON_WARNING"]
    }
    
    formatted_message = f"[{timestamp}] {icons.get(level, '')} {message}\n"
    
    log_textbox.insert("end", formatted_message, level)
    log_textbox.see("end")
    
    

