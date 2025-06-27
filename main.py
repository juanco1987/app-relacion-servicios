import customtkinter as ctk
from src.ui import ModernInformesApp

def main():
    ctk.set_appearance_mode("system")  # system, light, dark
    ctk.set_default_color_theme("blue")  # blue, dark-blue, green
    app = ModernInformesApp()
    app.run()

if __name__ == "__main__":
    main() 