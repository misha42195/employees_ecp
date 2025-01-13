import functools
from datetime import datetime
from math import ceil

import flet as ft
from flet_route import Params, Basket

from crud.employees import get_all_employees_ecp_kripto, delete_employee
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

    def edit_employee(self,employee):
        """Метод для перехода на страницу редактирования сотрудника."""
        self.page.go(f"/update_employees")


    def update_pagination_controls(self):
        """Обновляет элементы управления пагинацией."""
        self.pagination_controls.controls.clear()
        self.pagination_controls.controls.extend([
            ft.ElevatedButton(
                "Предыдущая",
                on_click=lambda e: self.go_to_page(self.current_page - 1),
                disabled=self.current_page <= 1  # Отключаем кнопку на первой странице
            ),
            ft.Text(f"Страница {self.current_page} из {self.total_pages}"),
            ft.ElevatedButton(
                "Следующая",
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

        except Exception as ex:
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()
        self.load_employees()

    def load_employees(self):
        """Загрузка данных сотрудников для текущей страницы."""
        try:
            # Получаем все данные из базы
            employees = get_all_employees_ecp_kripto()

            if not employees:
                self.result_text.value = "Нет сотрудников в базе."
                self.result_text.color = ft.Colors.RED
                # Очищаем предыдущие данные
                self.employee_info.controls.clear()
                self.page.update()

                return

            # Рассчитываем общее количество страниц
            self.total_pages = ceil(len(employees) / self.page_size)

            # Определяем данные для текущей страницы
            start_index = (self.current_page - 1) * self.page_size
            end_index = start_index + self.page_size
            page_employees = employees[start_index:end_index]

            # Очищаем предыдущие данные
            self.employee_info.controls.clear()

            # Добавляем сотрудников для текущей страницы
            for employee_tuple in page_employees:
                employee = employee_tuple[0]
                # Информация о сотруднике

                # Информация о сотруднике с кнопками справа
                employee_row = ft.Row(
                    controls=[
                        ft.Text(f"Сотрудник: {employee.full_name}", color=ft.Colors.WHITE, expand=1),  # Текст занимает всё доступное место
                        ft.Row(  # Контейнер для кнопок
                            controls=[
                                ft.ElevatedButton(
                                  "Посмотреть данные",
                                    color=menuFontColor,
                                    on_click=lambda e: self.page.go(f"/employees/{employee.id}"),

                                ),
                                ft.ElevatedButton(
                                    "Редактировать",
                                    color=menuFontColor,
                                    on_click=lambda e: self.edit_employee(employee),
                                ),
                                ft.ElevatedButton(
                                    "Удалить",
                                    color=ft.Colors.RED,
                                    on_click=lambda e: self.delete_employee(employee),
                                ),
                            ],
                            spacing=10  # Расстояние между кнопками
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Кнопки располагаются справа
                )

                self.employee_info.controls.append(employee_row)

                # Информация о ЕЦП
                if employee.ecp:
                    ecp_texts = [
                        ft.Text("ЭЦП:", color=ft.Colors.WHITE)
                    ]
                    for ecp_record in employee.ecp:
                        finish_date = (
                            ecp_record.finish_date.date()
                            if isinstance(ecp_record.finish_date, datetime)
                            else ecp_record.finish_date
                        )
                        days_left = (finish_date - datetime.now().date()).days
                        finish_date_color = ft.Colors.RED if days_left <= 20 else ft.Colors.WHITE

                        ecp_texts.extend([
                            ft.Text(f"Дата окончания: {finish_date}", color=finish_date_color),
                            ft.Divider()
                        ])
                    self.employee_info.controls.append(ft.Column(controls=ecp_texts))

                # Информация о КриптоПро
                if employee.kriptos:
                    kripto_texts = [
                        ft.Text("Криптопро:", color=ft.Colors.WHITE)
                    ]
                    for kripto_record in employee.kriptos:
                        finish_date = (
                            kripto_record.finish_date.date()
                            if isinstance(kripto_record.finish_date, datetime)
                            else kripto_record.finish_date
                        )
                        days_left = (finish_date - datetime.now().date()).days
                        finish_date_color = ft.Colors.RED if days_left <= 20 else ft.Colors.WHITE

                        kripto_texts.extend([
                            ft.Text(f"Дата окончания: {finish_date}", color=finish_date_color),
                            ft.Divider()
                        ])
                    self.employee_info.controls.append(ft.Column(controls=kripto_texts))

            # Обновляем элементы управления пагинацией
            self.update_pagination_controls()
            self.page.update()

        except Exception as ex:
            self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
            self.result_text.color = ft.Colors.RED
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
                    ft.TextButton("Добавить ЕЦП", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_ecp")),
                    ft.TextButton("Добавить Крипто ПРО", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_crypto")),
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
                        # Left side
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
