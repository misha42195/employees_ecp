from datetime import datetime
import flet as ft
from flet_route import Params, Basket

from utils.style import *
from crud.employees import get_ecp_kriptopro_employee_name


class EmployeesPage:

    def __init__(self, page: ft.Page):
        self.page = page
        self.result_text = ft.Text("", color=ft.Colors.BLACK)

        self.employee_info = ft.ListView(
            controls=[],
            expand=True,
        )

        self.text_add = ft.Text(
            "Получение сотрудника по имени",
            size=18,
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,
        )
        self.employee_full_name_input = (
            ft.Container(
                content=ft.TextField(
                    label="Введите ФИО сотрудника",
                    bgcolor=ft.Colors.GREY_100,
                    width=500,
                    border=ft.InputBorder.NONE,
                    filled=True,
                ),
                border_radius=15,
            )
        )
        self.find_button = ft.ElevatedButton(
            text="Найти сотрудника",
            on_click=self.submit_form,
            tooltip="Поиск сотрудника по ФИО",
            icon=ft.Icons.SEARCH,
            bgcolor="#F5EEE6",
            color=defaultBgColor,
            height=40,
        )

        self.add_ecp_button = ft.ElevatedButton(
            text="Добавить эцп",
            on_click=self.add_ecp_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            icon=ft.Icons.ADD,
            height=40,
            visible=False,
        )

        self.add_kpr_button = ft.ElevatedButton(
            text="Добавить криптопро",
            on_click=self.add_kpr_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            icon=ft.Icons.ADD,
            height=40,
            visible=False,
        )
        self.add_mchd_button = ft.ElevatedButton(
            text="Добавить мчд",
            on_click=self.add_mchd_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            icon=ft.Icons.ADD,
            height=40,
            visible=False,
        )

    def add_mchd_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)
        self.employee_full_name_input.content.value = ""
        self.page.go("/add_mchd")
        self.page.update()

    def add_ecp_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)
        self.employee_full_name_input.content.value = ""
        self.page.go("/add_ecp_find_empl")
        self.page.update()

    def add_kpr_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)
        self.employee_full_name_input.content.value = ""

        self.page.go("/add_kriptopro_find_empl")
        self.page.update()

    def go_home(self):
        self.employee_info.controls = []
        self.result_text.value = ""
        self.employee_full_name_input.content.value = ""
        self.page.update()
        self.page.go("/")

    def submit_form(self, e):
        full_name = self.employee_full_name_input.content.value.strip()
        full_name = full_name.capitalize()
        self.employee_info.controls = []
        self.result_text.value = ""
        self.add_ecp_button.visible = False
        self.add_kpr_button.visible = False
        self.add_mchd_button.visible = False
        self.page.update()
        self.result_text.value = ""

        if not full_name:
            self.result_text.value = "Пожалуйста, введите ФИО."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        try:
            employee = get_ecp_kriptopro_employee_name(full_name=full_name)
            self.result_text.color = ft.Colors.GREEN
            self.add_ecp_button.visible = True
            self.add_kpr_button.visible = True
            self.employee_info.controls.clear()
            self.employee_info.controls.extend(
                [
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Сотрудник:",
                                color=ft.Colors.BLUE_ACCENT_700,
                                size=22,
                                expand=1,
                            ),
                            ft.Text(
                                f"{employee.full_name}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Должность:", color=ft.Colors.BLUE, size=18, expand=1
                            ),
                            ft.Text(
                                f"{employee.position}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Имя компьютера:",
                                color=ft.Colors.BLUE,
                                size=18,
                                expand=1,
                            ),
                            ft.Text(
                                f"{employee.com_name}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "обновить данные",
                                bgcolor=defaultBgColor,
                                tooltip="обновление данных сотрудника",
                                icon=ft.Icons.UPDATE,
                                height=40,
                                on_click=lambda e: self.edit_employee(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "Добавить эцп",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый эцп",
                                on_click=lambda e: self.add_ecp_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "Добавить кпр",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый криптопро",
                                on_click=lambda e: self.add_kpr_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "Добавить мчд",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый мчд",
                                on_click=lambda e: self.add_mchd_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(expand=1, controls=[ft.Text("")]),
                    ft.Divider(color=defaultBgColor),
                ]
            )

            if employee.ecp:
                for ecp_record in employee.ecp:
                    finish_date = ecp_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )

                    self.employee_info.controls.extend(
                        [
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "ЭЦП",
                                        color=ft.Colors.BLUE_ACCENT_700,
                                        size=18,
                                        expand=1,
                                    )
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Тип ЭЦП:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.type_ecp}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Статус ЭЦП:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.status_ecp}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Место установки:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.install_location}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Место хранения:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.storage_location}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к СБИС:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.sbis}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к ЧЗ:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.chz}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к Диадок:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.diadok}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к ФНС:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.fns}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к отчетности:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.report}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к фед.рес:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.fed_resours}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Divider(color=defaultBgColor),
                        ]
                    )

            if employee.kriptos:
                for kriptos_record in employee.kriptos:
                    finish_date = kriptos_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )
                    self.employee_info.controls.extend(
                        [
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "КПР-csp",
                                        color=ft.Colors.BLUE_ACCENT_700,
                                        size=18,
                                        expand=1,
                                    )
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Место установки:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.install_location}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Тип лицензии:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.licens_type}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Версия лицении:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.version}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Divider(color=defaultBgColor),
                        ]
                    )
            if employee.mchd:
                for mchd_record in employee.mchd:
                    finish_date = mchd_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )

                    self.employee_info.controls.extend(
                        [
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "МЧД",
                                        color=ft.Colors.BLUE_ACCENT_700,
                                        size=18,
                                        expand=1,
                                    )
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "Номер доверенноси организации:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{mchd_record.organiazation_dov_num}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Номер доверенности фнс:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{mchd_record.fns_dov_num}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{mchd_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=1,
                                    ),
                                    ft.Text(
                                        f"{mchd_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Divider(color=defaultBgColor),
                        ]
                    )

            self.page.update()

        except ValueError as er:
            self.result_text.value = str(er)
            self.result_text.color = ft.Colors.RED
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Произошла ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

    def clear_page_date(self):
        self.employee_info.controls.clear()
        self.result_text.value = ""
        self.employee_id = None
        self.employee_name = None

    def go_to_add_emploees(self):
        self.text_add.value = ""
        self.employee_full_name_input.content.value = ""
        # self.find_button
        self.result_text.value = ""
        self.employee_info.clean()
        self.page.update()
        self.page.go("/add_employees")

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.clear_page_date()
        page.title = "Поиск сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"

        self.submit_form(e=None)

        style_menu = ft.ButtonStyle(
            color="#FBF0F0",
            icon_size=30,
            text_style=ft.TextStyle(size=16),
            overlay_color=defaultBgColor,
            shadow_color=defaultBgColor,
        )

        # Панель сайдбар
        self.sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=18),
                    ft.TextButton(
                        "Добавить сотрудника",
                        icon=ft.Icons.ADD,
                        style=style_menu,
                        on_click=lambda e: self.go_to_add_emploees(),
                    ),
                ]
            ),
        )

        return ft.View(
            route="/employees",
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(12),
                                        ),
                                        on_click=lambda e: self.go_home(),
                                    ),
                                    self.sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            padding=ft.padding.all(10),
                        ),
                        ft.Container(
                            expand=7,
                            alignment=ft.alignment.bottom_left,
                            padding=ft.padding.Padding(
                                left=40, top=40, right=40, bottom=60
                            ),
                            content=ft.Column(
                                controls=[
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.find_button,
                                    self.result_text,
                                    self.employee_info,
                                ],
                            ),
                            bgcolor=defaultBgColor,
                        ),
                    ],
                ),
            ],
            bgcolor=defaultBgColor,
            padding=0,
            appbar=ft.AppBar(title=ft.Text("Сотрудники с лицензиями")),
        )

    def edit_employee(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.go(f"/update_employees")
        self.page.update()
