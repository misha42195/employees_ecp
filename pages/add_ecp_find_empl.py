from datetime import datetime

import flet as ft
import time

from flet_route import Params, Basket

from crud.employees import get_one_employees_with_id
from model import Employee  # Ваши модели и функции
from schemas.ecpies import EcpReqestAdd
from utils.style import *
from crud.ecpies import create_ecp


class AddEcpFindEmpl:
    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения

        # Элементы интерфейса
        self.text_add = ft.Text(
            "Добавление эцп сотруднику",
            size=20,
            color=defaultFontColor,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT
        )

        # Поля ввода для "ECP"
        self.type_ecp_or_token_input = ft.Container(
            content=ft.Dropdown(
                label="вид ЭЦП",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="токен", text="токен"),
                    ft.dropdown.Option(key="реестр", text="реестр"),
                ]
            ),
            border_radius=10
        )

        self.status_ecp_input = ft.Container(
            content=ft.Dropdown(
                label="действующая ЭЦП\отозвана ЭЦП",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="действующая", text="действующая"),
                    ft.dropdown.Option(key="отозван", text="отозван"),
                ]
            ), border_radius=15)
        # место установки
        self.install_location_input = ft.Container(
            content=ft.TextField(
                label="введите место установки",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500),

            border_radius=15)

        # где хранится
        self.storage_location_input = ft.Container(
            content=ft.TextField(
                label="введите место хранения",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500),
            # color=secondaryFontColor),
            border_radius=15)

        # применим к сбис (да/нет) выпадающий список
        self.sbis_input = ft.Container(
            content=ft.Dropdown(
                label="применим к сбис",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="Нет", text="Нет"),
                ],
            ), border_radius=15)

        # применим к ЧЗ (да/нет) выпадающий список
        self.cz_input = ft.Container(
            content=ft.Dropdown(
                label="применим к чз",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ), border_radius=15)

        # применим к диадок(да/нет) выпадающий список
        self.diadok_input = ft.Container(
            content=ft.Dropdown(
                label="применим к диадок",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ), border_radius=15)

        # применим к фнс(да/нет) выпадающий список
        self.fns_input = ft.Container(
            content=ft.Dropdown(
                label="применим к фнс",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ), border_radius=15)

        # применим к отчетности(да/нет) выпадающий список
        self.report_input = ft.Container(
            content=ft.Dropdown(
                label="применим к отчетности",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ), border_radius=15)

        # Применим к фед. ресурсу(да/нет) выпадающий список
        self.fed_resours_input = ft.Container(
            content=ft.Dropdown(
                label="применим к фед.ресурсу",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
                options=[
                    ft.dropdown.Option(key="да", text="да"),
                    ft.dropdown.Option(key="нет", text="нет"),
                ],
            ),
            border_radius=15
        )
        # self.start_date_input = ft.Text("")
        # self.finish_date_input = ft.Text("")
        # self.start_date_input = ft.Container(
        #     content=ft.TextField(
        #         label="дата начала лицензии (дд.мм.гггг)",
        #         hint_text="пример: 10.10.2025",
        #         bgcolor=ft.Colors.GREY_100,
        #         border=ft.InputBorder.NONE,
        #         filled=True,
        #         width=500,
        #     ),
        #     border_radius=15)

        # self.start_date_input = ft.DatePicker(
        #     first_date=datetime(year=2023, month=1, day=1),
        #     last_date=datetime(year=2040, month=12, day=31),
        #     on_change=lambda e: self.get_start_date()
        # )
        #
        # # дата завершения лицензии
        # self.finish_date_input = ft.DatePicker(
        #     first_date=datetime(year=2023, month=1, day=1),
        #     last_date=datetime(year=2040, month=12, day=31),
        #     on_change=lambda e: self.get_finish_date()
        # )
        #
        # self.start_date_input_button = ft.Container(
        #     ft.ElevatedButton(
        #         "дата начала лицензии",
        #         icon=ft.Icons.CALENDAR_MONTH,
        #         # on_click=lambda e: self.page.open(self.start_date_input)),
        #         # on_click=lambda e: self.finish_date_input.pick_date()
        #         on_click=lambda e: self.page.open(self.start_date_input)
        #     )
        # )  #
        #
        # self.finish_date_input_button = ft.Container(
        #     ft.ElevatedButton(
        #         "дата окончания действия",
        #         icon=ft.Icons.CALENDAR_MONTH,
        #         on_click=lambda e: self.page.open(self.finish_date_input)))

        #     content=ft.TextField(
        #         label="дата окончания лицензии (дд.мм.гггг)",
        #         hint_text="пример: 20.12.2025",
        #         bgcolor=ft.Colors.GREY_100,
        #         border=ft.InputBorder.NONE,
        #         filled=True,
        #         width=500,
        #     ),
        #     border_radius=15
        # )

        self.finish_date_input = ft.Container(
            content=ft.TextField(
                label="дата окончания лицензии (дд.мм.гггг)",
                hint_text="пример: 20.12.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15
        )
        self.start_date_input = ft.Container(
            content=ft.TextField(
                label="дата начала лицензии (дд.мм.гггг)",
                hint_text="пример: 10.10.2025",
                bgcolor=ft.Colors.GREY_100,
                border=ft.InputBorder.NONE,
                filled=True,
                width=500,
            ),
            border_radius=15)

        self.employee_save_button = ft.ElevatedButton(
            text="сохранить сотрудника",
            on_click=self.submit_form,
            bgcolor=ft.Colors.BLUE_100,
            # color=defaultFontColor,
        )

        self.result_text = ft.Text("",color=ft.Colors.GREEN)

    def get_start_date(self):
        self.finish_date_input = self.finish_date_input
        self.page.update()

    # Диалоговое окно для подтверждения добавления ECP
    def get_finish_date(self):
        self.start_date_input = self.start_date_input
        self.page.update()

    def submit_form(self, e):

        # employees = self.page.session.get("employee_name")
        type_ecp_or_token = self.type_ecp_or_token_input.content.value
        status_ecp = str(self.status_ecp_input.content.value)
        install_location = str(self.install_location_input.content.value).strip()
        storage_location = str(self.storage_location_input.content.value).strip()
        sbis = str(self.sbis_input.content.value)
        chz = str(self.cz_input.content.value)
        diadok = str(self.diadok_input.content.value)
        fns = str(self.fns_input.content.value)
        report = str(self.report_input.content.value)
        fed_resours = str(self.fed_resours_input.content.value)
        start_date = self.start_date_input.content.value
        finish_date = self.finish_date_input.content.value

        # Проверка на заполненность всех полей
        if not (type_ecp_or_token and status_ecp and install_location
            and storage_location and sbis and chz and diadok and fns
            and report and fed_resours and start_date and finish_date):

            self.result_text.value = "Пожалуйста, заполните все поля."
            self.result_text.color = ft.colors.RED
            self.page.update()
            return

        try:
            start_date = datetime.strptime(str(self.start_date_input.content.value).strip(), "%d.%m.%Y").date()
            finish_date = datetime.strptime(str(self.finish_date_input.content.value).strip(), "%d.%m.%Y").date()
        except ValueError:
            self.result_text.value = "Введите корректную дату."
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return
        # start_date = self.start_date_input.value.date()
        # finish_date = self.finish_date_input.value.date()
        # Проверка на заполненность всех полей
        # if not type_ecp_or_token or not  status_ecp or not install_location or not storage_location or not\
        #         sbis or not chz or not diadok or not fns or not report or not fed_resours or not start_date or not finish_date:

        if finish_date <= start_date:
            self.result_text.value = "Дата окончания должна быть больше даты начала."
            print(finish_date)
            print(start_date)
            self.result_text.color = ft.Colors.RED
            self.page.update()
            return

        # Проверка даты окончания
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
                create_ecp(employees_id=employee.id, ecp_data=EcpReqestAdd(
                    type_ecp=type_ecp_or_token,
                    status_ecp=status_ecp,
                    install_location=install_location,
                    storage_location=storage_location,
                    sbis=sbis,
                    chz=chz,
                    diadok=diadok,
                    fns=fns,
                    report=report,
                    fed_resours=fed_resours,
                    start_date=start_date,
                    finish_date=finish_date), )
                self.result_text.value = f"сотруднику {employee.full_name} добавлен эцп."
                self.result_text.color = ft.Colors.GREEN
                self.page.update()
                time.sleep(1)
                # self.page.overlay.remove(self.finish_date_input)
                # self.page.overlay.remove(self.start_date_input)
                self.result_text.value = ""
                # Обнуляем поля формы
                # self.employee_full_name_input.content.value = ""
                self.type_ecp_or_token_input.content.value = None
                self.status_ecp_input.content.value = None
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = None
                self.cz_input.content.value = None
                self.diadok_input.content.value = None
                self.fns_input.content.value = None
                self.report_input.content.value = None
                self.fed_resours_input.content.value = None
                self.start_date_input.content.value = None
                self.finish_date_input.content.value = None
                # self.clear_page()
                self.page.go("/")


            except ValueError as er:

                # self.employee_full_name_input.content.value = ""
                self.type_ecp_or_token_input.content.value = None
                self.status_ecp_input.content.value = None
                self.install_location_input.content.value = ""
                self.storage_location_input.content.value = ""
                self.sbis_input.content.value = None
                self.cz_input.content.value = None
                self.diadok_input.content.value = None
                self.fns_input.content.value = None
                self.report_input.content.value = None
                self.fed_resours_input.content.value = None
                self.start_date_input.content.value = None
                self.finish_date_input.content.value = None

                self.result_text.value = str(er)
                self.result_text.color = ft.Colors.RED

            except Exception as e:
                self.result_text.value = f"Произошла ошибка: {str(e)}"
                self.result_text.color = ft.Colors.RED

        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Добавление эцп"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        # полное имя сотрудник
        self.employee_full_name = ft.Text(
            size=20,
            value=self.page.session.get("employee_name"),
            bgcolor=secondaryBgColor,
            color=secondaryFontColor)

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
            "/add_ecp_find_empl",
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
                                                      color={ft.ControlState.HOVERED: ft.Colors.GREY_100,
                                                             # Цвет при наведении
                                                             ft.ControlState.DEFAULT: ft.Colors.GREY_100},
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
                            # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
                            padding=ft.padding.all(10),

                        ),
                        ft.Container(
                            expand=4,
                            content=ft.Column(
                                # alignment=ft.MainAxisAlignment.START,
                                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.text_add,
                                    self.employee_full_name,  # todo вывести имя которому добавляется эцп
                                    self.type_ecp_or_token_input,
                                    self.status_ecp_input,
                                    self.install_location_input,
                                    self.storage_location_input,
                                    self.sbis_input,
                                    self.cz_input,
                                    self.diadok_input,
                                    self.fns_input,
                                    self.report_input,
                                    self.fed_resours_input,
                                    self.start_date_input,
                                    self.finish_date_input,
                                    self.result_text,
                                    # self.start_date_input_button,
                                    # self.finish_date_input_button,

                                    self.employee_save_button

                                ]
                            ),
                            bgcolor=defaultBgColor,
                            # border=ft.border.all(1, "#808080"),
                            padding=ft.padding.all(10),
                        )

                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
    # метод для очистки страницы
    # def clear_page(self):
    #     self.page.session.clear()
    #     self.page.controls.clear()
    #     self.page.update()
