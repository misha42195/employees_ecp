import time
from datetime import datetime

import flet as ft
from flet_route import Params, Basket

from crud.ecpies import delete_ecp
from crud.employees import get_one_employee_with_relation, delete_employee  # Импорт методов работы с базой данных
from crud.kriptoproies import delete_kpr
# from pages.dashboard_ import DashboardPage
from utils.style import *  # Стили и настройки


class EmployeesInfoPage:
    def __init__(self, page: ft.Page):
        self.selected_ecp_id = None  # id эцп для удаления
        self.selected_kpr_id = None  # id кпр для удаления
        self.page = page  # Главная страница приложения
        # self.dashboard_page = DashboardPage(page=self.page)

        self.result_text = ft.Text("", color=ft.Colors.BLACK)

        # Элементы интерфейса
        self.text_add = ft.Text(
            f"Данные сотрудника",
            color=defaultFontColor,
            size=18,
            text_align=ft.TextAlign.LEFT
        )

        self.add_ecp_button = ft.ElevatedButton(
            text="Добавить эцп",
            on_click=self.add_ecp_page,  # переход на страницу добавлния эцп
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
            # visible=False,
        )

        self.add_kpr_button = ft.ElevatedButton(
            text="Добавить криптопро",
            on_click=self.add_kpr_page,  # переход на страницу добавлния кпр
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=0,
            # visible=False
        )

        self.employee_info_left = ft.ListView(
            controls=[],
            # divider_thickness=True,
            # item_extent=300,
            # padding=ft.Padding(left=0, top=0, right=0, bottom=0),
        )

        self.employee_info_right = ft.ListView(
            controls=[],
            expand=True,
            divider_thickness=True,
            padding=ft.Padding(left=0, top=0, right=0, bottom=0),
            # auto_scroll=True,  # Автопрокрутка
        )
        self.delete_employee_dialog = ft.AlertDialog(
            title=ft.Text("Удаление сотрудника"),
            modal=True,
            content=ft.Text("Вы хотите удалить сотрудника?"),
            actions=[
                ft.TextButton(
                    text="Да",
                    on_click=self.close_dialog_employee_delete,
                ),
                ft.TextButton(
                    text="Нет",
                    on_click=self.close_dialog_employee),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.update(),

        )
        self.delete_ecp_dialog = ft.AlertDialog(
            title=ft.Text("Удаление ЭЦП"),
            modal=True,
            content=ft.Text("Вы хотите удалить ЭЦП?"),
            actions=[
                ft.TextButton(
                    text="Да",
                    on_click=self.close_dialog_ecp_delete,
                ),
                ft.TextButton(
                    text="Нет",
                    on_click=self.close_dialog_ecp),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.update(),
        )
        self.delete_kpr_dialog = ft.AlertDialog(
            title=ft.Text("Удаление криптопро"),
            modal=True,
            content=ft.Text("Вы хотите удалить криптопро?"),
            actions=[
                ft.TextButton(
                    text="Да",
                    on_click=self.close_dialog_with_delete_kpr
                ),
                ft.TextButton(
                    text="Нет",
                    on_click=self.close_dialog_kpr
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def close_dialog_with_delete_kpr(self, e):
        self.delete_kpr_(self.selected_kpr_id)
        self.page.close(self.delete_kpr_dialog)
        self.page.go("/employees_info")

    def open_delete_kpr_dialog(self, kpr_id):
        self.selected_kpr_id = kpr_id
        self.page.open(self.delete_kpr_dialog)

    def open_delete_ecp_dialog(self, ecp_id):
        self.selected_ecp_id = ecp_id
        self.page.open(self.delete_ecp_dialog)

    def close_dialog_ecp_delete(self, e):
        self.delete_ecp_(self.selected_ecp_id)
        self.page.close(self.delete_ecp_dialog)
        self.page.go("/employees_info")

    def close_dialog_ecp(self, e):
        self.page.close(self.delete_ecp_dialog)

    def close_dialog_employee(self, e):
        self.page.close(self.delete_employee_dialog)

    def close_dialog_employee_delete(self, e):
        self.delete_employee()
        self.page.close(self.delete_employee_dialog)
        self.page.go("/")
        self.employee_info_right.controls.clear()

    def close_dialog_kpr(self, e):
        self.page.close(self.delete_kpr_dialog)
        self.page.go("/employees_info")

    # переход на страницу обновления данных сотрудника
    def edit_employee(self, employee_id, employee_name):
        print(employee_id)
        print(employee_name)

        self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы

        # self.page.go(f"/update_employees?employee_id={employee_id}")
        self.page.go(f"/update_employees")
        self.page.update()

    def go_home(self):
        self.page.go("/")

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

    def delete_ecp_(self, ecp_id):
        try:
            print(f'delete_===', ecp_id)
            print(f"Удаление с ID: {ecp_id}")

            delete_ecp(ecp_id)  # Вызываем функцию удаления

            # Успешное завершение
            self.result_text.value = f"ЭЦП успешно удален."
            self.result_text.color = ft.Colors.GREEN
            self.page.update()
        except Exception as ex:
            print(f"Ошибка при удалении ЭЦП: {str(ex)}")
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        # Обновляем форму после завершения
        self.submit_form()

    def delete_kpr_(self, kpr_id):
        try:
            print(f'delete_===', kpr_id)
            print(f"Удаление с ID: {kpr_id}")

            delete_kpr(kpr_id)  # Вызываем функцию удаления

            # Успешное завершение
            self.result_text.value = f"КПР успешно удален."
            self.result_text.color = ft.Colors.GREEN
            self.delete_employee_dialog.open = False,
            self.page.update()
        except Exception as ex:
            print(f"Ошибка при удалении КПР: {str(ex)}")
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        # Обновляем форму после завершения
        self.submit_form()

    def delete_employee(self):
        emp = get_one_employee_with_relation(employee_id=self.page.session.get("empl_id"))
        print(f"ДОШШЛИ СДАААААААА {emp}")
        employee_id = emp.id
        delete_employee(employee_id=employee_id)  # Удаление из БД
        # self.page.go("/employees_info")

    # def open_dialog_delete_employee(self):
    #     employee_id = self.page.session.get("empl_id")
    #     # print()
    #     employee = get_one_employee_with_relation(employee_id=employee_id)
    #     # self.delete_employee_dialog.actions[0].on_click = delete_employee(employee_id=employee.id)
    #     self.delete_employee_dialog.actions[0].on_click = lambda e: self.delete_employee(employee)
    #     self.page.open(self.delete_employee_dialog)

    def submit_form(self):
        # self.page.update()
        self.employee_info_left.controls.clear()
        self.employee_info_right.controls.clear()
        self.result_text.value = ""

        # self.page.update()

        try:
            # Получаем данные о сотруднике
            employee_id = self.page.session.get("empl_id")
            employee = get_one_employee_with_relation(employee_id=employee_id)

            print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")

            self.result_text.color = ft.Colors.GREEN
            self.add_ecp_button.visible = True
            self.add_kpr_button.visible = True
            # Очистка предыдущего содержимого
            self.employee_info_left.controls.clear()
            self.employee_info_right.controls.clear()

            # Заполняем левую панель с основной информацией
            self.employee_info_left.controls.extend(
                [

                    ft.Row(
                        controls=[
                            ft.Text(f"Сотрудник: ", color=ft.Colors.BLUE_ACCENT_700, size=22, expand=1),
                            ft.Text(f"{employee.full_name}", color=defaultFontColor, size=18, expand=2)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Должность: ", color=ft.Colors.BLUE, size=18, expand=1),
                            ft.Text(f"{employee.position}", color=defaultFontColor, size=18, expand=2)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Имя компьютера: ", color=ft.Colors.BLUE, size=18, expand=1),
                            ft.Text(f"{employee.com_name}", color=defaultFontColor, size=18, expand=2)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    ft.Row(alignment=ft.MainAxisAlignment.START, expand=1, controls=[
                        ft.IconButton(
                            icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                            icon_color="pink600",
                            icon_size=30,
                            tooltip="удалить сотрудника",
                            on_click=lambda e: self.page.open(self.delete_employee_dialog)
                        ),
                    ]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "обновить данные",
                                bgcolor=defaultBgColor,
                                tooltip="обновление данных сотрудника",
                                icon=ft.Icons.UPDATE,
                                # bgcolor='#F5EEE6',
                                height=40,
                                on_click=lambda e: self.edit_employee(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name
                                )

                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=1,
                        controls=[
                            ft.FilledButton(
                                "Добавить эцп",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый эцп",
                                on_click=lambda e: self.add_ecp_page(
                                    employee_id=employee.id, employee_name=employee.full_name
                                ),
                            )
                            # self.add_ecp_button,
                        ]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=1,
                        controls=[
                            # self.add_kpr_button
                            ft.FilledButton(
                                "Добавить кпр",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый криптопро",
                                on_click=lambda e: self.add_kpr_page(
                                    employee_id=employee.id, employee_name=employee.full_name
                                ),
                            )
                        ]),
                    ft.Row(expand=1,
                           controls=[
                               ft.Text("")
                           ]),

                    ft.Divider(color=defaultBgColor),
                ])

            self.page.update()

            # Если у сотрудника есть ЭЦП
            if employee.ecp:
                for ecp_record in employee.ecp:
                    finish_date = (
                        ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
                                                                    datetime) else ecp_record.finish_date
                    )
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                    self.employee_info_right.controls.extend([
                        ft.Row(expand=1,
                               controls=[
                                   ft.Text("ЭЦП:", color=ft.Colors.BLUE_ACCENT_700, size=18)
                               ]),
                        ft.Row(
                            controls=[
                                ft.Text(f"Тип ЭЦП:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{ecp_record.type_ecp}", color=defaultFontColor, expand=2, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Статус ЭЦП:", color=ft.Colors.BLUE, expand=1, size=18, ),
                                ft.Text(f"{ecp_record.status_ecp}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Место установки:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{ecp_record.install_location}", color=defaultFontColor, expand=2, size=18)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Место хранения:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.storage_location}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к СБИС:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{ecp_record.sbis}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к ЧЗ:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.chz}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к Диадок:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.diadok}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к ФНС:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{ecp_record.fns}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к отчетности:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.report}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Прим. к фед.рес:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.fed_resours}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата начала:", color=ft.Colors.BLUE, size=18, expand=1),
                                ft.Text(f"{ecp_record.start_date.strftime('%d.%m.%Yг.')}", color=defaultFontColor,
                                        size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата окончания:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{ecp_record.finish_date.strftime('%d.%m.%Yг.')}", color=finish_date_color,
                                        size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(expand=1,
                               controls=[

                                   ft.IconButton(
                                       icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                       icon_color="pink600",
                                       icon_size=30,
                                       tooltip="Удалить ЭЦП",
                                       # on_click=lambda e: self.delete_ecp_(ecp_record.id)
                                       # on_click=lambda e: self.page.open(self.delete_employee_dialog)
                                       on_click=lambda e: self.open_delete_ecp_dialog(ecp_record.id)
                                   ),
                               ]
                               ),
                        ft.Divider(color=defaultBgColor),
                    ])
                self.page.update()

            # Если у сотрудника есть КриптоПро
            if employee.kriptos:
                self.employee_info_right.controls.append(ft.Divider(color=defaultBgColor))

                for kriptos_record in employee.kriptos:
                    finish_date = (
                        kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date,
                                                                        datetime) else kriptos_record.finish_date
                    )
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor

                    self.employee_info_right.controls.extend([
                        ft.Row(expand=1,
                               controls=[
                                   ft.Text("Кпр-csp", color=ft.Colors.BLUE_ACCENT_700, size=18)
                               ]),
                        ft.Row(
                            controls=[
                                ft.Text(f"Место установки:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{kriptos_record.install_location}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Имя комп:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{kriptos_record.licens_type}", color=defaultFontColor, size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Версия лицензии:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{kriptos_record.version}", color=defaultFontColor, size=18, expand=2)
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата начала:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{kriptos_record.start_date.strftime('%d.%m.%Yг.')}", color=defaultFontColor,
                                        size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Дата окончания:", color=ft.Colors.BLUE, size=18, expand=1, ),
                                ft.Text(f"{kriptos_record.finish_date.strftime('%d.%m.%Yг.')}", color=finish_date_color,
                                        size=18, expand=2)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Row(expand=1,
                               controls=[
                                   ft.IconButton(
                                       icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                       icon_color="pink600",
                                       icon_size=30,
                                       tooltip="Удалить криптопро",
                                       on_click=lambda e: self.open_delete_kpr_dialog(kriptos_record.id)
                                   ),
                               ]
                               ),
                        ft.Divider(color=defaultBgColor),
                    ])
                self.page.update()

        except ValueError as er:
            self.result_text.value = str(er)
            self.result_text.color = ft.Colors.RED
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Произошла ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        self.result_text = ft.Text("")
        # self.found_employee = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Информация о сотруднике"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        self.submit_form()

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
            "/employees_info",  # Исправленный маршрут
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Левая часть
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
                        # Правая часть
                        ft.Container(
                            expand=4,
                            alignment=ft.alignment.bottom_left,
                            padding=ft.padding.Padding(left=40,top=60,right=40,bottom=60),  # Просторные внутренние отступы
                            # border=ft.border.all(1, menuFontColor),  # Одинарная рамка
                            # border_radius=ft.border_radius.all(12),  # Закругленные углы
                            content=ft.Container(

                                content=ft.Column(
                                    controls=[
                                        self.result_text,
                                        self.employee_info_left,
                                        self.employee_info_right
                                    ])
                                ,
                            ),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,  # Основной фон
            padding=0,
        )
