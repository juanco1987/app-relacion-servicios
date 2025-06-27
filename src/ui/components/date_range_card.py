# src/ui/components/date_range_card.py

import customtkinter as ctk
from PIL import Image
from datetime import datetime, timedelta
from tkcalendar import Calendar
from src.utils.date_utils import mes_espaniol, fecha_larga
from src.utils import resource_path
from src.ui.styles.palet_colors import get_colors
from src.config import settings
from src.ui.components.modern_button import ModernButton
from src.utils.animations import fade_in, fade_out

class DateRangeCard(ctk.CTkFrame):
    def __init__(self, parent, fecha_inicio_var, fecha_fin_var, log_message_callback):
        self.colors = get_colors()
        self.fecha_inicio = fecha_inicio_var
        self.fecha_fin = fecha_fin_var
        self._log_message = log_message_callback        
        self.calendar_popup = None
        self._calendar = None

        super().__init__(
            parent,
            corner_radius=15,
            fg_color=(self.colors["card"], self.colors["card"]),
            border_width=1,
            border_color=(self.colors["accent"])
        )
        self.pack(fill="x", pady=(0, 20), padx=15)
        self._create_widgets()
        self._set_initial_dates()

    def _create_widgets(self):
        """Crea y organiza los widgets dentro de la tarjeta de rango de fechas."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 20))

        title_icon_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_icon_container.pack(expand=True) # Para que ocupe el espacio y centre
       
        try:
            icon_image = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["CALENDAR_ICON"])), size=(28, 28))
            icon_label = ctk.CTkLabel(
                title_icon_container, 
                text="", 
                image=icon_image,
                font=ctk.CTkFont(size=28)
            )
            icon_label.pack(side="left", padx=(0, 5))
        except Exception as e:
            icon_label = ctk.CTkLabel(title_icon_container, text="📅", font=ctk.CTkFont(size=28))
            icon_label.pack(side="left", padx=(0, 5))
            self._log_message(
                settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["CALENDAR_ICON_WARNING_NAME"], e),
                "warning"
            )

        title_label = ctk.CTkLabel(
            title_icon_container, 
            text=settings.APP_MESSAGES["DATE_RANGE_CARD_TITLE"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(self.colors["accent"], self.colors["accent"])
        )
        title_label.pack(side="left", padx=(5, 0))

        subtitle_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        subtitle_container.pack(fill="x")
        subtitle_inner =ctk.CTkFrame(subtitle_container,fg_color="transparent")
        subtitle_inner.pack(anchor="center")   
        icon_image_subtitle= ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["QUIK_ICON"])), size=(20, 20))

        icon_sub_label = ctk.CTkLabel(
            subtitle_inner,
            text="",
            image=icon_image_subtitle,
            font=ctk.CTkFont(size=22)
        )
        icon_sub_label.pack(side="left", padx=(0,6))

        subtitle_label = ctk.CTkLabel(
            subtitle_inner,
            text=settings.APP_MESSAGES["QUICK_SELECT_LABEL"],
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color=self.colors["texto"]
        )
        subtitle_label.pack(side="left")

        selectors_frame = ctk.CTkFrame(self, fg_color="transparent")
        selectors_frame.pack(fill="x", padx=20, pady=(0, 15))

        month_frame = ctk.CTkFrame(selectors_frame, fg_color="transparent")
        month_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            month_frame, 
            text=settings.APP_MESSAGES["MONTH_LABEL"], 
            font=ctk.CTkFont(size=13, weight="bold"), 
            text_color=self.colors["texto"]
            ).pack(anchor="center")

        self.mes_combo = ctk.CTkComboBox(
            month_frame,
            values=settings.APP_MESSAGES["MONTHS_NAMES"],
            command=self._update_dates_by_month,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=13),
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            justify="center"
        )
        self.mes_combo.pack(fill="x", pady=(5, 0))

        year_frame = ctk.CTkFrame(selectors_frame, fg_color="transparent")
        year_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))

        ctk.CTkLabel(
            year_frame, 
            text=settings.APP_MESSAGES["YEAR_LABEL"], 
            font=ctk.CTkFont(size=13, weight="bold"), 
            text_color=self.colors["texto"]
            ).pack(anchor="center")

        current_year = datetime.today().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        self.anio_combo = ctk.CTkComboBox(
            year_frame,
            values=years,
            command=self._update_dates_by_month,
            width=120,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            justify="center"
        )
        self.anio_combo.pack(fill="x", pady=(5, 0))

        custom_frame = ctk.CTkFrame(self, fg_color="transparent")
        custom_frame.pack(fill="x", padx=25, pady=(0, 25))

        custom_frame.grid_columnconfigure(1, weight=1)
        custom_frame.grid_columnconfigure(3, weight=1)

        try:
            icon_image_inicio = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["CALENDAR_ICON_2"])), size=(20, 20))
        except Exception as e:
            icon_image_inicio = None
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["CALENDAR_ICON_WARNING_NAME"], e), "warning")


        inicio_label = ctk.CTkLabel(
            custom_frame,
            text=settings.APP_MESSAGES["DATE_FROM_LABEL"],
            image=icon_image_inicio,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(self.colors["accent"], self.colors["accent"])
        )
        inicio_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)

        inicio_container = ctk.CTkFrame(custom_frame, fg_color="transparent")
        inicio_container.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=10)
        inicio_container.grid_columnconfigure(0, weight=1)

        self.date_entry_inicio = ctk.CTkEntry(
            inicio_container,
            textvariable=self.fecha_inicio,
            placeholder_text=settings.APP_MESSAGES["DATE_ENTRY_PLACEHOLDER"],
            font=ctk.CTkFont(size=16),
            height=45,
            corner_radius=10,
            border_width=2,
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"],
            border_color=self.colors["accent"],
            justify="center"
        )
        self.date_entry_inicio.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        try:
            icono_imagen_cal_inicio = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["CALENDAR_ICON"])), size=(20, 20))
        except Exception as e:
            icono_imagen_cal_inicio = None
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["CALENDAR_ICON_WARNING_NAME"], e), "warning")


        self.btn_calendar_inicio = ModernButton(
            inicio_container,
            text="",
            icon_image=icono_imagen_cal_inicio,
            command=lambda: self._open_calendar_popup("inicio"),
            height=45,
            width=45,
            font=ctk.CTkFont(size=20),
            corner_radius=10,
            base_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["texto_header"],
        )
        self.btn_calendar_inicio.button.configure(border_width=0)
        self.btn_calendar_inicio.grid(row=0, column=1)
        
        try:
            icon_image_fin = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["CALENDAR_ICON_2"])), size=(20, 20))
        except Exception as e:
            icon_image_fin = None
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["CALENDAR_ICON_WARNING_NAME"], e), "warning")


        fin_label = ctk.CTkLabel(
            custom_frame,
            text=settings.APP_MESSAGES["DATE_TO_LABEL"],
            image=icon_image_fin,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(self.colors["accent"], self.colors["accent"])
        )
        fin_label.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=10)

        fin_container = ctk.CTkFrame(custom_frame, fg_color="transparent")
        fin_container.grid(row=0, column=3, sticky="ew", pady=10)
        fin_container.grid_columnconfigure(0, weight=1)

        self.date_entry_fin = ctk.CTkEntry(
            fin_container,
            textvariable=self.fecha_fin,
            placeholder_text=settings.APP_MESSAGES["DATE_ENTRY_PLACEHOLDER"],
            font=ctk.CTkFont(size=16),
            height=45,
            corner_radius=10,
            border_width=2,
            fg_color=(self.colors["card"], self.colors["fondo_general"]),
            text_color=self.colors["texto"],
            border_color=self.colors["accent"],
            justify="center"
        )
        self.date_entry_fin.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        try:
            icono_imagen_cal_fin = ctk.CTkImage(Image.open(resource_path(settings.RESOURCE_PATHS["CALENDAR_ICON"])), size=(20, 20))
        except Exception as e:
            icono_imagen_cal_fin = None
            self._log_message(settings.APP_MESSAGES["WARNING_ICON_NOT_FOUND"].format(settings.APP_MESSAGES["CALENDAR_ICON_WARNING_NAME"], e), "warning")


        self.btn_calendar_fin = ModernButton(
            fin_container,
            text="",
            icon_image=icono_imagen_cal_fin,
            command=lambda: self._open_calendar_popup("fin"),
            height=45,
            width=45,
            font=ctk.CTkFont(size=20),
            corner_radius=10,
            base_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["texto_header"]
        )
        self.btn_calendar_fin.button.configure(border_width=0)
        self.btn_calendar_fin.grid(row=0, column=1)
        
    def _set_initial_dates(self):
        """Configura las fechas iniciales en los combos y entradas."""
        hoy = datetime.today()
        primer_dia_mes = datetime(hoy.year, hoy.month, 1)

        self.fecha_inicio.set(primer_dia_mes.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))
        self.fecha_fin.set(hoy.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))

        mes_actual = hoy.month - 1
        anio_actual = str(hoy.year)

        if hasattr(self, 'mes_combo'):
            self.mes_combo.set(self.mes_combo.cget("values")[mes_actual])
        if hasattr(self, 'anio_combo'):
            self.anio_combo.set(anio_actual)
        
        self._update_dates_by_month()

    def _update_dates_by_month(self, *args):
        """Actualiza las fechas de inicio y fin basándose en la selección de mes y año."""
        try:
            mes_nombre = self.mes_combo.get()
            meses = settings.APP_MESSAGES["MONTHS_NAMES"]
            mes_idx = meses.index(mes_nombre)
            año = int(self.anio_combo.get())

            primer_dia = datetime(año, mes_idx + 1, 1)

            if mes_idx == 11:
                ultimo_dia = datetime(año + 1, 1, 1) - timedelta(days=1)
            else:
                ultimo_dia = datetime(año, mes_idx + 2, 1) - timedelta(days=1)

            self.fecha_inicio.set(primer_dia.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))
            self.fecha_fin.set(ultimo_dia.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]))

            self._log_message(settings.APP_MESSAGES["DATE_PERIOD_UPDATED"].format(mes_espaniol(primer_dia)), "info")

        except Exception as e:
            self._log_message(f"{settings.APP_MESSAGES['DATE_UPDATE_MONTH_ERROR']} {e}", "error")

    def _open_calendar_popup(self, target_entry):
        """Abre una ventana emergente con un calendario para seleccionar una fecha."""
        if self.calendar_popup and self.calendar_popup.winfo_exists():
            self.calendar_popup.lift()
            return

        self.calendar_popup = ctk.CTkToplevel(self.master)
        self.calendar_popup.title(settings.APP_MESSAGES["CALENDAR_POPUP_TITLE"])
        self.calendar_popup.attributes('-topmost', True)
        self.calendar_popup.transient(self.master)
        self.calendar_popup.attributes('-alpha', 0)
        self.calendar_popup.protocol("WM_DELETE_WINDOW", lambda: fade_out(self.calendar_popup))

        popup_frame = ctk.CTkFrame(self.calendar_popup, corner_radius=10)
        popup_frame.pack(pady=20, padx=20, fill="both", expand=True)

        current_date_str = self.fecha_inicio.get() if target_entry == "inicio" else self.fecha_fin.get()
        try:
            current_date = datetime.strptime(current_date_str, settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"]).date()
        except ValueError:
            current_date = datetime.now().date()

        self._calendar = Calendar(
            popup_frame,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            font='Arial 12',
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )
        self._calendar.pack(pady=10, padx=10)

        btn_confirm = ctk.CTkButton(
            popup_frame,
            text=settings.APP_MESSAGES["CALENDAR_SELECT_BUTTON"],
            command=lambda: self._select_date_from_calendar(target_entry),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=(self.colors["texto_header"], self.colors["texto_header"]),
        )
        btn_confirm.pack(pady=10)
        fade_in(self.calendar_popup)

    def _select_date_from_calendar(self, target_entry):
        """Obtiene la fecha seleccionada del calendario y actualiza la entrada correspondiente."""
        try:
            selected_date_obj = self._calendar.selection_get()
            formatted_date = selected_date_obj.strftime(settings.APP_MESSAGES["DEFAULT_DATE_FORMAT"])

            if target_entry == "inicio":
                self.fecha_inicio.set(formatted_date)
            elif target_entry == "fin":
                self.fecha_fin.set(formatted_date)

            fade_out(self.calendar_popup)
            
            self._log_message(settings.APP_MESSAGES["DATE_SELECTED_FOR"].format(target_entry, fecha_larga(selected_date_obj)), "info")
        except Exception as e:
            self._log_message(f"{settings.APP_MESSAGES['DATE_SELECT_ERROR']} {e}", "error")
            if self.calendar_popup and self.calendar_popup.winfo_exists():
                 fade_out(self.calendar_popup)