import os
import shutil
import time
import flet as ft
from webbrowser import open as open_browser
from pages.add_kriptopro_find_empl import (
    defaultBgColor,
    defaultFontColor,
    defaultHeightWindow,
    defaultWithWindow,
    menuFontColor,
    secondaryBgColor,
)
from utils.style import secondaryFontColor

UPLOAD_DIR1 = "assert/mchd_class"


class AddMchdClassif:
    def __init__(self, page: ft.Page):
        self.page = page
        self.employee_full_name = ft.Text(
            size=22,
            bgcolor=secondaryBgColor,
            color=secondaryFontColor
        )
        self.xml_file_path = None
        self.url = "https://esnsi.gosuslugi.ru/classifiers/6714/data?pg=1&p=1"
        self.link = ft.Text(
            style=ft.TextStyle(
                color=ft.Colors.BLUE,
                size=22,
            ),
            spans=[
                ft.TextSpan(
                    text="Скачать актуальную версию на Госуслугах",
                    on_click=lambda e: open_browser(self.url),
                    style=ft.TextStyle(color=ft.Colors.BLUE_600),
                )
            ],
        )

        self.text_add = ft.Text(
            "Загрузите актуальный xml файл справочник-классификатор.",
            color=defaultFontColor,
            size=18,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,
        )
        self.pick_xml_dial = ft.FilePicker(
            on_result=self.pick_xml_result,
        )

        self.xml_status = ft.Text("xml файл не выбран", color=ft.Colors.RED)

        self.result_text = ft.Text()

        self.page.overlay.extend(
            [self.pick_xml_dial]
        )

    def pick_xml_result(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.xml_status.value = "Файл не выбран"
            self.xml_status.color = ft.Colors.RED
            self.xml_status.update()
            return

        file_path = e.files[0].path
        if not file_path.lower().endswith(".xml"):
            self.xml_status.value = "Ошибка: выбранный файл не является XML"
            self.xml_status.color = ft.Colors.RED
            self.xml_status.update()
            return
        f_path = os.path.abspath("assert/mchd_class")

        try:
            if os.path.isdir(f_path):
                shutil.rmtree(f_path)

            os.makedirs(UPLOAD_DIR1, exist_ok=True)
            save_path = os.path.join(UPLOAD_DIR1, os.path.basename(file_path))

            # копируем файл
            shutil.copy2(file_path, save_path)

            self.xml_file_path = save_path
            self.xml_status.value = f"xml файл: {os.path.basename(file_path)}"
            self.xml_status.color = ft.Colors.GREEN
            self.xml_status.update()
        except Exception as er:
            self.xml_status.value = f"Ошибка загрузки xml: {er}"
            self.xml_status.color = ft.Colors.RED
            self.xml_status.update()

    def save_data(self, e):
        if self.xml_file_path is None:
            self.result_text.value = "Необходимо загрузить файл"
            self.result_text.color = ft.Colors.RED
            self.result_text.update()
            return
        try:
            self.result_text.value = "Данные успешно сохранены!"
            self.result_text.color = ft.Colors.GREEN
            self.page.update()

            time.sleep(2)
            self.go_home()
        except Exception as e:
            self.result_text.value = f"Ошибка: {str(e)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()
        finally:
            # Удаление временных файлов
            if self.xml_file_path and os.path.exists(self.xml_file_path):
                os.remove(self.xml_file_path)

    def go_h(self):
        self.page.controls.clear()
        self.result_text.value = ""
        self.employee_full_name.value = ""
        self.page.go("/")
        self.page.update()

    def go_home(self):
        self.xml_file_path = None
        self.xml_status = ft.Text("xml файл не выбран", color=ft.Colors.RED)
        self.result_text.value = ""

        self.page.update()
        self.page.go("/")
        self.page.session.clear()

    def view(self, page: ft.Page, params, basket):
        page.title = "Добавление мчд"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600

        self.employee_full_name.value = self.page.session.get("employee_name")

        style_menu = ft.ButtonStyle(
            color="#FBF0F0",
            icon_size=30,
            text_style=ft.TextStyle(size=16),
            overlay_color=defaultBgColor,
            shadow_color=defaultBgColor,
        )
        sidebar_menu = ft.Container(
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
                ]
            ),
        )

        return ft.View(
            "/add_mcd_classif",
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
                                    ft.TextButton(
                                        "Домой",
                                        icon=ft.Icons.HOME,
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.ControlState.HOVERED: ft.Colors.GREY_100,
                                                ft.ControlState.DEFAULT: ft.Colors.GREY_100,
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(12),
                                        ),
                                        on_click=lambda e: self.go_h(),
                                    ),
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                            padding=ft.padding.all(10),
                        ),
                        ft.Container(
                            expand=7,
                            content=ft.Column(
                                controls=[
                                    self.link,
                                    self.text_add,
                                    self.employee_full_name,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Загрузить xml",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=lambda e: self.pick_xml_dial.pick_files(),
                                            ),
                                            self.xml_status,
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Сохранить",
                                                icon=ft.Icons.SAVE,
                                                on_click=lambda e: self.save_data(e),
                                            ),
                                            self.result_text,
                                        ],
                                    ),
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
