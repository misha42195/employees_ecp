import os
import shutil
import time
import xml.etree.ElementTree as ET
import flet as ft
from datetime import datetime

from crud.mchd import create_mchd
from pages.add_kriptopro_find_empl import (
    defaultBgColor,
    defaultFontColor,
    defaultHeightWindow,
    defaultWithWindow,
    menuFontColor,
    secondaryBgColor,
)
from schemas.mchd import MchdAdd
from utils.style import secondaryFontColor

UPLOAD_DIR_SIG = "assert/mchd_sign"
UPLOAD_DIR_DOWER = "assert/mchd_dower"


class AddMchdFindEmpl:
    def __init__(self, page: ft.Page):
        self.page = page
        self.employee_full_name = ft.Text(
            size=22,
            bgcolor=secondaryBgColor,
            color=secondaryFontColor
        )
        self.xml_file_path = None
        self.sig_file_path = None

        # элементы интерфейса
        self.text_add = ft.Text(
            "Добавление мчд сотруднику.\nДанные загрузятся из XML-файла.",
            color=defaultFontColor,
            size=18,
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.LEFT,
        )

        self.pick_xml_dialog = ft.FilePicker(
            on_result=self.pick_xml_result,
        )
        self.pick_sig_dialog = ft.FilePicker(
            on_result=self.pick_sig_result,
        )

        self.xml_status = ft.Text("xml файл не выбран", color=ft.Colors.RED)
        self.sig_status = ft.Text("sig, sign файл не выбран", color=ft.Colors.RED)

        self.result_text = ft.Text()

        self.page.overlay.extend([self.pick_xml_dialog, self.pick_sig_dialog])

    def pick_sig_result(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.sig_status.value = "Файл sig не выбран"
            self.sig_status.color = ft.Colors.RED
            self.sig_status.update()
            return

        file_path = e.files[0].path

        if not file_path.lower().endswith((".sig", ".sign")):
            self.sig_status.value = "Ошибка: выберите файл с расширением sig или sign"
            self.sig_status.update()
            return
        try:
            f_path = os.path.abspath("assert/mchd_sign")
            if os.path.isdir(f_path):
                shutil.rmtree(f_path)

            os.makedirs(UPLOAD_DIR_SIG, exist_ok=True)

            save_path = os.path.join(UPLOAD_DIR_SIG, os.path.basename(file_path))
            print(f"Путь к файлу", save_path)
            shutil.copy2(file_path, save_path)

            self.sig_file_path = save_path
            self.sig_status.value = f"sig файл: {os.path.basename(file_path)}"
            self.sig_status.color = ft.Colors.GREEN
            self.sig_status.update()
        except Exception as er:
            self.sig_status.value = f"Ошибка загрузки sig: {er}"
            self.sig_status.update()

    def pick_xml_result(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.xml_status.value = "Файл не выбран"
            self.xml_status.update()
            return

        file_path = e.files[0].path

        if not file_path.lower().endswith(".xml"):
            self.xml_status.value = "Выберите файл с расширением .xml"
            self.xml_status.update()
            return

        try:
            f_path = os.path.abspath("assert/mchd_dower")
            if os.path.isdir(f_path):
                shutil.rmtree(f_path)

            os.makedirs(UPLOAD_DIR_DOWER, exist_ok=True)
            save_path = os.path.join(UPLOAD_DIR_DOWER, os.path.basename(file_path))
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
        if self.xml_file_path is None or self.sig_file_path is None:
            self.result_text.value = "Необходимо загрузить файл"
            self.result_text.color = ft.Colors.RED
            self.result_text.update()
            return

        try:
            with open(self.xml_file_path, "rb") as fx:
                xml_content = fx.read()
            with open(self.sig_file_path, "rb") as fs:
                csp_content = fs.read()

            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            ns = {"ns": "urn://x-artefacts/EMCHD_1"}

            doc = root.find("ns:Документ/ns:Довер/ns:СвДов", ns)
            if doc is None:
                raise ValueError("Некорректный XML-файл!")

            fns_dov_num = doc.attrib.get("НомДовер")
            start_date_str = doc.attrib.get("ДатаВыдДовер")
            finish_date_str = doc.attrib.get("СрокДейст")

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                finish_date = datetime.strptime(finish_date_str, "%Y-%m-%d").date()
            except ValueError:
                start_date = datetime(1900, 1, 1).date()
                finish_date = datetime(1900, 1, 1).date()

            org = root.find(".//ns:СвДов", ns)
            org_dov_num = org.attrib.get("ВнНомДовер")

            powers = root.findall(".//ns:СвПолн/ns:МашПолн", ns)

            name_of_powers = ", ".join([p.attrib.get("НаимПолн", "") for p in powers])

            employee_id = self.page.session.get("employee_id")

            oMcdAdd = MchdAdd(
                employees_id=employee_id,
                organiazation_dov_num=org_dov_num,
                fns_dov_num=fns_dov_num,
                start_date=start_date,
                finish_date=finish_date,
                file_mchd=xml_content,
                file_csp=csp_content,
                name_of_powers=name_of_powers,
            )

            create_mchd(mchd_data=oMcdAdd)

            self.result_text.value = "Данные успешно сохранены!"
            self.result_text.color = ft.Colors.GREEN
            self.page.update()

            time.sleep(2)
            self.page.session.remove("employee_id")
            self.page.session.remove("employee_name")
            self.go_home()

        except Exception as e:
            self.result_text.value = f"Ошибка: {str(e)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()
        finally:
            if self.xml_file_path and os.path.exists(self.xml_file_path):
                os.remove(self.xml_file_path)
            if self.sig_file_path and os.path.exists(self.sig_file_path):
                os.remove(self.sig_file_path)

    def go_h(self):
        self.page.controls.clear()
        self.result_text.value = ""
        self.employee_full_name.value = ""
        self.page.go("/")
        self.page.update()

    def go_home(self):
        self.sig_file_path = None
        self.xml_file_path = None
        self.xml_status = ft.Text("xml файл не выбран", color=ft.Colors.RED)
        self.sig_status = ft.Text("sig файл не выбран", color=ft.Colors.RED)
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
            "/add_mchd",
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
                                    self.text_add,
                                    self.employee_full_name,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "загрузить sig",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=lambda e: self.pick_sig_dialog.pick_files(),
                                            ),
                                            self.sig_status,
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Загрузить xml",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=lambda e: self.pick_xml_dialog.pick_files(),
                                            ),
                                            self.xml_status,
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Сохранить",
                                                icon=ft.Icons.SAVE,
                                                on_click=self.save_data,
                                                disabled=False,
                                            ),
                                            self.result_text,
                                        ]
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
