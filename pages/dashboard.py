from datetime import datetime, date
from math import ceil

import flet as ft
from flet_route import Params, Basket

from crud.employees import get_all_employees_ecp_kripto
from utils.style import *


# todo def showdetailed_employee_info - метод для отображения информации о сотруднике с его лицензиями ecp и kpr
class DashboardPage:

    def __init__(self, page: ft.Page):
        self.pagination_controls_dash = ft.Row()
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.WHITE)
        self.employee_info_dash = ft.ListView(expand=True)
        self.current_page = 1
        self.page_size = 15
        self.total_pages = 1
        self.result_text = ft.Text()
        # self.load_employees()
        self.filter_menu_bar = ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("действующие ЭЦП и КриптоПро-CSP"),
                    controls=[
                        # ft.MenuItemButton(
                        #     content=ft.Text("все работники"),
                        #     on_click=self.go_all_employees  #,
                        # ),
                        ft.MenuItemButton(
                            content=ft.Text("все работники"),
                            on_click=self.go_all_employees  #
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("недействующие ЭЦП и КриптоПро-CSP"),
                            on_click=self.go_easisted_licenses  # todo реализовать
                        ),
                    ],
                )
            ]
        )

    # def go_current_license(self, e):
    #     self.page.go("/dashboard_current_licens")  # todo запуск метода со всеми сотрудниками

    def go_all_employees(self, e):
        self.page.go("/all_employees")  # todo запуск метода сотрудниками со всеми действующими лицензиям

    def go_easisted_licenses(self, e):
        self.page.go("/dashboard_easisted_licenses")  # todo запуск метода сотрудниками со всеми просрченными лицензиям

    def update_pagination_controls(self):
        """Обновляет элементы управления пагинацией."""
        self.pagination_controls_dash.controls.clear()
        self.pagination_controls_dash.controls.extend([
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

        self.page.go(f"/employees_info")

    def load_employees(self):
        # ст
        try:
            employees = get_all_employees_ecp_kripto()
            # employees = get_all_employees()
            if not employees:
                self.result_text.value = "Нет сотрудников в базе."
                self.result_text.color = ft.Colors.RED
                self.employee_info_dash.controls.clear()
                self.page.update()
                return

            def license_active(employee):
                ecp_active = any(
                    (rec.finish_date if isinstance(rec.finish_date, date) else rec.finish_date.date()) >= datetime.now().date()
                    for rec in (employee.ecp or [])
                ) if employee.ecp else False  # Если записей нет, считаем, что ЭЦП просрочено

                kripto_active = any(
                    (rec.finish_date if isinstance(rec.finish_date, date) else rec.finish_date.date()) >= datetime.now().date()
                    for rec in (employee.kriptos or [])
                ) if employee.kriptos else False  # Если записей нет, считаем, что КриптоПро просрочено

                return ecp_active or kripto_active

            # Функция для получения минимальной даты окончания ЭЦП
            def get_min_ecp_date(employee):
                dates = [
                    ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
                                                                datetime) else ecp_record.finish_date
                    for ecp_record in (employee.ecp or [])  # Если нет записей, используем пустой список
                ]
                return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату

            # Функция для получения минимальной даты окончания КриптоПро
            def get_min_kripto_date(employee):
                dates = [
                    kripto_record.finish_date.date() if isinstance(kripto_record.finish_date,
                                                                   datetime) else kripto_record.finish_date
                    for kripto_record in (employee.kriptos or [])
                ]
                return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату

            # Функция для получения минимальной даты из ЭЦП и КриптоПро
            def get_min_ecp_kripto_date(employee):
                ecp_date = get_min_ecp_date(employee)
                kripto_date = get_min_kripto_date(employee)

                return min(ecp_date, kripto_date)  # Берем минимальную из двух дат

            # Сортировка сотрудников
            employees.sort(key=lambda emp_tuple: get_min_ecp_kripto_date(emp_tuple[0]))

            # Отфильтруем сотрудников без активных лицензий
            #     filtered_employees = [
            #     emp for emp in employees
            #     if any(
            #         ((rec.finish_date if isinstance(rec.finish_date, date) else rec.finish_date.date()) - datetime.now().date()).days > 0
            #         for rec in (emp[0].ecp or []) + (emp[0].kriptos or [])
            #     )
            # ]


            # Фильтрация сотрудников с активными лицензиями
            filtered_employees = [emp_tuple for emp_tuple in employees if license_active(emp_tuple[0])]

            # Сортировка по ближайшей дате окончания
            filtered_employees.sort(key=lambda emp_tuple: get_min_ecp_kripto_date(emp_tuple[0]))

            # def license_active(employee):
            #     ecp_active = any(
            #         (rec.finish_date if isinstance(rec.finish_date, date) else rec.finish_date.date()) >= datetime.now().date()
            #         for rec in (employee.ecp or [])
            #     ) if employee.ecp else False  # Если записей нет, считаем, что ЭЦП просрочено
            #
            #     kripto_active = any(
            #         (rec.finish_date if isinstance(rec.finish_date, date) else rec.finish_date.date()) >= datetime.now().date()
            #         for rec in (employee.kriptos or [])
            #     ) if employee.kriptos else False  # Если записей нет, считаем, что КриптоПро просрочено
            #
            #     return ecp_active or kripto_active  # Возвращаем True, если хотя бы одна лицензия активна

            filtered_employees = [
                emp for emp in employees
                if any(
                    (rec.finish_date if isinstance(rec.finish_date,
                                                   date) else rec.finish_date.date()) >= datetime.now().date()
                    for rec in (emp[0].ecp or []) + (emp[0].kriptos or [])
                )
            ]

            # Расчёт данных для текущей страницы
            self.total_pages = ceil(len(filtered_employees) / self.page_size)
            start_index = (self.current_page - 1) * self.page_size
            end_index = start_index + self.page_size
            page_employees = filtered_employees[start_index:end_index]

            self.employee_info_dash.controls.clear()

            # Заголовки таблицы
            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("cотрудник", color=ft.Colors.WHITE, size=22)),
                    ft.DataColumn(ft.Text("дата окончания эцп", color=ft.Colors.WHITE, size=22)),
                    ft.DataColumn(ft.Text("дата окончания кпр", color=ft.Colors.WHITE, size=22)),
                ],
                rows=[],
            )

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
                        if days_left > 0:  # Фильтрация истекших записей
                            ecp_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")

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
                        if days_left > 0:  # Фильтрация истекших записей
                            kripto_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")

                kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"

                # Если у сотрудника нет активных лицензий, не добавлять его в таблицу
                if not ecp_data and not kripto_data:
                    continue

                # Добавление строки с данными сотрудника
                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(employee.full_name, color=ft.Colors.WHITE, size=18)),
                            ft.DataCell(ft.Text(ecp_info,
                                                color=ft.Colors.GREEN if "дней осталось" in ecp_info else ft.Colors.RED,
                                                size=18)),
                            ft.DataCell(ft.Text(kripto_info,
                                                color=ft.Colors.GREEN if "дней осталось" in kripto_info else ft.Colors.RED,
                                                size=18)),
                        ],
                        # Обработчик нажатия
                        on_long_press=lambda e, emp_id=employee.id: self.show_employee_info(emp_id),
                    )
                )

            # Добавление таблицы в контейнер
            self.employee_info_dash.controls.append(data_table)

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
        page.title = "Работники с лицензиями"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"
        self.load_employees()  # обновление данных при каждом переходе на страницу

        # Проверяем параметр обновления
        # if params.get("refresh") == "true":
        #     self.load_employees()

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
            "/",
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # Левая сторона
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                controls=[
                                    sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),  # Внутренние отступы
                        ),
                        # Контейнер с данными сотрудников
                        ft.Container(
                            expand=4,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.filter_menu_bar
                                        ]
                                    ),
                                    # self.filter_menu_bar,
                                    self.result_text,
                                    ft.Divider(),
                                    self.employee_info_dash,
                                    ft.Divider(),
                                    self.pagination_controls_dash
                                ]
                            ),
                            bgcolor=defaultBgColor,
                            # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),  # Внутренние отступы
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
