#
#
# import flet as ft
# from datetime import datetime
#
# from flet_route import Params, Basket
#
# from crud.employees import delete_employee, get_one_with_employees_full_name
# from model import Employee, ECP, KriptoPro, add_instance  # Ваши модели и функции
# from utils.style import *
#
#
# class DeleteEmployeesPage:
#     def __init__(self, page: ft.Page):
#         self.page = page  # основная страница приложения
#
#
#         # Элементы интерфейса
#         self.text_add = ft.Text("Удаление сотрудника", color=defaultFontColor,
#                            weight=ft.FontWeight.NORMAL,
#                            text_align=ft.TextAlign.LEFT
#                            )
#
#         # Поля ввода для "ECP"
#         self.employee_full_name_input = ft.Container(
#             content=ft.TextField(
#                 label="Укажите ФИО сотрудника",
#                 bgcolor=secondaryBgColor,
#                 border=ft.InputBorder.NONE,
#                 filled=True,
#                 color=secondaryFontColor,
#             ),
#             border_radius=15,
#         )
#
#         # Кнопка проверки сотрудника
#         self.check_employee_button = ft.ElevatedButton(
#             text="Проверить сотрудника",
#             on_click=self.check_employee,
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#         )
#
#         # Кнопка удаления сотрудника (скрыта до проверки)
#         self.delete_employee_button = ft.ElevatedButton(
#             text="Удалить сотрудника",
#             on_click=self.delete_employee,
#             bgcolor=defaultBgColor,
#             color=ft.Colors.RED,
#             visible=False  # Скрываем кнопку до проверки
#         )
#
#
#
#         self.result_text = ft.Text("")
#         self.subbmit_button = ft.ElevatedButton(
#             text="Удалить сотрудника",
#             on_click=self.delete_button,
#             bgcolor=defaultBgColor,
#             color=defaultFontColor
#         )
#     # Функция проверки сотрудника
#     def check_employee(self, e):
#         full_name = self.employee_full_name_input.content.value.strip()
#         if not full_name:
#             self.result_text.value = "Пожалуйста, введите ФИО."
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#             return
#
#         try:
#             # Получаем данные о сотруднике
#             employee = get_one_with_employees_full_name(full_name=full_name)
#             self.result_text.value = f"Найден сотрудник: {employee.full_name}. Нажмите 'Удалить', чтобы подтвердить."
#             self.result_text.color = ft.Colors.GREEN
#             self.delete_employee_button.visible = True  # Показываем кнопку удаления
#             self.page.update()
#         except ValueError as ve:
#             self.result_text.value = str(ve)
#             self.result_text.color = ft.Colors.RED
#             self.delete_employee_button.visible = False  # Скрываем кнопку удаления
#             self.page.update()
#         except Exception as ex:
#             self.result_text.value = f"Ошибка: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.delete_employee_button.visible = False  # Скрываем кнопку удаления
#             self.page.update()
#
#     # Функция удаления сотрудника
#     def delete_employee(self, e):
#         full_name = self.employee_full_name_input.content.value.strip()
#         try:
#             full_name = self.employee_full_name_input.content.value.strip()
#             employees = get_one_with_employees_full_name(full_name=full_name)
#             delete_employee(employee_id=employees.id)  # Удаляем сотрудника
#             self.result_text.value = f"Сотрудник {full_name} успешно удалён."
#             self.result_text.color = ft.Colors.GREEN
#             self.delete_employee_button.visible = False  # Скрываем кнопку удаления
#             self.page.update()
#         except Exception as ex:
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#
#
#     def delete_button(self, e):
#         full_name = self.employee_full_name_input.content.value.strip()
#
#
#
#     def view(self, page: ft.Page, params: Params, basket: Basket):
#         page.title = "Удаление сотрудника"
#         page.window.width = defaultWithWindow
#         page.window.height = defaultHeightWindow
#         page.window.min_width = 1000
#         page.window.min_height = 600
#
#         return ft.View(
#             "/add",
#             controls=[
#                 ft.Row(
#                     expand=True,
#                     controls=[
#                         ft.Container(
#                             expand=2,
#                             padding=ft.padding.only(20, top=40, right=10, bottom=40),
#                             content=ft.Column(
#                                 alignment=ft.MainAxisAlignment.START,
#                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                                 controls=[
#                                     ft.TextButton("Домой",
#                                                   icon=ft.Icons.HOME,  # Иконка "домой"
#                                                   style=ft.ButtonStyle(
#                                                       color={ft.ControlState.HOVERED: ft.Colors.BLUE,
#                                                              # Цвет при наведении
#                                                              ft.ControlState.DEFAULT: ft.Colors.BLACK},
#                                                       # Цвет по умолчанию
#                                                       shape=ft.RoundedRectangleBorder(radius=8),  # Округлённые углы
#                                                       padding=ft.padding.all(12),  # Внутренние отступы
#                                                   ),
#                                                   on_click=lambda e: self.page.go("/")
#                                                   ),  # Обработчик клика (переход на главную страницу)
#                                     self.text_add,
#                                     self.employee_full_name_input,
#                                     self.check_employee_button,
#                                     self.delete_employee_button,
#                                     self.result_text
#                                 ]
#                             )
#                         ),
#                         ft.Container(
#                             expand=4,
#                             image_src="assets/salavat.jpg",
#                             image_fit=ft.ImageFit.COVER,
#                         )
#                     ]
#                 )
#             ],
#             bgcolor=defaultBgColor,
#             padding=0,
#         )
#
#


import flet as ft
from flet_route import Params, Basket

from crud.employees import delete_employee, get_one_with_employees_full_name  # Импорт методов работы с базой данных
from utils.style import *  # Стили и настройки

class DeleteEmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # Главная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            "Удаление сотрудника",
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT
        )

        # Поле ввода для ФИО сотрудника
        self.employee_full_name_input = ft.Container(
            content=ft.TextField(
                label="Укажите ФИО сотрудника",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        # Кнопка проверки сотрудника
        self.check_employee_button = ft.ElevatedButton(
            text="Проверить сотрудника",
            on_click=self.check_employee,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
        )

        # Кнопка удаления сотрудника (скрыта до проверки)
        self.delete_employee_button = ft.ElevatedButton(
            text="Удалить сотрудника",
            on_click=self.delete_employee,
            bgcolor=defaultBgColor,
            color=ft.Colors.RED,
            visible=False  # Скрываем кнопку до проверки
        )

        # Текст для отображения результата
        self.result_text = ft.Text("")
        self.found_employee = None


    # Функция проверки сотрудника
    def check_employee(self, e):
        full_name = self.employee_full_name_input.content.value.strip()
        if not full_name:
            self.result_text.value = "Пожалуйста, введите ФИО."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        try:
            # Получаем данные о сотруднике
            self.found_employee = get_one_with_employees_full_name(full_name=full_name)
            self.result_text.value = f"Найден сотрудник: {self.found_employee.full_name}. Нажмите 'Удалить', чтобы подтвердить."
            self.result_text.color = ft.Colors.GREEN
            self.delete_employee_button.visible = True  # Показываем кнопку удаления
            self.page.update()
        except ValueError as ve:
            self.result_text.value = str(ve)
            self.result_text.color = ft.Colors.RED
            self.delete_employee_button.visible = False  # Скрываем кнопку удаления
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.delete_employee_button.visible = False  # Скрываем кнопку удаления
            self.page.update()

    # Функция удаления сотрудника
    def delete_employee(self, e):
        if not self.found_employee:
            self.result_text.value = "Сотрудник не найден. Пожалуйста, выполните проверку."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        try:
            # Переменная для хранения найденного сотрудника
            employee_id = self.found_employee.id
            # Удаляем сотрудника
            delete_employee(employee_id=employee_id)
            self.result_text.value = f"Сотрудник {self.found_employee.full_name} успешно удалён."
            self.result_text.color = ft.Colors.GREEN
            self.delete_employee_button.visible = False  # Скрываем кнопку удаления
            self.employee_full_name_input.content.value = ""
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

    # Метод для отображения страницы
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Удаление сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        return ft.View(
            "/delete_employee",  # Исправленный маршрут
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
                                    ft.TextButton(
                                        "Домой",
                                        icon=ft.Icons.HOME,
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.ControlState.HOVERED: ft.Colors.BLUE,
                                                ft.ControlState.DEFAULT: ft.Colors.BLACK
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(12),
                                        ),
                                        on_click=lambda e: self.page.go("/")
                                    ),
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.check_employee_button,
                                    self.delete_employee_button,
                                    self.result_text,
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
