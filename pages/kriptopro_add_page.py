import time

import flet as ft
from datetime import datetime

from flet_route import Params, Basket

from crud.employees import get_one_with_employees_full_name
from crud.kriptoproies import create_kriptopro
from model import Employee
from schemas.kriptopro import KriptoproRequestAdd
from utils.style import *


class AddKriptoproPage:
    def __init__(self, page: ft.Page):
        self.page = page

        self.text_add = ft.Text(
            "Добавление криптопро к сотруднику",
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,
        )

        self.employee_name_input = ft.Container(
            content=ft.TextField(
                label="Введите ФИО сотрудника",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.instal_location_input = ft.Container(
            content=ft.TextField(
                label="Введите место установки",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )
        self.licens_type_input = ft.Container(
            content=ft.TextField(
                label="Введите имя компьютера",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
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

    result_text = ft.Text("", color=ft.Colors.BLACK)

    def submit_form(self, e):
        full_name = self.employee_name_input.content.value.strip()
        install_location = self.instal_location_input.content.value.strip()
        licens_type = self.licens_type_input.content.value.strip()
        start_date = datetime.strptime(
            str(self.start_date_input.content.value).strip(), "%d.%m.%Y"
        ).date()
        finish_date = datetime.strptime(
            str(self.finish_date_input.content.value).strip(), "%d.%m.%Y"
        ).date()

        if (
            not full_name
            or not install_location
            or not licens_type
            or not start_date
            or not finish_date
        ):

            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.Colors.RED
        else:
            try:
                employee: Employee = get_one_with_employees_full_name(
                    full_name=full_name
                )
                if employee is None:
                    self.result_text.value = ("Сотрудник не найден в базе данных.\nВедите ФИО сотрудника. или "
                                              "добавьте сотрудника в базу данных.")
                    self.result_text.color = ft.Colors.RED

                print(f"сотрудник в методе submit_form: ", employee)
                create_kriptopro(
                    employees_id=employee.id,
                    kriptopro_data=KriptoproRequestAdd(
                        install_location=install_location,
                        licens_type=licens_type,
                        start_date=start_date,
                        finish_date=finish_date,
                    ),
                )
                self.result_text.color = ft.Colors.GREEN
                self.result_text.value = (
                    f"Сотруднику {employee.full_name} добавлен криптопро."
                )

                self.page.update()
                time.sleep(2)
                self.result_text.value = ""
                self.employee_name_input.content.value = ""
                self.instal_location_input.content.value = ""
                self.licens_type_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""
                self.page.go("/")
                self.page.session.clear()

            except ValueError as er:
                self.employee_name_input.content.value = ""
                self.instal_location_input.content.value = ""
                self.licens_type_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED

            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

                self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление криптопро сотруднику"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        style_menu = ft.ButtonStyle(
            color={ft.ControlState.HOVERED: ft.Colors.WHITE},
            icon_size=20,
            text_style=ft.TextStyle(size=16),
            overlay_color=hoverBgColor,
            shadow_color=hoverBgColor,
        )

        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=20),
                    ft.TextButton(
                        "Добавить нового сотрудника",
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
                    expand=True,
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
                                                ft.ControlState.HOVERED: ft.Colors.BLUE,
                                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(12),
                                        ),
                                        on_click=lambda e: self.page.go("/"),
                                    ),
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
                                    self.employee_name_input,
                                    self.instal_location_input,
                                    self.licens_type_input,
                                    self.start_date_input,
                                    self.finish_date_input,
                                    self.result_text,
                                    self.employee_save_button,
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=4,
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
