import flet as ft
from utils.style import *


class EmployeesForm:
    def __init__(self, page, on_success):
        self.page = page
        # self.on_success = on_success

        # фио сотрудника
        self.full_name_input = ft.Container(
            content=ft.TextField(label="Введите ФИО сотрудника",
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor),
            border_radius=15
        )
        # должность
        self.position_input = ft.Container(
            content=ft.TextField(label="Введите должность сотрудника",
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor),
            border_radius=15
        )
        # имя компьютера
        self.comp_name_input = ft.Container(
            content=ft.TextField(
                label="Введите имя компьютера",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor),
            border_radius=15)
    #
    #     # # тип контейнера(токен/реестр) выпадающий список
    #     self.type_ecp_or_token_input = ft.Container(
    #         ft.Dropdown(
    #             label="Выберите из списка токен или реестр",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="token", text="Токен"),
    #                 ft.dropdown.Option(key="reestr", text="Реестр"),
    #             ]
    #         ), border_radius=15)
    #
    #     # тип статус(работает/отозван) выпадающий список
    #     self.license_state_input = ft.Container(
    #         ft.Dropdown(
    #             label="Выберите статус лицензии",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="active", text="Работает"),
    #                 ft.dropdown.Option(key="revoked", text="Отозван"),
    #             ],
    #             value="Работает"
    #         ), border_radius=15)
    #
    #     # место установки
    #     self.install_location_input = ft.Container(
    #         content=ft.TextField(
    #             label="Введите место установки",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor),
    #         border_radius=15)
    #
    #     # где хранится
    #     self.storage_location_input = ft.Container(
    #         content=ft.TextField(
    #             label="Введите место хранения",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor),
    #         border_radius=15)
    #
    #     # дата начала лицензии
    #     self.start_date_input = ft.Container(
    #         content=ft.DatePicker()
    #     )
    #
    #     # дата завершения лицензии
    #     self.finish_date_input = ft.Container(
    #         content=ft.DatePicker()
    #     )
    #
    #     # применим к сбис (да/нет) выпадающий список
    #     self.sbis_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к СБИС",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    #     # применим к ЧЗ (да/нет) выпадающий список
    #     self.cz_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к ЧЗ",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    #     # применим к диадок(да/нет) выпадающий список
    #     self.diadok_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к Диадок",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    #     # применим к фнс(да/нет) выпадающий список
    #     self.fns_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к ФНС",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    #     # применим к отчетности(да/нет) выпадающий список
    #     self.report_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к отчетности",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    #     # Применим к фед. ресурсу(да/нет) выпадающий список
    #     self.fed_resours_input = ft.Container(
    #         ft.Dropdown(
    #             label="Применим к Фед.Ресурсу",
    #             bgcolor=secondaryBgColor,
    #             border=ft.InputBorder.NONE,
    #             filled=True,
    #             color=secondaryFontColor,
    #             options=[
    #                 ft.dropdown.Option(key="yes", text="Да"),
    #                 ft.dropdown.Option(key="no", text="Нет"),
    #             ],
    #         ), border_radius=15)
    #
    # def on_start_date_change(self, e):
    #     self.start_date_input = e.control.value
    #
    # def on_finish_date_change(self, e):
    #     self.finish_date_input = e.control.value
