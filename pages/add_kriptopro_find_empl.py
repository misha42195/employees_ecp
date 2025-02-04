from datetime import datetime

import flet as ft
import time

from dateutil.relativedelta import relativedelta
from flet_route import Params, Basket

from crud.employees import get_one_with_employees_full_name, get_one_employees_with_id
from crud.kriptoproies import create_kriptopro
from model import Employee, ECP, KriptoPro, add_instance  # Ваши модели и функции
from schemas.ecpies import EcpReqestAdd, EcpAdd
from schemas.kriptopro import KriptoproRequestAdd
from utils.style import *
from crud.ecpies import create_ecp


class AddKriptoproFindEmpl:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            "Добавление криптопро к сотруднику",
            color=defaultFontColor,
            size=18,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT
        )

        self.instal_location_input = ft.Container(
            content=ft.TextField(
                label="Введите место установки",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )
        self.licens_type_input = ft.Container(
            content=ft.TextField(
                label="Введите имя компьютера",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15,
        )
        self.version_input = ft.Container(
            content=ft.Dropdown(
                label="Версия криптопро",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=None,
                width=500,

                options=[
                    ft.dropdown.Option(key="5", text="5"),
                    ft.dropdown.Option(key="6", text="6"),
                    ft.dropdown.Option(key="7", text="7"),
                ],
            ),
            border_radius=15
        )

        self.license_action = ft.Container(
            content=ft.Dropdown(
                label="Срок действия",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=None,
                width=500,
                options=[
                    ft.dropdown.Option(key="Срочная", text="Срочная"),
                    ft.dropdown.Option(key="Бессрочная", text="Бессрочная"),
                ],
                on_change=self.change_finishdate,  # Добавляем обработчик изменения выбора
            ),
            border_radius=15
        )

        self.start_date_input = ft.Container(
            content=ft.TextField(
                label="Дата начала действия лицензии (дд.мм.гггг)",
                hint_text="Например: 20.10.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15)

        # дата завершения лицензии
        self.finish_date_input = ft.Container(
            content=ft.TextField(
                label="Дата начала действия лицензии (дд.мм.гггг)",
                hint_text="Например: 20.10.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15
        )

        self.employee_save_button = ft.ElevatedButton(
            text="Сохранить сотрудника",
            on_click=self.submit_form,
            bgcolor=ft.Colors.BLUE_100,
            # color=ft.Colors.BLUE_100,
        )

        self.result_text = ft.Text("",color=ft.Colors.GREEN)

    # метод сработает при выборе поля "бессрочная" для срока действия лицензии
    def change_finishdate(self, e):
        selected_value = self.license_action.content.value.strip()  # Убираем лишние пробелы

        if selected_value == "Бессрочная":
            self.finish_date_input.visible = False
            # self.result_text.color.
            self.result_text.value = "Срок действия лицензии криптопро 10 лет"
            self.finish_date_input.content.value = (datetime.today() + relativedelta(years=10)).strftime('%d.%m.%Y')
        else:
            self.finish_date_input.visible = True
            self.result_text.value = ""
            self.finish_date_input.content.value = ""

        # Обновляем элементы
        self.finish_date_input.update()  # Обновляем поле даты
        self.result_text.update()  # Обновляем текст результата
        self.license_action.update()  # Обновляем dropdown
        self.page.update()  # Обновляем всю страницу


    # Диалоговое окно для подтверждения добавления ECP
    def submit_form(self, e):
        # full_name = self.employee_name_input.content.value.strip()
        install_location = self.instal_location_input.content.value.strip()
        licens_type = self.licens_type_input.content.value.strip()
        version = self.version_input.content.value
        start_date = datetime.strptime(str(self.start_date_input.content.value).strip(), "%d.%m.%Y").date()
        finish_date = datetime.strptime(str(self.finish_date_input.content.value).strip(), "%d.%m.%Y").date()

        # Проверка на заполненность всех полей
        if not (install_location and licens_type and version and start_date and finish_date):
            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        # Проверка даты окончания
        if finish_date <= start_date:
            self.result_text.value = "Дата окончания должна быть больше даты начала."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return
        if finish_date <= datetime.today().date():
            self.result_text.value = "Дата окончания должна быть больше сегодняшней даты."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return


        else:
            try:
                # получаем сотрудника из базы данных
                employee_id = self.page.session.get("employee_id")
                employee: Employee = get_one_employees_with_id(employee_id=employee_id)

                print(f"сотрудник в методе submit_form: ", employee)
                # напишем функцию для добавления объекта ecp в базу данных
                create_kriptopro(employees_id=employee.id,
                                 kriptopro_data=KriptoproRequestAdd(
                                     install_location=install_location,
                                     licens_type=licens_type,
                                     version=version,
                                     start_date=start_date,
                                     finish_date=finish_date
                                 ))
                self.result_text.color = ft.Colors.GREEN
                self.result_text.value = f"Сотруднику {employee.full_name} добавлен криптопро."

                self.page.update()
                time.sleep(2)
                self.result_text.value = ""
                # Обнуляем поля формы
                # self.employee_name_input.content.value = ""
                self.instal_location_input.content.value = ""
                self.licens_type_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""
                self.page.go("/")

            except ValueError as er:
                # self.employee_name_input.content.value = ""
                self.instal_location_input.content.value = ""
                self.licens_type_input.content.value = ""
                self.start_date_input.content.value = ""
                self.finish_date_input.content.value = ""

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED

            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

                self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление криптопро"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        # полное имя сотрудник
        self.employee_full_name = ft.Text(
            value=self.page.session.get("employee_name"),
            bgcolor=secondaryBgColor,
            color=secondaryFontColor)

        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: defaultBgColor},
                                    icon_size=20,
                                    text_style=ft.TextStyle(size=16),
                                    overlay_color=ft.Colors.GREY_300,
                                    shadow_color=ft.Colors.GREY_300,
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
            "/add_kriptopro_find_empl",
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                                                             ft.ControlState.DEFAULT: ft.Colors.GREY_300},
                                                      # Цвет по умолчанию
                                                      shape=ft.RoundedRectangleBorder(radius=8),  # Округлённые углы
                                                      padding=ft.padding.all(12),  # Внутренние отступы
                                                  ),
                                                  on_click=lambda e: self.page.go("/"),
                                                  ),  # Обработчик клика (переход на главную страницу)
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),

                        ),
                        ft.Container(
                            expand=4,
                            content=ft.Column(
                                controls=[
                                    self.text_add,
                                    self.employee_full_name,  # todo вывести имя которому добавляется эцп
                                    self.instal_location_input,
                                    self.licens_type_input,
                                    self.version_input,
                                    self.license_action,
                                    self.start_date_input,
                                    self.finish_date_input,
                                    self.result_text,

                                    self.employee_save_button

                                ]
                            ),
                            bgcolor=defaultBgColor,
                            border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),

                        ),
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
