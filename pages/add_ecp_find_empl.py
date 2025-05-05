from datetime import datetime

import flet as ft
import time

from flet_route import Params, Basket

from crud.employees import get_one_employees_with_id

from schemas.ecpies import EcpReqestAdd
from utils.style import *
from crud.ecpies import create_ecp


class AddEcpFindEmpl:
    def __init__(self, page: ft.Page):
        self.page = page
        self.employee_full_name = ft.Text(
            size=22,
            bgcolor=secondaryBgColor,
            color=secondaryFontColor
        )

        self.text_add = ft.Text(
            "Добавление эцп сотруднику",
            size=22,
            bgcolor=secondaryBgColor,
            color=secondaryFontColor
        )

        self.type_ecp_or_token_input = ft.Container(
            content=ft.Dropdown(
                label="вид ЭЦП",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="токен", text="токен"),
                    ft.dropdown.Option(key="реестр", text="реестр"),
                ],
            ),
            border_radius=10,
        )

        self.status_ecp_input = ft.Container(
            content=ft.Dropdown(
                label="действующая ЭЦП или отозвана ЭЦП",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="действующая", text="действующая"),
                    ft.dropdown.Option(key="отозван", text="отозван"),
                ],
            ),
            border_radius=15,
        )
        self.install_location_input = ft.Container(
            content=ft.TextField(
                label="введите место установки",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )

        self.storage_location_input = ft.Container(
            content=ft.TextField(
                label="введите место хранения",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )

        self.sbis_input = ft.Container(
            content=ft.Dropdown(
                label="применим к сбис",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ),
            border_radius=15,
        )

        self.cz_input = ft.Container(
            content=ft.Dropdown(
                label="применим к чз",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15,
        )

        self.diadok_input = ft.Container(
            content=ft.Dropdown(
                label="применим к диадок",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15,
        )

        self.fns_input = ft.Container(
            content=ft.Dropdown(
                label="применим к фнс",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15,
        )

        self.report_input = ft.Container(
            content=ft.Dropdown(
                label="применим к отчетности",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15,
        )

        self.fed_resours_input = ft.Container(
            content=ft.Dropdown(
                label="применим к фед.ресурсу",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15,
        )

        self.finish_date_input = ft.Container(
            content=ft.TextField(
                label="дата окончания лицензии (дд.мм.гггг)",
                hint_text="пример: 20.12.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )
        self.start_date_input = ft.Container(
            content=ft.TextField(
                label="дата начала лицензии (дд.мм.гггг)",
                hint_text="пример: 10.10.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )

        self.employee_save_button = ft.ElevatedButton(
            text="сохранить сотрудника",
            on_click=self.submit_form,
            bgcolor=ft.Colors.BLUE_100,
            # color=defaultFontColor,
        )

        self.result_text = ft.Text("", color=ft.Colors.GREEN)

    def get_start_date(self):
        self.finish_date_input = self.finish_date_input
        self.page.update()

    def get_finish_date(self):
        self.start_date_input = self.start_date_input
        self.page.update()

    def go_home(self):
        self.page.controls.clear()
        self.result_text.value = ""
        self.employee_full_name.value = ""
        self.page.go("/")
        self.page.update()

    def submit_form(self, e):
        type_ecp_or_token = self.type_ecp_or_token_input.content.value
        status_ecp = str(self.status_ecp_input.content.value)
        install_location = str(self.install_location_input.content.value).strip()
        storage_location = str(self.storage_location_input.content.value).strip()
        sbis = str(self.sbis_input.content.value)
        chz = str(self.cz_input.content.value)
        diadok = str(self.diadok_input.content.value)
        fns = str(self.fns_input.content.value)
        report = str(self.report_input.content.value)
        fed_resours = str(self.fed_resours_input.content.value)
        start_date = self.start_date_input.content.value
        finish_date = self.finish_date_input.content.value

        if not (
            type_ecp_or_token
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
            self.result_text.color = ft.colors.RED
            self.page.update()
            return

        try:
            start_date = datetime.strptime(
                str(self.start_date_input.content.value).strip(), "%d.%m.%Y"
            ).date()
            finish_date = datetime.strptime(
                str(self.finish_date_input.content.value).strip(), "%d.%m.%Y"
            ).date()
        except ValueError:
            self.result_text.value = "Введите корректную дату."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        if finish_date <= start_date:
            self.result_text.value = "Дата окончания должна быть больше даты начала."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        if finish_date <= datetime.today().date():
            self.result_text.value = (
                "Дата окончания должна быть больше сегодняшней даты."
            )
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        else:
            try:

                employee_id = self.page.session.get("employee_id")
                employee = get_one_employees_with_id(employee_id=employee_id)

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
                    f"сотруднику {employee.full_name} добавлен эцп."
                )
                self.result_text.color = ft.Colors.GREEN
                self.page.update()
                time.sleep(1)
                self.result_text.value = ""
                self.type_ecp_or_token_input.content.value = None
                self.status_ecp_input.content.value = None
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = None
                self.cz_input.content.value = None
                self.diadok_input.content.value = None
                self.fns_input.content.value = None
                self.report_input.content.value = None
                self.fed_resours_input.content.value = None
                self.start_date_input.content.value = None
                self.finish_date_input.content.value = None
                self.page.go("/")
                self.page.session.clear()
                self.page.session.remove("employee_id")
                self.page.session.remove("employee_name")

            except ValueError as er:
                self.type_ecp_or_token_input.content.value = None
                self.status_ecp_input.content.value = None
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = None
                self.cz_input.content.value = None
                self.diadok_input.content.value = None
                self.fns_input.content.value = None
                self.report_input.content.value = None
                self.fed_resours_input.content.value = None
                self.start_date_input.content.value = None
                self.finish_date_input.content.value = None

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED

            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление эцп"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        self.employee_full_name.value = self.page.session.get("employee_name")

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
            "/add_ecp_find_empl",
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                controls=[
                                    ft.TextButton(
                                        "Домой",
                                        icon=ft.Icons.HOME,
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.ControlState.HOVERED: ft.Colors.GREY_100,
                                                ft.ControlState.DEFAULT: ft.Colors.GREY_100,
                                            },
                                            shape=ft.RoundedRectangleBorder(
                                                radius=8
                                            ),
                                            padding=ft.padding.all(
                                                12
                                            ),
                                        ),
                                        on_click=lambda e: self.go_home(),
                                    ),
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            padding=ft.padding.all(10),
                        ),
                        ft.Container(
                            expand=7,
                            content=ft.Column(
                                controls=[
                                    self.text_add,
                                    self.employee_full_name,  # todo вывести имя которому добавляется эцп
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
                                ]
                            ),
                            bgcolor=defaultBgColor,
                            padding=ft.padding.all(10),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
