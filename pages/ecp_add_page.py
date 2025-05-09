from datetime import datetime

import flet as ft
import time
from flet_route import Params, Basket

from crud.employees import get_one_with_employees_full_name
from model import Employee
from schemas.ecpies import EcpReqestAdd
from utils.style import *
from crud.ecpies import create_ecp


class AddEcpPage:

    def __init__(self, page: ft.Page):
        self.page = page

        self.text_add = ft.Text(
            "Добавление ECP",
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,
        )
        self.employee_full_name_input = ft.Container(
            content=ft.TextField(
                label="Введите ФИО сотрудника",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.type_ecp_or_token_input = ft.Container(
            ft.Dropdown(
                label="Выберите из списка токен или реестр",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Токен", text="Токен"),
                    ft.dropdown.Option(key="Реестр", text="Реестр"),
                ],
            ),
            border_radius=15,
        )

        self.status_ecp_input = ft.Container(
            ft.Dropdown(
                label="Выберите из списка работает или отозван",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Работает", text="Работает"),
                    ft.dropdown.Option(key="Отозван", text="Отозван"),
                ],
            ),
            border_radius=15,
        )

        self.install_location_input = ft.Container(
            content=ft.TextField(
                label="Введите место установки",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.storage_location_input = ft.Container(
            content=ft.TextField(
                label="Введите место хранения",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.sbis_input = ft.Container(
            ft.Dropdown(
                label="Применим к СБИС",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.cz_input = ft.Container(
            ft.Dropdown(
                label="Применим к ЧЗ",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.diadok_input = ft.Container(
            ft.Dropdown(
                label="Применим к Диадок",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.fns_input = ft.Container(
            ft.Dropdown(
                label="Применим к ФНС",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.report_input = ft.Container(
            ft.Dropdown(
                label="Применим к отчетности",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.fed_resours_input = ft.Container(
            ft.Dropdown(
                label="Применим к Фед.Ресурсу",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                options=[
                    ft.dropdown.Option(key="Да", text="Да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.start_date_input = ft.Container(
            content=ft.TextField(
                label="Введите дату (дд.мм.гггг)",
                hint_text="Например: 21.12.2024",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )
        self.finish_date_input = ft.Container(
            content=ft.TextField(
                label="Введите дату (дд.мм.гггг)",
                hint_text="Например: 21.12.2024",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.employee_save_button = ft.ElevatedButton(
            text="Сохранить сотрудника",
            on_click=self.submit_form,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
        )

        self.result_text = ft.Text("")

    def submit_form(self, e):

        employees = self.employee_full_name_input.content.value.strip()
        type_ecp_or_token = self.type_ecp_or_token_input.content.value.strip()
        status_ecp = str(self.status_ecp_input.content.value).strip()
        install_location = str(self.install_location_input.content.value).strip()
        storage_location = str(self.storage_location_input.content.value).strip()
        sbis = str(self.sbis_input.content.value).strip()
        chz = str(self.cz_input.content.value).strip()
        diadok = str(self.diadok_input.content.value).strip()
        fns = str(self.fns_input.content.value).strip()
        report = str(self.report_input.content.value).strip()
        fed_resours = str(self.fed_resours_input.content.value).strip()
        start_date = datetime.strptime(
            str(self.start_date_input.content.value).strip(), "%d.%m.%Y"
        ).date()
        finish_date = datetime.strptime(
            str(self.finish_date_input.content.value).strip(), "%d.%m.%Y"
        ).date()

        if not (
            employees
            and type_ecp_or_token
            and status_ecp
            and install_location
            and storage_location
            and sbis
            and chz
            and diadok
            and fns
            and report
            and fed_resours
            and start_date
            and finish_date
        ):
            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.Colors.RED
        else:
            try:

                employee: Employee = get_one_with_employees_full_name(
                    full_name=employees
                )
                if employee is None:
                    self.result_text.value = "Сотрудник не найден в базе данных.\nВедите ФИО сотрудника. или добавьте сотрудника в базу данных."
                    self.result_text.color = ft.Colors.RED

                print(f"сотрудник в методе submit_form: ", employee)
                create_ecp(
                    employees_id=employee.id,
                    ecp_data=EcpReqestAdd(
                        type_ecp=type_ecp_or_token,
                        status_ecp=status_ecp,
                        install_location=install_location,
                        storage_location=storage_location,
                        sbis=sbis,
                        chz=chz,
                        diadok=diadok,
                        fns=fns,
                        report=report,
                        fed_resours=fed_resours,
                        start_date=start_date,
                        finish_date=finish_date,
                    ),
                )
                self.result_text.value = (
                    f"Сотруднику {employee.full_name} добавлен ECP."
                )
                self.result_text.color = ft.Colors.GREEN
                self.page.update()
                time.sleep(2)
                self.result_text.value = ""
                self.employee_full_name_input.content.value = ""
                self.type_ecp_or_token_input.content.value = ""
                self.status_ecp_input.content.value = ""
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = ""
                self.cz_input.content.value = ""
                self.diadok_input.content.value = ""
                self.fns_input.content.value = ""
                self.report_input.content.value = ""
                self.fed_resours_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""
                self.page.go("/")
                self.page.session.clear()

            except ValueError as er:

                self.employee_full_name_input.content.value = ""
                self.type_ecp_or_token_input.content.value = ""
                self.status_ecp_input.content.value = ""
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = ""
                self.cz_input.content.value = ""
                self.diadok_input.content.value = ""
                self.fns_input.content.value = ""
                self.report_input.content.value = ""
                self.fed_resours_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED

            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        style_menu = ft.ButtonStyle(
            color="#FBF0F0",
            icon_size=30,
            text_style=ft.TextStyle(size=16),
            overlay_color=defaultBgColor,
            shadow_color=defaultBgColor,
        )

        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=18),
                    ft.TextButton(
                        "Поиск сотрудника",
                        icon=ft.Icons.SEARCH,
                        style=style_menu,
                        on_click=lambda e: self.page.go("/employees"),
                    ),
                    ft.TextButton(
                        "Добавить сотрудника",
                        icon=ft.Icons.ADD,
                        style=style_menu,
                        on_click=lambda e: self.page.go("/add_employees"),
                    ),
                ]
            ),
        )

        return ft.View(
            "/add",
            controls=[
                ft.Row(
                    expand=2,
                    controls=[
                        # левая сторона
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                controls=[
                                    ft.TextButton(
                                        "Домой",
                                        icon=ft.Icons.HOME,
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.ControlState.HOVERED: ft.Colors.BLUE,
                                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                            },
                                            shape=ft.RoundedRectangleBorder(
                                                radius=8
                                            ),
                                            padding=ft.padding.all(
                                                12
                                            ),
                                        ),
                                        on_click=lambda e: self.page.go("/"),
                                    ),
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                        ),
                        ft.Container(
                            expand=7,
                            padding=ft.padding.only(20, top=40, right=10, bottom=40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.type_ecp_or_token_input,
                                    self.status_ecp_input,
                                    self.install_location_input,
                                    self.storage_location_input,
                                    self.sbis_input,
                                    self.cz_input,
                                    self.diadok_input,
                                    self.fns_input,
                                    self.report_input,
                                    self.fed_resours_input,
                                    self.start_date_input,
                                    self.finish_date_input,
                                    self.result_text,
                                    self.employee_save_button,
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=5,
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
