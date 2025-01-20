from datetime import datetime
from math import ceil

import flet as ft
from flet_route import Params, Basket

from utils.style import *
from crud.employees import get_one_with_employees_full_name, add_employee, get_ecp_kriptopro_employee_name, \
    get_all_employees_ecp_kripto
from model import Employee


class EmployeesPage:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения
        # Элементы интерфейса
        self.result_text = ft.Text("", color=ft.Colors.BLACK)

        self.employee_info = ft.ListView( # контейнер для отображения сотрудника
            controls=[],
            expand=True,
        )

        self.text_add = ft.Text(
            "Получение сотрудника по имени",
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,

        )
        self.employee_full_name_input = ft.Container( # в объекте хранится значения имения для поиска в базе
            content=ft.TextField(
                label="Введите ФИО сотрудника",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )

        self.find_button = ft.ElevatedButton( # кнопка запускает метод submit_form
            text="Найти сотрудника",
            on_click=self.submit_form,  # Привязка кнопки к обработчику
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
        )

    def load_employees(self):
        full_name = self.employee_full_name_input.content.value.strip()
        full_name = full_name.capitalize()
        print(full_name)

        self.employee_info.controls.clear()
        self.result_text.value = ""

        if not full_name:
            self.result_text.value = "Пожалуйста, введите ФИО."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        """Загрузка данных сотрудников для текущей страницы."""
        try:
            employees = get_one_with_employees_full_name(full_name=full_name)
            if not employees:
                self.result_text.value = "Нет сотрудников в базе."
                self.result_text.color = ft.Colors.RED
                self.employee_info.controls.clear()
                self.page.update()
                return



            # Очистка текущего содержимого
            self.employee_info.controls.clear()

            # Заголовки таблицы
            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ФИО", color=ft.Colors.WHITE, size=18)),
                    ft.DataColumn(ft.Text("Дата окончания ЭЦП", color=ft.Colors.WHITE, size=18)),
                    ft.DataColumn(ft.Text("Дата окончания КриптоПро", color=ft.Colors.WHITE, size=18)),
                    ft.DataColumn(ft.Text("Действия", color=ft.Colors.WHITE, size=18)), # todo
                ],
                rows=[]
            )

            # Заполнение строк таблицы
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
                        color = ft.Colors.GREEN if days_left > 20 else ft.Colors.RED
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
                        color = ft.Colors.GREEN if days_left > 20 else ft.Colors.RED
                        kripto_data.append(f"{finish_date} ({days_left} дней осталось)")

                kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"

                # Добавление строки в таблицу
                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(employee.full_name, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(ecp_info, color=ft.Colors.GREEN if "дней осталось" in ecp_info else ft.Colors.RED)),
                            ft.DataCell(ft.Text(kripto_info, color=ft.Colors.GREEN if "дней осталось" in kripto_info else ft.Colors.RED)),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Редактировать",
                                            color=ft.Colors.BLUE,
                                            on_click=lambda e, emp=employee: self.edit_employee(
                                                employee_id=emp.id, employee_name=emp.full_name
                                            ),
                                        ),
                                        ft.ElevatedButton(
                                            "Удалить",
                                            color=ft.Colors.RED,
                                            on_click=lambda e, emp=employee: self.delete_employee(emp),
                                        ),
                                    ],
                                    spacing=10,
                                )
                            ),
                        ]
                    )
                )

            # Добавление таблицы на страницу
            self.employee_info.controls.append(data_table)

            # Обновление пагинации и страницы
            self.update_pagination_controls()
            self.page.update()

        except Exception as ex:
            import traceback
            self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            print(traceback.format_exc())  # Вывод трейсбэка для отладки
            self.page.update()


    # def submit_form(self, e):
    #     full_name = self.employee_full_name_input.content.value.strip()
    #     full_name = full_name.capitalize()
    #     print(full_name)
    #
    #     self.employee_info.controls.clear()
    #     self.result_text.value = ""
    #
    #     if not full_name:
    #         self.result_text.value = "Пожалуйста, введите ФИО."
    #         self.result_text.color = ft.Colors.RED
    #         self.page.update()
    #         return
    #
    #     try:
    #         # Получаем данные о сотруднике
    #         employee = get_ecp_kriptopro_employee_name(full_name=full_name)
    #
    #         # Для отладки: выводим информацию о сотруднике
    #         print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")
    #
    #         self.result_text.value = f"Сотрудник '{employee.full_name}' есть в базе!"
    #         self.result_text.color = ft.Colors.GREEN
    #
    #         # Очистка предыдущего содержимого
    #         self.employee_info.controls.clear()
    #
    #         # Добавляем данные о сотруднике в ListView
    #         self.employee_info.controls.extend([
    #             ft.Text(f"Сотрудник: {employee.full_name}", color=ft.Colors.BLUE, size=22, weight=ft.FontWeight.BOLD,
    #                     selectable=True),
    #             ft.Text(f"Должность : {employee.position}", color=defaultFontColor, size=20),
    #             ft.Text(f"Имя компьютера : {employee.com_name}", color=defaultFontColor, size=20),
    #             ft.Divider(color=defaultBgColor),
    #
    #         ])
    #         # Добавляем связанные данные (ecp и kriptos)
    #         if employee.ecp:
    #
    #             for ecp_record in employee.ecp:
    #                 finish_date = ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
    #                                                                           datetime) else ecp_record.finish_date
    #                 days_left = (finish_date - datetime.now().date()).days
    #                 finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
    #
    #                 self.employee_info.controls.extend([
    #                     ft.Text(f"ЕСП:", color=ft.Colors.BLUE, size=20, weight=ft.FontWeight.BOLD),
    #                     ft.Text(f"Тип:ЕСП\t\t \t                {ecp_record.type_ecp}", color=defaultFontColor,
    #                             size=18),
    #                     ft.Text(f"Статус ЕСП:\t\t             {ecp_record.status_ecp}", color=defaultFontColor,
    #                             size=18),
    #                     ft.Text(f"Место установки:\t        {ecp_record.install_location}", color=defaultFontColor,
    #                             size=18),
    #                     ft.Text(f"Место хранения:\t         {ecp_record.storage_location}", color=defaultFontColor,
    #                             size=18),
    #                     ft.Text(f"Прим. к СБИС:\t        {ecp_record.sbis}", color=defaultFontColor, size=18),
    #                     ft.Text(f"прим. к ЧЗ:\t\t          {ecp_record.chz}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Прим. к Диадок:\t      {ecp_record.diadok}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Прим. к ФНС:\t\t        {ecp_record.fns}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Прим. к отчетности:\t  {ecp_record.report}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Прим. к фед.рес:\t {ecp_record.fed_resours}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Дата начала:\t\t           {ecp_record.start_date}", color=defaultFontColor, size=18),
    #                     ft.Text(f"Дата окончания:\t         {ecp_record.finish_date}", color=finish_date_color,
    #                             size=18),
    #                     ft.Divider(color=defaultBgColor),
    #                 ])
    #
    #             if employee.kriptos:
    #                 for kriptos_record in employee.kriptos:
    #                     finish_date = kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date,
    #                                                                                   datetime) else kriptos_record.finish_date
    #                     days_left = (finish_date - datetime.now().date()).days
    #                     finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
    #                     self.employee_info.controls.extend([
    #                         ft.Text(f"КриптоПро: ", color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD, size=18),
    #                         ft.Text(f"Место установки: {kriptos_record.install_location}", color=defaultFontColor,
    #                                 size=18),
    #                         ft.Text(f"Тип лицензии: {kriptos_record.licens_type}", color=defaultFontColor, size=18),
    #                         ft.Text(f"Дата начала: {kriptos_record.start_date}", color=defaultFontColor, size=18),
    #                         ft.Text(f"Дата окончания: {kriptos_record.finish_date}", color=finish_date_color, size=18),
    #                         ft.Divider(color=defaultBgColor),
    #                     ])
    #         # Обновляем страницу для отображения новых данных
    #         self.page.update()
    #
    #     except ValueError as er:
    #         self.result_text.value = str(er)
    #         self.result_text.color = ft.Colors.RED
    #         self.page.update()
    #     except Exception as ex:
    #         self.result_text.value = f"Произошла ошибка: {str(ex)}"
    #         self.result_text.color = ft.Colors.RED
    #         self.page.update()


    def submit_form(self, e):
        full_name = self.employee_full_name_input.content.value.strip()
        full_name = full_name.capitalize()
        print(full_name)

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

                ft.Divider(color=defaultBgColor),
            ])

            # Добавляем связанные данные (ecp и kriptos)
            if employee.ecp:
                for ecp_record in employee.ecp:
                    finish_date = ecp_record.finish_date.date() if isinstance(ecp_record.finish_date, datetime) else ecp_record.finish_date
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

        self.employee_id = self.page.session.get("employee_id")

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
