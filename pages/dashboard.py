import time
from datetime import datetime
from math import ceil

import flet as ft
from flet_route import Params, Basket
from sqlalchemy.orm.sync import update

from crud.employees import get_all_employees_ecp_kripto, delete_employee, update_employee, add_employee
from utils.style import *


class DashboardPage:

    def __init__(self, page: ft.Page):
        self.pagination_controls = ft.Row()
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.WHITE)
        self.employee_info = ft.ListView(expand=True)
        self.current_page = 1
        self.page_size = 1
        self.total_pages = 1
        self.result_text = ft.Text()
        self.load_employees()

    def update_pagination_controls(self):
        """Обновляет элементы управления пагинацией."""
        self.pagination_controls.controls.clear()
        self.pagination_controls.controls.extend([
            ft.Button(
                "Предыдущая",
                color=menuFontColor,
                on_click=lambda e: self.go_to_page(self.current_page - 1),
                disabled=self.current_page <= 1  # Отключаем кнопку на первой странице
            ),
            ft.Text(f"Страница {self.current_page} из {self.total_pages}", color=ft.Colors.WHITE),
            ft.ElevatedButton(
                "Следующая",
                color=menuFontColor,
                on_click=lambda e: self.go_to_page(self.current_page + 1),
                disabled=self.current_page >= self.total_pages  # Отключаем кнопку на последней странице
            )
        ])

    # Функция удаления сотрудника
    def delete_employee(self, emp):

        try:
            # Переменная для хранения найденного сотрудника
            employee = emp
            employee_id = employee.id
            # Удаляем сотрудника
            delete_employee(employee_id=employee_id)
            self.result_text.value = f"Сотрудник {employee.full_name} успешно удалён."
            self.result_text.color = ft.Colors.GREEN
            self.page.update()
            time.sleep(2)
            self.result_text.value = ""

        except Exception as ex:
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()
        self.load_employees()

    # переход на страницу обновления данных сотрудника
    def edit_employee(self, employee_id, employee_name):
        print(employee_id)
        print(employee_name)

        self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы

        # self.page.go(f"/update_employees?employee_id={employee_id}")
        self.page.go(f"/update_employees")
        self.page.update()

    def show_employee_info(self, empl_id: int):
        self.page.session.set("empl_id", empl_id)
        print(f"dashboard, {empl_id}"),

        self.page.go(f"/employees_info")

    def add_certificate_row(self, title, finish_date, days_left, color):
        """Добавление строки с сертификатом (ЕЦП или КриптоПро)."""
        finish_date_color = color if days_left <= 20 else ft.Colors.WHITE
        return ft.DataCell(
            ft.Text(f"{title}: дата окончания: {finish_date}", color=finish_date_color, expand=1),
        )




    def load_employees(self):
        """Загрузка данных сотрудников для текущей страницы."""

        try:
            employees = get_all_employees_ecp_kripto()
            if not employees:
                self.result_text.value = "Нет сотрудников в базе."
                self.result_text.color = ft.Colors.RED
                self.employee_info.controls.clear()
                self.page.update()
                return

            # Расчёт данных для текущей страницы
            self.total_pages = ceil(len(employees) / self.page_size)
            start_index = (self.current_page - 1) * self.page_size
            end_index = start_index + self.page_size
            page_employees = employees[start_index:end_index]

            self.employee_info.controls.clear()

            for employee_tuple in page_employees:
                employee = employee_tuple[0]

                # Сбор информации об ЭЦП
                ecp_data = []
                if employee.ecp:
                    for ecp_record in employee.ecp:
                        finish_date = (
                            ecp_record.finish_date.date()
                            if isinstance(ecp_record.finish_date, datetime)
                            else ecp_record.finish_date
                        )
                        days_left = (finish_date - datetime.now().date()).days
                        ecp_data.append(f"{finish_date} ({days_left} дней осталось)")

                ecp_info = "\n".join(ecp_data) if ecp_data else "Нет данных"

                # Сбор информации о КриптоПро
                kripto_data = []
                if employee.kriptos:
                    for kripto_record in employee.kriptos:
                        finish_date = (
                            kripto_record.finish_date.date()
                            if isinstance(kripto_record.finish_date, datetime)
                            else kripto_record.finish_date
                        )
                        days_left = (finish_date - datetime.now().date()).days
                        kripto_data.append(f"{finish_date} ({days_left} дней осталось)")

                kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"

                # Добавление информации в таблицу
                self.employee_info.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Имя", color=ft.Colors.WHITE, size=18)),
                            ft.DataColumn(ft.Text("Дата окончания эцп", color=ft.Colors.WHITE, size=18)),
                            ft.DataColumn(ft.Text("Дата окончания криптопро", color=ft.Colors.WHITE)),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text(
                                            employee.full_name,
                                            color=ft.Colors.WHITE)),
                                    ft.DataCell(ft.Text(
                                        ecp_info,
                                        color=ft.Colors.GREEN if "дней осталось" in ecp_info else ft.Colors.RED,
                                        size=15
                                    )),
                                    ft.DataCell(ft.Text(
                                        kripto_info,
                                        color=ft.Colors.GREEN if "дней осталось" in kripto_info else ft.Colors.RED,
                                        size=15
                                    )),
                                ],
                                on_long_press=lambda e: self.show_employee_info(empl_id=employee.id)
                            )
                        ],
                          # Заполнение доступного пространства
                        data_row_max_height=float("inf"),  # Автоматическая подстройка высоты строки
                        data_row_min_height=48.0,  # Минимальная высота строки (по умолчанию)

                    )
                )

                # Кнопки редактирования и удаления
                self.employee_info.controls.append(
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        "Редактировать",
                                        color=menuFontColor,
                                        on_click=lambda e: self.edit_employee(
                                            employee_id=employee.id, employee_name=employee.full_name
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "Удалить",
                                        color=ft.Colors.RED,
                                        on_click=lambda e: self.delete_employee(employee),
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )

                # Разделитель между сотрудниками
                self.employee_info.controls.append(ft.Divider(color=ft.Colors.WHITE))

            # Обновление пагинации и страницы
            self.update_pagination_controls()
            self.page.update()

        except Exception as ex:
            import traceback
            self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            print(traceback.format_exc())  # Вывод трейсбэка для отладки
            self.page.update()



    def go_to_page(self, page_number):
        """Переход к указанной странице."""
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number
            self.load_employees()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Панель управления"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"

        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.Colors.WHITE},
                                    icon_size=30,
                                    overlay_color=hoverBgColor,
                                    shadow_color=hoverBgColor,
                                    )

        # Панель сайдбар
        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=12),
                    ft.TextButton("Данные сотрудника", icon=ft.Icons.WORK, style=style_menu,
                                  on_click=lambda e: self.page.go("/employees")),
                    ft.TextButton("Добавить нового сотрудника", icon=ft.Icons.ADD, style=style_menu,
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
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # левая сторона
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                controls=[
                                    sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBgColor
                        ),
                        # Container with employee data
                        ft.Container(
                            expand=4,
                            content=ft.Column(
                                controls=[self.result_text,
                                          ft.Divider(),
                                          self.employee_info,
                                          ft.Divider(),
                                          self.pagination_controls]
                            ),
                            bgcolor=defaultBgColor
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
