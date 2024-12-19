import flet as ft
from utils.style import *


class KriptoProForm:
    def __init__(self, page, on_success):
        self.page = page
        self.on_success = on_success

        # место установки
        self.install_location_input = ft.Container(
            content=ft.TextField(
                label="Введите место установки",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor),
            border_radius=15)

        self.license_type = ft.Container(
            content=ft.TextField(
                label="Введите тип лицензии",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor
            ),
            border_radius=15
        )


    # дата начала лицензии
        self.start_date_input = ft.Container(
            content=ft.DatePicker()
        )

        # дата завершения лицензии
        self.finish_date_input = ft.Container(
            content=ft.DatePicker()
        )
