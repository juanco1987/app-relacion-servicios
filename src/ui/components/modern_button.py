import customtkinter as ctk
from src.ui.styles.palet_colors import get_colors

class ModernButton(ctk.CTkFrame):
    def __init__(self, master, text="", command=None,
                 height=45,
                 width=None,
                 base_color=None, hover_color=None, text_color=None,
                 font=None, corner_radius=12, icon_image=None, **kwargs):

        colors = get_colors()
        base_color = base_color or colors["primary"]
        hover_color = hover_color or colors["primary_hover"]
        text_color = text_color or colors["texto_boton"]

        frame_kwargs = {
            "master": master,
            "fg_color": "transparent",
            "height": height
        }
        if width is not None:
            frame_kwargs["width"] = width

        super().__init__(**frame_kwargs)
        self.pack_propagate(False)
        self.command = command
        self.base_color = base_color
        self.hover_color = hover_color
        self.base_text_color = text_color
        self.hover_text_color = colors["texto_boton_hover"] if "texto_boton_hover" in colors else "#ffffff"
        self._original_text = text
        self._progress_anim_id = None
        self._leave_check_id = None
        self._animation_id = None

        button_kwargs = {
            "master": self,
            "text": text,
            "image": icon_image,
            "command": self._on_click,
            "fg_color": base_color,
            "hover": False,
            "text_color": text_color,
            "font": font or ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": corner_radius,
            "height": height,
            "cursor": "hand2",
            **kwargs
        }
        if width is not None:
            button_kwargs["width"] = width

        self.button = ctk.CTkButton(**button_kwargs)
        self.button.pack(fill="both", expand=True)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.button.bind("<Enter>", self._on_enter)
        self.button.bind("<Leave>", self._on_leave)

    def _on_click(self):
        if callable(self.command):
            self.command()

    def _on_enter(self, event=None):
        if self._leave_check_id:
            self.after_cancel(self._leave_check_id)
            self._leave_check_id = None
        if self.button.cget("state") == "normal":
            self._animate_color_change(self.button.cget("fg_color"), self.hover_color, 
                                     self.button.cget("text_color"), self.hover_text_color)

    def _on_leave(self, event=None):
        self._leave_check_id = self.after(50, self._check_if_truly_left)

    def _check_if_truly_left(self):
        if not self.winfo_exists(): return
        widget_under_cursor = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
        is_still_over = False
        current_widget = widget_under_cursor
        while current_widget is not None:
            if current_widget == self:
                is_still_over = True; break
            current_widget = current_widget.master
        if not is_still_over and self.button.cget("state") == "normal":
            self._animate_color_change(self.button.cget("fg_color"), self.base_color,
                                     self.button.cget("text_color"), self.base_text_color)
        self._leave_check_id = None

    def _animate_color_change(self, start_color, end_color, start_text_color=None, end_text_color=None, steps=15, delay=10):
        if self._animation_id:
            self.after_cancel(self._animation_id)

        def get_mode_color(color_val):
            if isinstance(color_val, str): return color_val
            if isinstance(color_val, tuple):
                return ctk.get_appearance_mode() == "Dark" and color_val[1] or color_val[0]
            return "#FFFFFF"

        start_color_str = get_mode_color(start_color)
        end_color_str = get_mode_color(end_color)

        # SOLUCIÓN: Manejar colores transparentes
        if start_color_str == "transparent" or end_color_str == "transparent":
            self.button.configure(fg_color=end_color_str)
            if end_text_color:
                self.button.configure(text_color=end_text_color)
            return
        # Manejar animación del texto si se proporcionan colores
        animate_text = start_text_color is not None and end_text_color is not None
        if animate_text:
            start_text_color_str = get_mode_color(start_text_color)
            end_text_color_str = get_mode_color(end_text_color)

        def hex_to_rgb(hex_val):
            return tuple(int(hex_val.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb_tuple):
            # SOLUCIÓN: Asegurarse de que los valores RGB estén siempre entre 0 y 255.
            safe_rgb = [max(0, min(255, int(v))) for v in rgb_tuple]
            return f"#{safe_rgb[0]:02x}{safe_rgb[1]:02x}{safe_rgb[2]:02x}"

        start_rgb, end_rgb = hex_to_rgb(start_color_str), hex_to_rgb(end_color_str)
        delta = [(e - s) for s, e in zip(start_rgb, end_rgb)]
        
        if animate_text:
            start_text_rgb, end_text_rgb = hex_to_rgb(start_text_color_str), hex_to_rgb(end_text_color_str)
            text_delta = [(e - s) for s, e in zip(start_text_rgb, end_text_rgb)]
        
        current_step = 0

        def step_animation():
            nonlocal current_step
            if not self.winfo_exists(): return
            current_step += 1
            progress = current_step / steps 
            # Animar color de fondo
            new_rgb = [start_rgb[i] + progress * delta[i] for i in range(3)]
            self.button.configure(fg_color=rgb_to_hex(new_rgb))
            # Animar color de texto si es necesario
            if animate_text:
                new_text_rgb = [start_text_rgb[i] + progress * text_delta[i] for i in range(3)]
                self.button.configure(text_color=rgb_to_hex(new_text_rgb))
            
            if current_step < steps:
                self._animation_id = self.after(delay, step_animation)
            else:
                self._animation_id = None
        step_animation()

    def set_colors(self, new_base_color=None, new_hover_color=None, new_text_color=None, state=None):
        if new_base_color is not None:
            self.base_color = new_base_color
            self.button.configure(fg_color=self.base_color)
        if new_hover_color is not None:
            self.hover_color = new_hover_color
        if new_text_color is not None:
            self.button.configure(text_color=new_text_color)
        if state is not None:
            self.button.configure(state=state)

    def configure(self, **kwargs):
        if 'text' in kwargs:
            self.button.configure(text=kwargs['text'])
        super().configure(**{k: v for k, v in kwargs.items() if k != 'text'})


    

        
