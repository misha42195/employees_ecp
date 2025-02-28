import time

import flet as ft


from flet_route import Params, Basket

from crud.employees import add_employee
from model import Employee
from utils.style import *


class AddEmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            "Добавление сотрудника",
            size=18,
            color=defaultFontColor,
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
                # color=secondaryFontColor,
                width=500,
            ),
            border_radius=15,
        )

        self.employee_position_input = ft.Container(
            content=ft.TextField(
                label="Введите должность",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                #color=secondaryFontColor,
                width=500,
            ),
            border_radius=15,
        )

        self.employee_com_name_input = ft.Container(
            content=ft.TextField(
                label="Введите имя компьютера",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                # color=secondaryFontColor,
                width=500,
            ),
            border_radius=15,
        )

        # Создаем кнопку в методе view, где доступен self
        self.employee_save_button = ft.FilledButton(
            "Сохранить сотрудника",
            icon="save",
            on_click=self.submit_form,  # Указываем правильный обработчик
            bgcolor='#F5EEE6',
            color =defaultBgColor,
            height=40
        )

    result_text = ft.Text("")

    def submit_form(self, e):
        """
        Обработчик кнопки: добавление нового сотрудника.
        """
        full_name = self.employee_full_name_input.content.value.strip()
        position = self.employee_position_input.content.value.strip()
        company = self.employee_com_name_input.content.value.strip()

        # Проверка на заполненность всех полей
        if not full_name or not position or not company:
            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.Colors.RED
        else:
            # Вызов функции добавления сотрудника
            try:
                add_employee(Employee(full_name=full_name, position=position, com_name=company))
                self.result_text.color = ft.Colors.GREEN
                self.result_text.value = f"Сотрудник '{full_name}' успешно добавлен!"
                self.page.update()
                time.sleep(2)
                self.page.go("/")

                self.result_text.value = ""
                # Обнуляем поля формы
                self.employee_full_name_input.content.value = ""
                self.employee_position_input.content.value = ""
                self.employee_com_name_input.content.value = ""



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


    # Элементы интерфейса
    text_add = ft.Text("Добавление сотрудника", color=defaultFontColor,
                       weight=ft.FontWeight.NORMAL,
                       text_align=ft.TextAlign.LEFT
                       )

    # Поля ввода для "Сотрудника"
    employee_full_name_input = ft.Container(
        content=ft.TextField(
            label="Введите ФИО сотрудника",
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




    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600




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
            "/add",
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
                            #padding=ft.padding.only(20, top=40, right=10, bottom=40),
                            content=ft.Column(
                                # alignment=ft.MainAxisAlignment.START,
                                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[  # Обработчик клика (переход на главную страницу)
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.employee_position_input,
                                    self.employee_com_name_input,
                                    self.result_text,

                                    self.employee_save_button,]
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
