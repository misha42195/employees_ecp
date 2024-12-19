#
# import flet as ft
# from flet_route import Params, Basket
# from typing_extensions import Container
#
# from utils.persons import Employee
# from utils.style import *
# from utils.save_in_pkl import save_person_to_file, load_persons_from_file
#
# # Загружаем сотрудников из файла
# # persons = load_persons_from_file()
#
#
# class AddEmployeesPage:
#     persons = load_persons_from_file()
#
#     def __init__(self, page):
#         self.page: ft.Page = page  # основная страница приложения
#         self.selected_date = None
#
#         # Поля ввода данных сотрудника
#         self.full_name_input = ft.Container(
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
#         self.position_input = ft.Container(
#             content=ft.TextField(
#                 label="Введите должность сотрудника",
#                 bgcolor=secondaryBgColor,
#                 border=ft.InputBorder.NONE,
#                 filled=True,
#                 color=secondaryFontColor,
#             ),
#             border_radius=15,
#         )
#
#         self.comp_name_input = ft.Container(
#             content=ft.TextField(
#                 label="Введите имя компьютера",
#                 bgcolor=secondaryBgColor,
#                 border=ft.InputBorder.NONE,
#                 filled=True,
#                 color=secondaryFontColor,
#             ),
#             border_radius=15,
#         )
#
#         # Кнопка сохранения
#         self.save_button = ft.ElevatedButton(
#             text="Сохранение сотрудника",
#             on_click=self.save_employee,  # Передаем метод, не вызывая его
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#         )
#
#
#
#
#     def display_all_employees(self, e):
#         """Показывает всех сотрудников, сохраненных в словаре."""
#         self.page.controls.append(self.display_employees())
#         self.page.update()
#
#
#     def display_employees(self):
#         """Отображает список сотрудников."""
#         employee_list = ft.Column()  # Создаем колонку для отображения данных
#         for employee in self.persons.values():  # Итерируемся по значениям словаря (объекты Employee)
#             employee_list.controls.append(
#                 ft.Text(f"ФИО: {employee.full_name}, Должность: {employee.position}, Компьютер: {employee.com_name}")
#             )
#         return employee_list
#
#     def save_employee(self, e):
#         """Сохраняет нового сотрудника в словарь persons и файл pickle."""
#
#         full_name = self.full_name_input.content.value
#         position = self.position_input.content.value
#         com_name = self.comp_name_input.content.value
#
#         print(f"ПОЛНОЕ ИМЯ СОТРУДНИКА: {full_name}, Position: {position}, Computer Name: {com_name}")  # Для отладки
#         print(self.persons)
#
#         if full_name and position and com_name:
#             if full_name in self.persons:
#                 self.page.snack_bar = ft.SnackBar(
#                     content=ft.Text(f"Сотрудник с именем {full_name} уже существует!"),
#                     bgcolor="orange",
#                 )
#             else:
#                 # Создание объекта сотрудника
#                 new_employee = Employee(full_name=full_name, position=position, com_name=com_name)
#                 print(f"сотрудник {new_employee}")
#                 self.persons[full_name] = new_employee  # Добавляем сотрудника в словарь
#
#                 # Сохранить обновленный список сотрудников в файл
#                 save_person_to_file()  # Сохраняем данные в файл pickle
#
#                 self.page.snack_bar = ft.SnackBar(
#                     content=ft.Text(f"Сотрудник {full_name} успешно добавлен!"),
#                     bgcolor="green",
#                 )
#         else:
#             self.page.snack_bar = ft.SnackBar(
#                 content=ft.Text("Заполните все поля перед сохранением."),
#                 bgcolor="red",
#             )
#
#         self.page.snack_bar.open = True  # Отображение SnackBar
#         self.page.update()
#
#
#     def view(self, page: ft.Page, params: Params, basket: Basket):
#         """Отображение страницы добавления сотрудников."""
#         page.title = "Добавление сотрудников"
#         return ft.View(
#             "/add",
#             controls=[
#                 ft.Row(
#                     expand=True,
#                     controls=[
#                         ft.Container(
#                             expand=2,
#                             padding=ft.padding.all(40),
#                             content=ft.Column(
#                                 alignment=ft.MainAxisAlignment.START,
#                                 horizontal_alignment=ft.CrossAxisAlignment.START,
#                                 controls=[
#                                     ft.IconButton(
#                                         icon=ft.Icons.HOME,
#                                         on_click=lambda e: page.go("/"),
#                                         bgcolor=secondaryBgColor,
#                                     ),
#                                     ft.Text(
#                                         "Введите данные сотрудника",
#                                         color=defaultFontColor,
#                                         weight=ft.FontWeight.NORMAL,
#                                     ),
#                                     self.full_name_input,
#                                     self.position_input,
#                                     self.comp_name_input,
#                                     self.save_button,  # Добавляем кнопку в интерфейс
#                                     self.display_employees(),
#                                 ],
#                             ),
#                         ),
#                     ],
#                 ),
#             ],
#             bgcolor=defaultBgColor,
#             padding=0,
#         )
#


import flet as ft
from datetime import datetime

from flet_route import Params, Basket

from model import Employee, ECP, KriptoPro, add_instance  # Ваши модели и функции
from utils.style import *


class AddEmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения


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

    employee_save_button = ft.ElevatedButton(
        text="Сохранить сотрудника",
        # on_click=self.save_employee,
        bgcolor=defaultBgColor,
        color=defaultFontColor,
    )

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление сотрудников"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400

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

        #         self.employee_full_name_input,
        #         self.employee_position_input,
        #         self.employee_com_name_input,
        #         self.employee_save_button # todo сделать кнопку
        #     ]
        # )


"""       # Поля ввода для "ЭЦП"
        self.ecp_type_input = ft.Container(
            content=ft.TextField(
                label="Тип ЭЦП (токен/реестр)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_status_input = ft.Container(
            content=ft.TextField(
                label="Статус ЭЦП (работает/отозван)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_install_location_input = ft.Container(
            content=ft.TextField(
                label="Место установки",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_storage_location_input = ft.Container(
            content=ft.TextField(
                label="Где хранится",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_start_date_input = ft.Container(
            content=ft.TextField(
                label="Дата начала лицензии (гггг-мм-дд)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_finish_date_input = ft.Container(
            content=ft.TextField(
                label="Дата окончания лицензии (гггг-мм-дд)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.ecp_save_button = ft.ElevatedButton(
            text="Сохранить ЭЦП",
            on_click=self.save_ecp,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
        )

        # Поля ввода для "КриптоПро"
        self.kripto_install_location_input = ft.Container(
            content=ft.TextField(
                label="Место установки",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.kripto_license_type_input = ft.Container(
            content=ft.TextField(
                label="Тип лицензии",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.kripto_start_date_input = ft.Container(
            content=ft.TextField(
                label="Дата начала лицензии (гггг-мм-дд)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.kripto_finish_date_input = ft.Container(
            content=ft.TextField(
                label="Дата окончания лицензии (гггг-мм-дд)",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.kripto_save_button = ft.ElevatedButton(
            text="Сохранить КриптоПро",
            on_click=self.save_kriptopro,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
        )

    def save_employee(self, e):
        full_name = self.employee_full_name_input.content.value
        position = self.employee_position_input.content.value
        com_name = self.employee_com_name_input.content.value
        if full_name and position and com_name:
            employee = Employee(full_name=full_name, position=position, com_name=com_name)
            add_instance(employee)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Сотрудник {full_name} успешно добавлен!"),
                bgcolor="green",
            )
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Заполните все поля перед сохранением."),
                bgcolor="red",
            )
        self.page.snack_bar.open = True
        self.page.update()

    def save_ecp(self, e):
        ecp_type = self.ecp_type_input.content.value
        status = self.ecp_status_input.content.value
        install_location = self.ecp_install_location_input.content.value
        storage_location = self.ecp_storage_location_input.content.value
        start_date = self.ecp_start_date_input.content.value
        finish_date = self.ecp_finish_date_input.content.value

        if all([ecp_type, status, install_location, storage_location, start_date, finish_date]):
            try:
                ecp = ECP(
                    ecp_type=ecp_type,
                    status=status,
                    install_location=install_location,
                    storage_location=storage_location,
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    finish_date=datetime.strptime(finish_date, "%Y-%m-%d").date(),
                )
                add_instance(ecp)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("ЭЦП успешно добавлен!"),
                    bgcolor="green",
                )
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Неверный формат даты. Используйте ГГГГ-ММ-ДД."),
                    bgcolor="red",
                )
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Заполните все поля перед сохранением."),
                bgcolor="red",
            )
        self.page.snack_bar.open = True
        self.page.update()

    def save_kriptopro(self, e):
        install_location = self.kripto_install_location_input.content.value
        license_type = self.kripto_license_type_input.content.value
        start_date = self.kripto_start_date_input.content.value
        finish_date = self.kripto_finish_date_input.content.value

        if all([install_location, license_type, start_date, finish_date]):
            try:
                kriptopro = KriptoPro(
                    install_location=install_location,
                    license_type=license_type,
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    finish_date=datetime.strptime(finish_date, "%Y-%m-%d").date(),
                )
                add_instance(kriptopro)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("КриптоПро успешно добавлен!"),
                    bgcolor="green",
                )
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Неверный формат даты. Используйте ГГГГ-ММ-ДД."),
                    bgcolor="red",
                )
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Заполните все поля перед сохранением."),
                bgcolor="red",
            )
        self.page.snack_bar.open = True
        self.page.update()

    def view(self, page: ft.Page, params, basket):
        return ft.View(
            "/add",
            controls=[
                ft.Container(
                    padding=ft.padding.all(40),
                    content=ft.Column(
                        controls=[
                            ft.Text("Добавить сотрудника"),
                            self.employee_full_name_input,
                            self.employee_position_input,
                            self.employee_com_name_input,
                            self.employee_save_button,
                            ft.Divider(),
                            ft.Text("Добавить ЭЦП"),
                            self.ecp_type_input,
                            self.ecp_status_input,
                            self.ecp_install_location_input,
                            self.ecp_storage_location_input,
                            self.ecp_start_date_input,
                            self.ecp_finish_date_input,
                            self.ecp_save_button,
                            self.kripto_install_location_input,
                            self.kripto_license_type_input,
                            self.kripto_start_date_input,
                            self.kripto_finish_date_input,
                            self.kripto_save_button, ]))])
"""
