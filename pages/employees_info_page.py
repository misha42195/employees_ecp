from datetime import datetime

import flet as ft
from flet_route import Params, Basket

from crud.employees import delete_employee, get_one_with_employees_full_name, \
    get_one_employee_with_relation  # Импорт методов работы с базой данных
from utils.style import *  # Стили и настройки


class EmployeesInfoPage:
    def __init__(self, page: ft.Page):
        self.page = page  # Главная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            f"Данные сотрудника",
            color=defaultFontColor,
            size=18,
            text_align=ft.TextAlign.LEFT
        )

        self.employee_info_left = ft.ListView(
            controls=[],
            expand=True,
        )
        self.employee_info_right = ft.ListView(
            controls=[],
            expand=True,
        )

        self.result_text = ft.Text("", color=ft.Colors.BLACK)

        self.submit_form()

    def submit_form(self):
        self.employee_info_left.controls.clear()
        self.employee_info_right.controls.clear()
        self.result_text.value = ""

        try:
            # Получаем данные о сотруднике
            # employee = get_ecp_kriptopro_employee_name(full_name=full_name)
            employee_id = self.page.session.get("empl_id")

            employee = get_one_employee_with_relation(employee_id=employee_id)  # # получаем сотрудника со ЭЦП и КПР
            # Для отладки: выводим информацию о сотруднике
            print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")

            # self.result_text.value = f"Сотрудник '{employee.full_name}' есть в базе!"
            # self.result_text.color = ft.Colors.GREEN

            # Очистка предыдущего содержимого
            self.employee_info_left.controls.clear()
            self.employee_info_right.controls.clear()

            self.employee_info_left.controls.extend(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Сотрудник", color=ft.Colors.BLUE, size=22), ),
                            ft.DataColumn(ft.Text("Должность", color=ft.Colors.BLUE, size=22)),
                            ft.DataColumn(ft.Text("Имя компьютера", color=ft.Colors.BLUE, size=22)),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(f"{employee.full_name}", color=ft.Colors.WHITE, size=19), ),
                                    ft.DataCell(ft.Text(f"{employee.position}", color=ft.Colors.WHITE, size=19)),
                                    ft.DataCell(ft.Text(f"{employee.com_name}", color=ft.Colors.WHITE, size=19)),
                                ]
                            )
                        ]
                    ),

                ],
            )

            if employee.ecp:

                for ecp_record in employee.ecp:
                    finish_date = ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
                                                                              datetime) else ecp_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                    self.employee_info_right.controls.extend([
                        ft.Row(controls=[
                            ft.Text(f"ЭЦП", color=ft.Colors.BLUE, size=17, weight=ft.FontWeight.BOLD),

                        ]),
                        ft.Row(
                            controls=[
                                ft.Text("Тип", color=defaultFontColor, size=16, width=150),
                                # Фиксированная ширина для выравнивания
                                ft.Text(ecp_record.type_ecp, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Статус", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.status_ecp, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Место устан.", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.install_location, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Место хран.", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.storage_location, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к СБИС", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.sbis, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к ЧЗ", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.chz, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к Диадок", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.diadok, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к ФНС", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.fns, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к отчетности", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.report, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Прим. к фед.ресурс", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.fed_resours, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Дата нач.", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.start_date, color=defaultFontColor, size=16),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Дата оконч.", color=defaultFontColor, size=16, width=150),
                                ft.Text(ecp_record.finish_date, color=finish_date_color, size=16),
                                ft.ElevatedButton(
                                    "Удалить",
                                    color=ft.Colors.RED,
                                    on_click=lambda e: self.delete_ecp(employee),  # todo добавить
                                ),

                            ]
                        ),
                        ft.Divider(),
                    ])

                if employee.kriptos:
                    # Первый разделитель перед всеми элементами
                    self.employee_info_right.controls.append(ft.Divider(color=defaultBgColor))

                    for kriptos_record in employee.kriptos:
                        finish_date = kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date,
                                                                                      datetime) else kriptos_record.finish_date
                        days_left = (finish_date - datetime.now().date()).days
                        finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                        self.employee_info_right.controls.extend([
                            ft.Row(controls=[
                                ft.Text(f"КПР", color=ft.Colors.BLUE, size=17, weight=ft.FontWeight.BOLD),

                            ]),
                            ft.Row(
                                controls=[
                                    ft.Text("Место устан.", color=defaultFontColor, size=16, width=150),
                                    ft.Text(kriptos_record.install_location, color=defaultFontColor, size=16),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Тип лиц.", color=defaultFontColor, size=16, width=150),
                                    ft.Text(kriptos_record.licens_type, color=defaultFontColor, size=16),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Дата нач.", color=defaultFontColor, size=16, width=150),
                                    ft.Text(str(kriptos_record.start_date), color=defaultFontColor, size=16),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Дата оконч.", color=defaultFontColor, size=16, width=150),
                                    ft.Text(str(kriptos_record.finish_date), color=finish_date_color, size=16),
                                    ft.ElevatedButton(
                                        "Удалить",
                                        color=ft.Colors.RED,
                                        on_click=lambda e: self.delete_ecp(employee),  # todo добавить
                                    ),
                                    # Добавление разделителя между каждым объектом
                                    ft.Divider(color=defaultBgColor),

                                ]
                            ),

                        ])

                    # Обновляем страницу для отображения новых данных после завершения цикла
                    self.page.update()


        except ValueError as er:
            self.result_text.value = str(er)
            self.result_text.color = ft.Colors.RED
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Произошла ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        # Текст для отображения результата
        self.result_text = ft.Text("")
        self.found_employee = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Информация о сотруднике"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        self.submit_form()

        return ft.View(
            "/employees_info",  # Исправленный маршрут
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=3,
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
                                            alignment=ft.alignment.bottom_left
                                        ),
                                        on_click=lambda e: self.page.go("/"),
                                        tooltip="На главную"
                                    ),
                                    self.text_add,
                                    self.employee_info_left,
                                    # self.employee_full_name_input,
                                    # self.check_employee_button,
                                    # self.delete_employee_button,
                                    self.result_text,
                                ]
                            )
                        ),
                        ft.Container(
                            expand=3,
                            alignment=ft.alignment.bottom_left,
                            content=ft.Column(
                                controls=[
                                    self.result_text,
                                    self.employee_info_right]
                            ),
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,

        )
