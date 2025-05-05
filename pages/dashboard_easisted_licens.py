import asyncio
from datetime import datetime
from math import ceil
import threading

import flet as ft
from flet_route import Params, Basket

from crud.employees import get_all_employees_ecp_kripto_mchd
from utils.style import *


class DashboardEasistedPage:

    def __init__(self, page: ft.Page):
        self.pagination_controls = ft.Row()
        self.page = page

        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.WHITE)
        self.employee_info_easisted = ft.ListView(expand=True)
        self.current_page = 1
        self.page_size = 15
        self.total_pages = 1
        self.result_text = ft.Text()
        self.loading_ring = ft.ProgressRing(
            width=40, height=40, stroke_width=3, color=ft.Colors.AMBER, visible=False
        )
        # self.load_employees()
        self.filter_menu_bar = ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("недействующие ЭЦП, КриптоПро-CSP, МЧД"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("действующие ЭЦП, КриптоПро-CSP, МЧД"),
                            on_click=self.go_all,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("все работники"),
                            on_click=self.go_current_licenses,  #
                        ),
                    ],
                )
            ]
        )

    def reset_state(self):
        self.current_page = 1
        self.total_pages = 1
        self.employee_info_easisted.controls.clear()
        self.result_text.value = ""
        self.pagination_controls.controls = []

    def add_mcd_classif(self):
        self.reset_state()
        self.page.go("/add_mcd_classif")  # todo переход на добавления файла

    def add_employees(self):
        self.reset_state()
        self.page.go("/add_employees")

    def go_all(self, e):
        self.reset_state()
        self.page.go("/all_employees")

    def go_current_licenses(self, e):
        self.reset_state()
        self.page.go("/")

    def update_pagination_controls(self):
        self.pagination_controls.controls.clear()
        self.pagination_controls.controls.extend(
            [
                ft.Button(
                    "Предыдущая",
                    color=menuFontColor,
                    on_click=lambda e: self.go_to_page(self.current_page - 1),
                    disabled=self.current_page
                             <= 1,  # Отключаем кнопку на первой странице
                ),
                ft.Text(
                    f"Страница {self.current_page} из {self.total_pages}",
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    "Следующая",
                    color=menuFontColor,
                    on_click=lambda e: self.go_to_page(self.current_page + 1),
                    disabled=self.current_page >= self.total_pages,
                ),
            ]
        )

    def go_to_page(self, page_number):
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number
            self.reset_state()
            self.load_employees()

    def _run_show_employee_info(self, emp_id):
        asyncio.run(self.load_and_show_employee(emp_id))

    def on_employee_press(self, emp_id):
        self.loading_ring.visible = True
        self.page.update()

        threading.Thread(
            target=self._run_show_employee_info, args=(emp_id,), daemon=True
        ).start()

    async def load_and_show_employee(self, emp_id):
        self.show_employee_info(emp_id)
        await asyncio.sleep(6)
        self.loading_ring.visible = False
        self.page.update()

    def edit_employee(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.go(f"/update_employees")
        self.page.update()

    def show_employee_info(self, empl_id: int):
        self.page.session.set("empl_id", None)
        self.page.session.set("empl_id", empl_id)
        self.page.session.set("empl_id", empl_id)
        self.page.go(f"/employees_info")

    def load_employees(self):
        self.employee_info_easisted.controls.clear()
        try:
            employees = get_all_employees_ecp_kripto_mchd()
            if not employees:
                self.result_text.value = "Нет сотрудников в базе."
                self.result_text.color = ft.Colors.RED
                self.employee_info_easisted.controls.clear()
                self.update_pagination_controls()
                self.page.update()
                return

            def get_min_ecp_date(employee):
                dates = [
                    ecp_record.finish_date
                    for ecp_record in (
                        employee.ecp or []
                    )
                ]
                return min(
                    dates, default=datetime.max.date()
                )

            def get_min_mchd_date(employee):
                dates = [
                    mchd_record.finish_date for mchd_record in (employee.mchd or [])
                ]
                return min(
                    dates, default=datetime.max.date()
                )

            def get_min_kripto_date(employee):
                dates = [
                    kripto_record.finish_date
                    for kripto_record in (employee.kriptos or [])
                ]
                return min(
                    dates, default=datetime.max.date()
                )

            def get_min_ecp_kripto_date(employee):
                ecp_date = get_min_ecp_date(employee)
                kripto_date = get_min_kripto_date(employee)
                mchd_date = get_min_mchd_date(employee)

                return min(
                    ecp_date, kripto_date, mchd_date
                )

            employees.sort(key=lambda emp_tuple: get_min_ecp_kripto_date(emp_tuple[0]))

            def has_expired_license(employee):
                today = datetime.now().date()
                has_expired_ecp = any(
                    record.finish_date < today for record in (employee.ecp or [])
                )

                has_expired_kripto = any(
                    record.finish_date < today for record in (employee.kriptos or [])
                )
                has_expired_mchd = any(
                    record.finish_date < today for record in (employee.mchd or [])
                )
                return has_expired_ecp or has_expired_kripto or has_expired_mchd

            employees = [empl for empl in employees if has_expired_license(empl[0])]

            self.total_pages = ceil(len(employees) / self.page_size)
            start_index = (self.current_page - 1) * self.page_size
            end_index = start_index + self.page_size
            page_employees = employees[start_index:end_index]

            if not employees:
                self.result_text.value = "Нет сотрудников с истекшими лицензиями."
                self.result_text.color = ft.Colors.RED
                self.employee_info_easisted.controls.clear()
                self.update_pagination_controls()
                self.page.update()
                return

            self.current_page = min(self.current_page, self.total_pages)

            start_index = (self.current_page - 1) * self.page_size
            end_index = start_index + self.page_size
            page_employees = employees[start_index:end_index]

            self.employee_info_easisted.controls.clear()

            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text()),
                    ft.DataColumn(ft.Text("Сотрудник", color=ft.Colors.BLUE, size=22)),
                    ft.DataColumn(ft.Text("ЭЦП", color=ft.Colors.BLUE, size=22)),
                    ft.DataColumn(
                        ft.Text("КриптоПро-CSP", color=ft.Colors.BLUE, size=22)
                    ),
                    ft.DataColumn(ft.Text("МЧД", color=ft.Colors.BLUE, size=22)),
                ],
                rows=[],
            )

            for num, employee_tuple in enumerate(page_employees, start_index + 1):
                employee = employee_tuple[0]

                ecp_data = []
                if employee.ecp:
                    for ecp_record in employee.ecp:
                        finish_date = ecp_record.finish_date
                        days_left = (finish_date - datetime.now().date()).days
                        if days_left < 0:
                            ecp_data.append(
                                f"{finish_date.strftime('%d.%m.%Yг.')} (-{days_left})"
                            )

                ecp_info = "\n".join(ecp_data) if ecp_data else ""

                kripto_data = []
                if employee.kriptos:
                    for kripto_record in employee.kriptos:
                        finish_date = kripto_record.finish_date
                        days_left = (finish_date - datetime.now().date()).days
                        if days_left < 0:
                            kripto_data.append(
                                f"{finish_date.strftime('%d.%m.%Yг.')} (-{days_left})"
                            )

                kripto_info = "\n".join(kripto_data) if kripto_data else ""

                mchd_data = []
                if employee.mchd:
                    for mchd_record in employee.mchd:
                        finish_date = mchd_record.finish_date
                        days_left = (finish_date - datetime.now().date()).days
                        if days_left < 0:
                            mchd_data.append(
                                f"{finish_date.strftime('%d.%m.%Yг.')} (-{days_left})"
                            )

                mchd_info = "\n".join(mchd_data) if mchd_data else ""

                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(value=str(num), size=18, color=ft.Colors.BLUE)
                            ),
                            ft.DataCell(
                                ft.Text(
                                    employee.full_name, color=ft.Colors.WHITE, size=18
                                )
                            ),
                            ft.DataCell(
                                ft.Text(ecp_info, color=ft.Colors.WHITE, size=18)
                            ),
                            ft.DataCell(
                                ft.Text(kripto_info, color=ft.Colors.WHITE, size=18)
                            ),
                            ft.DataCell(
                                ft.Text(mchd_info, color=ft.Colors.WHITE, size=18)
                            ),
                        ],
                        on_long_press=lambda e, emp_id=employee.id: self.on_employee_press(
                            emp_id
                        ),
                    )
                )

            self.employee_info_easisted.controls = [data_table]

            self.update_pagination_controls()
            self.page.update()

        except Exception as ex:
            self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.reset_state()

        page.title = "Истекшие лицензии"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        self.load_employees()

        style_menu = ft.ButtonStyle(
            color="#FBF0F0",
            icon_size=30,
            text_style=ft.TextStyle(size=16),
            overlay_color=defaultBgColor,
            shadow_color=defaultBgColor,
        )

        self.sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=18),
                    ft.TextButton(
                        "Поиск сотрудника",
                        icon=ft.Icons.SEARCH,
                        style=style_menu,
                        on_click=lambda e: self.page.go("/employees"),
                    ),
                    ft.TextButton(
                        "Добавить сотрудника",
                        icon=ft.Icons.ADD,
                        style=style_menu,
                        on_click=lambda e: self.page.go("/add_employees"),
                    ),
                    ft.TextButton(
                        "Загрузить мчд справочник",
                        icon=ft.Icons.DOWNLOAD,
                        style=style_menu,
                        on_click=lambda e: self.add_mcd_classif(),
                    ),
                ]
            ),
        )

        return ft.View(
            "/dashboard_easisted_licenses",
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            expand=2,
                            content=ft.Column(controls=[self.sidebar_menu]),
                            bgcolor=secondaryBgColor,
                            padding=ft.padding.all(10),
                        ),
                        ft.Container(
                            expand=7,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.filter_menu_bar,
                                            self.loading_ring,
                                        ]
                                    ),
                                    self.result_text,
                                    ft.Divider(),
                                    self.employee_info_easisted,
                                    ft.Divider(),
                                    self.pagination_controls,
                                ]
                            ),
                            bgcolor=defaultBgColor,
                            padding=ft.padding.all(10),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
