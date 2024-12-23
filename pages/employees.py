#
# import flet as ft
# from flet_route import Params, Basket
# from utils import *
# from utils.style import *
# from repositories.employees import EmployeesRepository
# from crud.employees import get_one_with_employees_full_name, add_employee
# from model import Employee
#
#
# class EmployeesPage:
#     def __init__(self, page: ft.Page):
#         self.page = page  # основная страница приложения
#
#         # Элементы интерфейса
#         self.result_text = ft.Text("", color=ft.Colors.BLACK)
#         self.employee_info = ft.Column(
#             controls=[],
#             expand=True
#         )
#
#         self.text_add = ft.Text(
#             "Получение сотрудника по имени",
#             color=defaultFontColor,
#             weight=ft.FontWeight.NORMAL,
#             text_align=ft.TextAlign.LEFT,
#         )
#         self.employee_full_name_input = ft.Container(
#             content=ft.TextField(
#                 label="Введите ФИО сотрудника",
#                 bgcolor=secondaryBgColor,
#                 border=ft.InputBorder.NONE,
#                 filled=True,
#                 color=secondaryFontColor,
#             ),
#             border_radius=15,
#         )
#
#         self.find_button = ft.ElevatedButton(
#             text="Найти сотрудника",
#             on_click=self.submit_form,  # Привязка кнопки к обработчику
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#         )
#     def submit_form(self, e):
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
#
#             # Для отладки: выводим информацию о сотруднике
#             print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")  # Проверка
#
#             self.result_text.value = f"Сотрудник '{employee.full_name}' есть в базе!"
#             self.result_text.color = ft.Colors.GREEN
#
#             # Очистка предыдущего содержимого
#             self.employee_info.controls.clear()
#
#             # Создание таблицы с данными
#             self.employee_info.controls.append(
#                 ft.DataTable(
#                     columns=[
#                         ft.DataColumn(ft.Text("Поле", color=defaultFontColor)),
#                         ft.DataColumn(ft.Text("Значение", color=defaultFontColor)),
#                     ],
#                     rows=[
#
#                         ft.DataRow(cells=[ft.DataCell(ft.Text("ФИО", color=defaultFontColor)), ft.DataCell(ft.Text(employee.full_name, color=defaultFontColor))]),
#                         ft.DataRow(cells=[ft.DataCell(ft.Text("Должность", color=defaultFontColor)), ft.DataCell(ft.Text(employee.position, color=defaultFontColor))]),
#                         ft.DataRow(cells=[ft.DataCell(ft.Text("Имя компьютера", color=defaultFontColor)), ft.DataCell(ft.Text(employee.com_name, color=defaultFontColor))]),
#                     ],
#                     bgcolor=secondaryBgColor,  # Фоновый цвет таблицы
#                     border=ft.Border(
#                         left=ft.BorderSide(1, ft.Colors.BLACK),  # Толщина и цвет левой границы
#                         right=ft.BorderSide(1, ft.Colors.BLACK),  # Толщина и цвет правой границы
#                         top=ft.BorderSide(1, ft.Colors.BLACK),  # Толщина и цвет верхней границы
#                         bottom=ft.BorderSide(1, ft.Colors.BLACK),  # Толщина и цвет нижней границы
#                     ),
#                     expand=True  # Чтобы таблица заполнила доступное пространство
#                 ),
#
#             )
#
#             # Обновляем страницу для отображения новых данных
#             self.page.update()
#
#         except ValueError as er:
#             self.result_text.value = str(er)
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#         except Exception as ex:
#             self.result_text.value = f"Произошла ошибка: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#
#
#     def view(self, page: ft.Page, params: Params, basket: Basket):
#         page.title = "Все сотрудники"
#         page.window.width = defaultWithWindow
#         page.window.height = defaultHeightWindow
#         page.window.min_width = 1000
#         page.window.min_height = 600
#         page.scroll = "adaptive"
#
#         return ft.View(
#             "/",
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
#                                     ft.TextButton(
#                                         "Домой",
#                                         icon=ft.Icons.HOME,
#                                         style=ft.ButtonStyle(
#                                             color={
#                                                 ft.ControlState.HOVERED: ft.Colors.BLUE,  # Цвет при наведении
#                                                 ft.ControlState.DEFAULT: ft.Colors.BLACK,  # Цвет по умолчанию
#                                             },
#                                             shape=ft.RoundedRectangleBorder(radius=8),  # Округлённые углы
#                                             padding=ft.padding.all(3),  # Внутренние отступы
#                                         ),
#                                         on_click=lambda e: self.page.go("/dashboard"),
#                                     ),
#                                     self.text_add,
#                                     self.employee_full_name_input,
#                                     self.find_button,
#                                     self.result_text,
#                                     self.employee_info,  # Добавляем поле для информации о сотруднике
#                                 ],
#                             ),
#                         ),
#                         ft.Container(
#                             expand=4,
#                             #image_src="assets/salavat.jpg",
#                             #image_fit=ft.ImageFit.COVER,
#                             content=self.employee_info,
#                             padding=0,
#                         ),
#
#                     ],
#                 ),
#             ],
#             bgcolor=defaultBgColor,
#             padding=0,
#         )
#
#


import flet as ft
from flet_route import Params, Basket
from utils import *
from utils.style import *
from repositories.employees import EmployeesRepository
from crud.employees import get_one_with_employees_full_name, add_employee
from model import Employee


class EmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.BLACK)
        self.employee_info = ft.ListView(
            controls=[],
            expand=True,
            auto_scroll=True
        )

        self.text_add = ft.Text(
            "Получение сотрудника по имени",
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

        self.find_button = ft.ElevatedButton(
            text="Найти сотрудника",
            on_click=self.submit_form,  # Привязка кнопки к обработчику
            bgcolor=defaultBgColor,
            color=defaultFontColor,
        )

    def submit_form(self, e):
        full_name = self.employee_full_name_input.content.value.strip()
        if not full_name:
            self.result_text.value = "Пожалуйста, введите ФИО."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        try:
            # Получаем данные о сотруднике
            employee = get_one_with_employees_full_name(full_name=full_name)

            # Для отладки: выводим информацию о сотруднике
            print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")

            self.result_text.value = f"Сотрудник '{employee.full_name}' есть в базе!"
            self.result_text.color = ft.Colors.GREEN

            # Очистка предыдущего содержимого
            self.employee_info.controls.clear()

            # Добавляем данные о сотруднике в ListView
            self.employee_info.controls.extend([
                ft.Text(f"ФИО: {employee.full_name}", color=defaultFontColor),
                ft.Text(f"Должность: {employee.position}", color=defaultFontColor),
                ft.Text(f"Имя компьютера: {employee.com_name}", color=defaultFontColor),
                # todo: в зависимости(ecp или kriptopro) у сотрудника будут разные поля
            ])

            # Обновляем страницу для отображения новых данных
            self.page.update()

        except ValueError as er:
            self.result_text.value = str(er)
            self.result_text.color = ft.Colors.RED
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Произошла ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Все сотрудники"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"

        return ft.View(
            "/",
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
                                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(3),
                                        ),
                                        on_click=lambda e: self.page.go("/dashboard"),
                                    ),
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.find_button,
                                    self.result_text,
                                    self.employee_info,  # Добавляем поле для информации о сотруднике
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=4,
                            content=self.employee_info,
                            padding=0,
                        ),

                    ],
                ),
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
