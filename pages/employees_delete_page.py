

import flet as ft
from datetime import datetime

from flet_route import Params, Basket

from model import Employee, ECP, KriptoPro, add_instance  # Ваши модели и функции
from utils.style import *


class DeleteEmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения


    # Элементы интерфейса
    text_add = ft.Text("Добавление ECP", color=defaultFontColor,
                       weight=ft.FontWeight.NORMAL,
                       text_align=ft.TextAlign.LEFT
                       )

    # Поля ввода для "ECP"
    employee_full_name_input = ft.Container(
        content=ft.TextField(
            label="Укажите ФИО сотрудника",
            bgcolor=secondaryBgColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
        ),
        border_radius=15,
    )

    employee_position_input = ft.Container(
        content=ft.TextField(
            label="Введите должность",
            bgcolor=secondaryBgColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
        ),
        border_radius=15,
    )
    employee_com_name_input = ft.Container(
        content=ft.TextField(
            label="Введите имя компьютера",
            bgcolor=secondaryBgColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
        ),
        border_radius=15,
    )

    employee_save_button = ft.ElevatedButton(
        text="Сохранить сотрудника",
        # on_click=self.save_employee,
        bgcolor=defaultBgColor,
        color=defaultFontColor,
    )

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Удаление сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        return ft.View(
            "/add",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=2,
                            padding=ft.padding.only(20, top=40, right=10, bottom=40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.TextButton("Домой",
                                                  icon=ft.Icons.HOME,  # Иконка "домой"
                                                  style=ft.ButtonStyle(
                                                      color={ft.ControlState.HOVERED: ft.Colors.BLUE,
                                                             # Цвет при наведении
                                                             ft.ControlState.DEFAULT: ft.Colors.BLACK},
                                                      # Цвет по умолчанию
                                                      shape=ft.RoundedRectangleBorder(radius=8),  # Округлённые углы
                                                      padding=ft.padding.all(12),  # Внутренние отступы
                                                  ),
                                                  on_click=lambda e: self.page.go("/")
                                                  ),  # Обработчик клика (переход на главную страницу)
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.employee_position_input,
                                    self.employee_com_name_input,
                                    self.employee_save_button

                                ]
                            )
                        ),
                        ft.Container(
                            expand=4,
                            image_src="assets/salavat.jpg",
                            image_fit=ft.ImageFit.COVER,
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
