import time
from datetime import datetime
from math import ceil

import flet as ft
from flet_route import Params, Basket

from crud.ecpies import delete_ecp
from utils.style import *
from crud.employees import get_ecp_kriptopro_employee_name


class EmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения
        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.BLACK)

        self.employee_info = ft.ListView(  # контейнер для отображения сотрудника
            controls=[],
            expand=True,
        )

        self.text_add = ft.Text(
            "Получение сотрудника по имени",
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,

        )
        self.employee_full_name_input = ft.Container(  # в объекте хранится значения имения для поиска в базе
            content=ft.TextField(
                label="Введите ФИО сотрудника",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.find_button = ft.ElevatedButton(  # кнопка запускает метод submit_form
            text="Найти сотрудника",
            on_click=self.submit_form,  # Привязка кнопки к обработчику
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
        )

        self.add_ecp_button = ft.ElevatedButton(
            text="Добавить эцп",
            on_click=self.add_ecp_page,  # переход на страницу добавлния эцп
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
            visible=False,
        )

        self.add_kpr_button = ft.ElevatedButton(
            text="Добавить криптопро",
            on_click=self.add_kpr_page,  # переход на страницу добавлния кпр
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
            visible=False
        )

        # переход на страницу добавления эцп

    def add_ecp_page(self, employee_id, employee_name):
        print(employee_id)
        print(employee_name)

        self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
        self.page.session.set("employee_name", employee_name)  # установка имени для вывода на странице добавления
        # self.page.go(f"/update_employees?employee_id={employee_id}")
        self.page.go(f"/add_ecp_find_empl")
        self.page.update()

    # переход на страницу добавлния криптопро
    def add_kpr_page(self, employee_id, employee_name):
        print(employee_id)
        print(employee_name)

        self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
        self.page.session.set("employee_name", employee_name)

        # self.page.go(f"/update_employees?employee_id={employee_id}")
        self.page.go(f"/add_kriptopro_find_empl")
        self.page.update()

    def submit_form(self, e):
        full_name = self.employee_full_name_input.content.value.strip()
        full_name = full_name.capitalize()
        print(full_name)

        # Очистка предыдущего содержимого
        self.employee_info.controls.clear()
        self.result_text.value = ""
        self.add_ecp_button.visible = False
        self.add_kpr_button.visible = False
        self.page.update()  # Обновляем страницу сразу после очистки

        self.employee_info.controls.clear()
        self.result_text.value = ""

        if not full_name:
            self.result_text.value = "Пожалуйста, введите ФИО."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        try:
            # Получаем данные о сотруднике
            employee = get_ecp_kriptopro_employee_name(full_name=full_name)

            # Для отладки: выводим информацию о сотруднике
            print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")

            # self.result_text.value = f"Сотрудник '{employee.full_name}' есть в базе!"
            self.result_text.color = ft.Colors.GREEN
            self.add_ecp_button.visible = True
            self.add_kpr_button.visible = True
            # Очистка предыдущего содержимого
            self.employee_info.controls.clear()

            # Добавляем данные о сотруднике в ListView
            self.employee_info.controls.extend([
                ft.Row(
                    controls=[
                        ft.Text(f"Сотрудник:              ", color=ft.Colors.BLUE, size=22, ),
                        ft.Text(f"{employee.full_name}", color=defaultFontColor, size=18)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Должность:                    ", color=ft.Colors.BLUE, size=18, ),
                        ft.Text(f"{employee.position}", color=defaultFontColor, size=18)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Имя компьютера:         ", color=ft.Colors.BLUE, size=18, ),
                        ft.Text(f"{employee.com_name}", color=defaultFontColor, size=18)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Добавить эцп",
                            bgcolor=ft.Colors.BLUE_100,
                            tooltip="Добавить новый эцп",
                            on_click=lambda e: self.add_ecp_page(
                                employee_id=employee.id, employee_name=employee.full_name
                            ),
                        )
                        # self.add_ecp_button,
                    ]),
                ft.Row(controls=[
                    # self.add_kpr_button
                    ft.ElevatedButton(
                        text="Добавить криптопро",
                        tooltip="Добавить новый криптопро",
                        bgcolor=ft.Colors.BLUE_100,
                        on_click=lambda e: self.add_kpr_page(
                            employee_id=employee.id, employee_name=employee.full_name
                        ),
                    ),
                ]),

                ft.Divider(color=defaultBgColor),
            ])

            # Добавляем связанные данные (ecp и kriptos)
            if employee.ecp:
                for ecp_record in employee.ecp:
                    finish_date = ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
                                                                              datetime) else ecp_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                    self.employee_info.controls.extend([
                        ft.Row(
                            controls=[
                                ft.Text(f"ЭЦП:                                  ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.type_ecp}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Статус ЭЦП:                    ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.status_ecp}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Место установки:         ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.install_location}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Место хранения:          ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.storage_location}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к СБИС:               ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.sbis}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к ЧЗ:                     ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.chz}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к Диадок:           ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.diadok}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к ФНС:                 ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.fns}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к отчетности:   ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.report}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к фед.рес:          ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.fed_resours}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата начала:                 ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.start_date}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата окончания:         ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{ecp_record.finish_date}", color=finish_date_color, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Divider(color=defaultBgColor),
                    ])

            if employee.kriptos:
                for kriptos_record in employee.kriptos:
                    finish_date = kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date, datetime) \
                        else kriptos_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                    self.employee_info.controls.extend([
                        ft.Row(
                            controls=[
                                ft.Text(f"Криптопро:                    ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{kriptos_record.install_location}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Тип лицензии:               ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{kriptos_record.licens_type}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата начала:                  ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{kriptos_record.start_date}", color=defaultFontColor, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата окончания:          ", color=ft.Colors.BLUE, size=18, ),
                                ft.Text(f"{kriptos_record.finish_date}", color=finish_date_color, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Divider(color=defaultBgColor),
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
        page.title = "Поиск сотрудника"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"

        self.submit_form(None)

        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.Colors.WHITE},
                                    icon_size=20,
                                    text_style=ft.TextStyle(size=16),
                                    overlay_color=hoverBgColor,
                                    shadow_color=hoverBgColor,
                                    )

        # Панель сайдбар
        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=12),
                    # ft.TextButton("Поиск сотрудника", icon=ft.Icons.SEARCH, style=style_menu,
                    #               on_click=lambda e: self.page.go("/employees")),
                    ft.TextButton("Добавить сотрудника", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_employees")),
                    # ft.TextButton("Добавить ЕЦП", icon=ft.Icons.ADD, style=style_menu,
                    #               on_click=lambda e: self.page.go("/add_ecp")),
                    # ft.TextButton("Добавить Крипто ПРО", icon=ft.Icons.ADD, style=style_menu,
                    #               on_click=lambda e: self.page.go("/add_crypto")),
                    # ft.TextButton("Удалить сотрудника", icon=ft.Icons.DELETE, style=style_menu,
                    #              on_click=lambda e: self.page.go("/delete_employees")),
                ]
            )
        )

        return ft.View(
            "/employees",
            controls=[
                ft.Row(
                    expand=True,
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
                            bgcolor=secondaryBgColor

                        ),
                        ft.Container(
                            expand=4,
                            padding=ft.padding.only(20, top=40, right=10, bottom=40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.text_add,
                                    self.employee_full_name_input,
                                    self.find_button,
                                    self.result_text,
                                    self.employee_info,  # Добавляем поле для информации о сотруднике
                                ],
                            ),
                        ),
                    ],
                ),
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )

#
# import time
# from datetime import datetime
#
# import flet as ft
# from flet_route import Params, Basket
#
# from crud.ecpies import delete_ecp
# from crud.employees import get_one_employee_with_relation  # Импорт методов работы с базой данных
# from crud.kriptoproies import delete_kpr
# from utils.style import *  # Стили и настройки
#
#
# class EmployeesPage:
#     def __init__(self, page: ft.Page):
#         self.page = page  # Главная страница приложения
#
#         # Элементы интерфейса
#         self.text_add = ft.Text(
#             f"Данные сотрудника",
#             color=defaultFontColor,
#             size=18,
#             text_align=ft.TextAlign.LEFT
#         )
#
#         self.add_ecp_button = ft.ElevatedButton(
#             text="Добавить эцп",
#             on_click=self.add_ecp_page,  # переход на страницу добавлния эцп
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#             height=40,
#             # visible=False,
#         )
#
#         self.add_kpr_button = ft.ElevatedButton(
#             text="Добавить криптопро",
#             on_click=self.add_kpr_page,  # переход на страницу добавлния кпр
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#             height=0,
#             # visible=False
#         )
#
#         self.employee_info_right = ft.ListView(
#             controls=[],
#             height=100,
#             expand=True,
#             divider_thickness=True,
#             padding=ft.Padding(left=10, top=10, right=10, bottom=10),
#         )
#
#         self.employee_info_left = ft.ListView(
#             controls=[],
#             divider_thickness=True,
#             height=100,
#             padding=ft.Padding(left=0, top=0, right=0, bottom=0),
#         )
#
#
#         self.result_text = ft.Text("", color=ft.Colors.BLACK)
#
#     def go_home(self):
#         self.page.go("/")
#         self.employee_info_left.controls.clear()
#         self.employee_info_right.controls.clear()
#         self.page.update()
#
#     def add_ecp_page(self, employee_id, employee_name):
#         print(employee_id)
#         print(employee_name)
#
#         self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
#         self.page.session.set("employee_name", employee_name)  # установка имени для вывода на странице добавления
#         # self.page.go(f"/update_employees?employee_id={employee_id}")
#         self.page.go(f"/add_ecp_find_empl")
#         self.page.update()
#
#     # переход на страницу добавлния криптопро
#     def add_kpr_page(self, employee_id, employee_name):
#         print(employee_id)
#         print(employee_name)
#
#         self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
#         self.page.session.set("employee_name", employee_name)
#
#         # self.page.go(f"/update_employees?employee_id={employee_id}")
#         self.page.go(f"/add_kriptopro_find_empl")
#         self.page.update()
#
#     def delete_ecp_(self, ecp_id):
#         try:
#             print(f'delete_===', ecp_id)
#             print(f"Удаление с ID: {ecp_id}")
#
#             delete_ecp(ecp_id)  # Вызываем функцию удаления
#
#             # Успешное завершение
#             self.result_text.value = f"ЭЦП успешно удален."
#             self.result_text.color = ft.Colors.GREEN
#             self.page.update()
#         except Exception as ex:
#             print(f"Ошибка при удалении ЭЦП: {str(ex)}")
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#         # Обновляем форму после завершения
#         self.submit_form()
#
#     def delete_kpr_(self, kpr_id):
#         try:
#             print(f'delete_===', kpr_id)
#             print(f"Удаление с ID: {kpr_id}")
#
#             delete_kpr(kpr_id)  # Вызываем функцию удаления
#
#             # Успешное завершение
#             self.result_text.value = f"КПР успешно удален."
#             self.result_text.color = ft.Colors.GREEN
#             self.page.update()
#         except Exception as ex:
#             print(f"Ошибка при удалении КПР: {str(ex)}")
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#         # Обновляем форму после завершения
#         self.submit_form()
#
#     def submit_form(self):
#         self.employee_info_left.controls.clear()
#         self.employee_info_right.controls.clear()
#         self.result_text.value = ""
#
#         # Очистка предыдущего содержимого
#
#         self.add_ecp_button.visible = False
#         self.add_kpr_button.visible = False
#         self.page.update()
#
#         try:
#             # Получаем данные о сотруднике
#             employee_id = self.page.session.get("empl_id")
#             employee = get_one_employee_with_relation(employee_id=employee_id)
#
#             print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")
#
#             # Заполняем левую панель с основной информацией
#             self.employee_info_left.controls.extend(
#                 [
#                     ft.DataTable(
#                         columns=[
#                             ft.DataColumn(
#                                 ft.Text("Сотрудник", color=ft.Colors.BLUE, size=20, weight=ft.FontWeight.BOLD)),
#                             ft.DataColumn(
#                                 ft.Text("Должность", color=ft.Colors.BLUE, size=20, weight=ft.FontWeight.BOLD)),
#                             ft.DataColumn(
#                                 ft.Text("Имя компьютера", color=ft.Colors.BLUE, size=20, weight=ft.FontWeight.BOLD)),
#                         ],
#                         rows=[
#                             ft.DataRow(
#                                 cells=[
#                                     ft.DataCell(ft.Text(f"{employee.full_name}", color=ft.Colors.WHITE, size=18)),
#                                     ft.DataCell(ft.Text(f"{employee.position}", color=ft.Colors.WHITE, size=18)),
#                                     ft.DataCell(ft.Text(f"{employee.com_name}", color=ft.Colors.WHITE, size=18)),
#                                 ]
#                             ),
#                         ],
#                     ),
#                 ],
#             )
#             self.page.update()
#
#             # Если у сотрудника есть ЭЦП
#             if employee.ecp:
#                 for ecp_record in employee.ecp:
#                     finish_date = (
#                         ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                     datetime) else ecp_record.finish_date
#                     )
#                     days_left = (finish_date - datetime.now().date()).days
#                     finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
#
#                     self.employee_info_right.controls.extend([
#                         ft.Row(controls=[
#                             ft.Text(f"ЭЦП", color=ft.Colors.BLUE, size=18, weight=ft.FontWeight.BOLD),
#                         ]),
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Тип", color=defaultFontColor, size=16, width=150),
#                                 ft.Text(ecp_record.type_ecp, color=defaultFontColor, size=16),
#                             ]
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Статус", color=defaultFontColor, size=16, width=150),
#                                 ft.Text(ecp_record.status_ecp, color=defaultFontColor, size=16),
#                             ]
#                         ),
#                         # Добавляем остальные поля
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Дата оконч.", color=defaultFontColor, size=16, width=150),
#                                 ft.Text(str(ecp_record.finish_date), color=finish_date_color, size=16),
#                                 ft.ElevatedButton(
#                                     "Удалить",
#                                     color=ft.Colors.RED,
#                                     on_click=lambda e, ecp_id=ecp_record.id: self.delete_ecp_(ecp_id),
#                                 ),
#                             ]
#                         ),
#                         ft.Divider(),
#                     ])
#                 self.page.update()
#
#             # Если у сотрудника есть КриптоПро
#             if employee.kriptos:
#                 self.employee_info_right.controls.append(ft.Divider(color=defaultBgColor))
#
#                 for kriptos_record in employee.kriptos:
#                     finish_date = (
#                         kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date,
#                                                                         datetime) else kriptos_record.finish_date
#                     )
#                     days_left = (finish_date - datetime.now().date()).days
#                     finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
#
#                     self.employee_info_right.controls.extend([
#                         ft.Row(controls=[
#                             ft.Text(f"КПР", color=ft.Colors.BLUE, size=18, weight=ft.FontWeight.BOLD),
#                         ]),
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Место устан.", color=defaultFontColor, size=16, width=150),
#                                 ft.Text(kriptos_record.install_location, color=defaultFontColor, size=16),
#                             ]
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Дата оконч.", color=defaultFontColor, size=16, width=150),
#                                 ft.Text(str(kriptos_record.finish_date), color=finish_date_color, size=16),
#                                 ft.ElevatedButton(
#                                     "Удалить",
#                                     color=ft.Colors.RED,
#                                     on_click=lambda e, kpr_id=kriptos_record.id: self.delete_kpr_(kpr_id),
#                                 ),
#                             ]
#                         ),
#                         ft.Divider(),
#                     ])
#                 self.page.update()
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
#         self.result_text = ft.Text("")
#         self.found_employee = None
#
#     def view(self, page: ft.Page, params: Params, basket: Basket):
#         page.title = "Поиск сотрудника"
#         page.window.width = defaultWithWindow
#         page.window.height = defaultHeightWindow
#         page.window.min_width = 1000
#         page.window.min_height = 600
#
#         self.submit_form()
#
#         style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.Colors.WHITE},
#                                     icon_size=20,
#                                     text_style=ft.TextStyle(size=16),
#                                     overlay_color=hoverBgColor,
#                                     shadow_color=hoverBgColor,
#                                     )
#
#         # Панель сайдбар
#         sidebar_menu = ft.Container(
#             padding=ft.padding.symmetric(0, 13),
#             content=ft.Column(
#                 controls=[
#                     ft.Text("МЕНЮ", color=menuFontColor, size=12),
#                     ft.TextButton("Поиск сотрудника", icon=ft.Icons.SEARCH, style=style_menu,
#                                   on_click=lambda e: self.page.go("/employees")),
#                     ft.TextButton("Добавить сотрудника", icon=ft.Icons.ADD, style=style_menu,
#                                   on_click=lambda e: self.page.go("/add_employees")),
#                     # ft.TextButton("Добавить ЕЦП", icon=ft.Icons.ADD, style=style_menu,
#                     #               on_click=lambda e: self.page.go("/add_ecp")),
#                     # ft.TextButton("Добавить Крипто ПРО", icon=ft.Icons.ADD, style=style_menu,
#                     #               on_click=lambda e: self.page.go("/add_crypto")),
#                     # ft.TextButton("Удалить сотрудника", icon=ft.Icons.DELETE, style=style_menu,
#                     #              on_click=lambda e: self.page.go("/delete_employees")),
#                 ]
#             )
#         )
#
#         return ft.View(
#             "/employees",  # Исправленный маршрут
#             controls=[
#                 ft.Row(
#                     expand=True,
#                     controls=[
#                         # Левая часть
#                         ft.Container(
#                             expand=2,
#                             content=ft.Column(
#                                 controls=[
#
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
#                                                   on_click=lambda e: self.page.go("/"),
#                                                   ),  # Обработчик клика (переход на главную страницу)
#                                     sidebar_menu,
#                                 ]
#                             ),
#                             bgcolor=secondaryBgColor
#
#                         ),
#                         # Правая часть
#                         ft.Container(
#                             expand=4,
#                             alignment=ft.alignment.bottom_left,
#                             padding=ft.padding.all(20),  # Просторные внутренние отступы
#                             border=ft.border.all(1, menuFontColor),  # Одинарная рамка
#                             border_radius=ft.border_radius.all(12),  # Закругленные углы
#                             content=ft.Container(
#                                 content=ft.Column(controls=[
#                                     self.result_text,
#                                     self.employee_info_left,
#                                     ft.Divider(),
#                                     self.employee_info_right
#                                 ])
#                                 ,
#                             ),
#                         ),
#                     ],
#                 )
#             ],
#             bgcolor=defaultBgColor,  # Основной фон
#             padding=0,
#         )
