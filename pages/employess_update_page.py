import time

import flet as ft

from flet_route import Params, Basket

from crud.employees import update_employee, get_one_employees_with_id
from model import Employee
from utils.style import *


class UpdateEmployeesPage:
    def __init__(self, page: ft.Page):
        self.employee_name = None
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            "Обновление сотрудника",
            color=defaultFontColor,
            size=18,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT
        )

        # Поля ввода для "Сотрудника"
        self.employee_full_name_input = ft.Container(
            content=ft.TextField(
                label="Введите ФИО сотрудника",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500),
            border_radius=15,
        )

        self.employee_position_input = ft.Container(
            content=ft.TextField(
                label="Введите должность",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500),
            border_radius=15,
        )
        self.employee_com_name_input = ft.Container(
            content=ft.TextField(
                label="Введите имя компьютера",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
            width=500),
            border_radius=15,
        )



        self.result_text = ft.Text("", color=ft.Colors.GREEN)


        # Создаем кнопку в методе view, где доступен self
        self.employee_save_button = ft.ElevatedButton(
            text="Сохранить сотрудника",
            on_click=self.submit_form,  # Указываем правильный обработчик
            bgcolor=ft.Colors.BLUE_100,
            # color=defaultFontColor,
        )

    def submit_form(self, e):
        """
        Обработчик кнопки: добавление нового сотрудника.
        """
        full_name = self.employee_full_name_input.content.value.strip()
        position = self.employee_position_input.content.value.strip()
        company = self.employee_com_name_input.content.value.strip()

        # Проверка на заполненность всех полей
        if not (full_name and position and company):
            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return
        else:
            # Вызов функции добавления сотрудника
            try:
                employee_id = self.page.session.get("employee_id")  # получаем сотрудника
                employee: Employee = get_one_employees_with_id(employee_id)
                update_employee(
                    employee_id=employee_id,
                    full_name=full_name,
                    position=position,
                    com_name=company
                )

                self.result_text.color = ft.Colors.GREEN
                self.result_text.value = f"Сотрудник '{full_name}' успешно обновлен!"
                self.page.update()
                time.sleep(2)
                self.result_text.value = ""
                self.employee_full_name_input.content.value = ""
                self.employee_position_input.content.value = ""
                self.employee_com_name_input.content.value = ""

                self.page.go("/")




            except ValueError as er:
                self.employee_full_name_input.content.value = ""
                self.employee_position_input.content.value = ""
                self.employee_com_name_input.content.value = ""

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED
            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

                self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Обновление данных"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600


        employee_id = self.page.session.get("employee_id")  # Получаем ID сотрудника
        employee = get_one_employees_with_id(employee_id)

        self.employee_full_name = ft.Text(
            value=employee.full_name,
            bgcolor=secondaryBgColor,
            color=secondaryFontColor
        )


        style_menu = ft.ButtonStyle(color='#FBF0F0',
                                    icon_size=30,
                                    text_style=ft.TextStyle(size=16),
                                    overlay_color=defaultBgColor,
                                    shadow_color=defaultBgColor,
                                    )

        # Панель сайдбар
        sidebar_menu = ft.Container(

            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=18),
                    ft.TextButton("Поиск сотрудника", icon=ft.Icons.SEARCH, style=style_menu,
                                  on_click=lambda e: self.page.go("/employees")),
                    ft.TextButton("Добавить сотрудника", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_employees")),
                ]
            )
        )
        return ft.View(
            "/update_employees",
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
                                                  on_click=lambda e: self.page.go("/"),
                                                  ),  # Обработчик клика (переход на главную страницу)
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),

                        ),
                        ft.Container(
                            expand=4,
                            # padding=ft.padding.only(20, top=40, right=10, bottom=40),
                            content=ft.Column(
                                # alignment=ft.MainAxisAlignment.START,
                                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[  # Обработчик клика (переход на главную страницу)
                                    self.text_add,
                                    self.employee_full_name,
                                    self.employee_full_name_input,
                                    self.employee_position_input,
                                    self.employee_com_name_input,
                                    self.result_text,

                                    self.employee_save_button, ]
                            ),
                            bgcolor=defaultBgColor,
                            # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),

                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
