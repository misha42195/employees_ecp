from datetime import datetime
import os
import shutil

import tempfile
import flet as ft
from flet_route import Params, Basket

from crud.ecpies import delete_ecp
from crud.employees import (
    get_one_employee_with_relation,
    delete_employee,
)
from crud.kriptoproies import delete_kpr
from crud.mchd import get_xml_from_db

from crud.mchd import delete_mchd
from utils.pow_class import (
    get_cod_from_xml,
    get_code_classifier,
    match_codes_classifier,
)
from utils.style import *


class EmployeesInfoPage:
    def __init__(self, page: ft.Page):
        self.selected_mchd_id = None
        self.page = page
        self.selected_ecp_id = None
        self.selected_kpr_id = None
        self.result_info_mchd = ft.Text()
        self.result_text = ft.Text()
        self.save_file_dialog_x = ft.FilePicker(on_result=self.save_file_result_xml)
        self.save_file_dialog_c = ft.FilePicker(on_result=self.save_file_result_sig)
        self.page.overlay.append(self.save_file_dialog_x)
        self.page.overlay.append(self.save_file_dialog_c)

        self.text_add = ft.Text(
            f"Данные сотрудника",
            color=defaultFontColor,
            size=18,
            text_align=ft.TextAlign.LEFT,
        )

        self.add_ecp_button = ft.ElevatedButton(
            text="Добавить эцп",
            on_click=self.add_ecp_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=40,
        )

        self.add_kpr_button = ft.ElevatedButton(
            text="Добавить криптопро",
            on_click=self.add_kpr_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=0,
        )
        self.add_mcd_button = ft.ElevatedButton(
            text="Добавить мчд",
            on_click=self.add_mchd_page,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=0,
        )
        self.download_mchd_button = ft.ElevatedButton(
            "скачать xml-файл",
            on_click=self.download_mchd_xml,
            bgcolor=defaultBgColor,
            color=defaultFontColor,
            height=0,
        )

        self.employee_info_left = ft.ListView(
            controls=[],
        )

        self.employee_info_right = ft.ListView(
            controls=[],
            expand=True,
            divider_thickness=True,
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
                ft.TextButton(text="Нет", on_click=self.close_dialog_employee),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
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
                ft.TextButton(text="Нет", on_click=self.close_dialog_ecp),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.delete_kpr_dialog = ft.AlertDialog(
            title=ft.Text("Удаление криптопро"),
            modal=True,
            content=ft.Text("Вы хотите удалить криптопро?"),
            actions=[
                ft.TextButton(text="Да", on_click=self.close_dialog_with_delete_kpr),
                ft.TextButton(text="Нет", on_click=self.close_dialog_kpr),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.delete_mchd_dialog = ft.AlertDialog(
            title=ft.Text("Удаление мчд"),
            modal=True,
            content=ft.Text("Вы хотите удалить мчд?"),
            actions=[
                ft.TextButton(text="Да", on_click=self.close_dialog_with_delete_mchd),
                ft.TextButton(text="Нет", on_click=self.close_dialog_mchd),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def download_mchd_sig(self, e, mchd_id=None):
        try:
            o_mchd = get_xml_from_db(mchd_id)
            if not o_mchd or not o_mchd.file_csp:
                raise ValueError("Файл не найден в базе")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".sig") as tmp:
                tmp.write(o_mchd.file_csp)
                temp_path = tmp.name

            self.save_file_dialog_c.save_file(
                allowed_extensions=["sig"], file_name=f"sig_{o_mchd.id}.sig"
            )
            self._temp_path_sig = temp_path

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {str(ex)}"))
            self.page.snack_bar.open = True
            self.page.update()

    def show(self, mchd_id: int):
        o_mchd = get_xml_from_db(mchd_id)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
            tmp.write(o_mchd.file_mchd)
            temp_file = tmp.name
            self._temp_path_xml = temp_file

        dower_code_list = get_cod_from_xml(self._temp_path_xml)

        classifier_file_path = os.path.abspath("assert/mchd_class")
        if not os.path.isdir(classifier_file_path):
            self.result_text.value = "Нужно загрузить классификатор"
            self.result_text.color = ft.Colors.RED
            self.result_text.update()
            return {}

        matched = []
        for file in os.listdir(classifier_file_path):
            full_path = os.path.join(classifier_file_path, file)
            if os.path.isfile(full_path) and file.lower().endswith(".xml"):
                classifier_mapping = get_code_classifier(
                    full_path, valid_codes=dower_code_list
                )
                matched = match_codes_classifier(
                    dover_codes=dower_code_list, classifier_map=classifier_mapping
                )
        return matched

    def download_mchd_xml(self, e, mchd_id=None):
        try:
            o_mchd = get_xml_from_db(mchd_id)
            if not o_mchd or not o_mchd.file_mchd:
                raise ValueError("Файл не найден в базе данных")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(o_mchd.file_mchd)
                temp_path = tmp.name

            self.save_file_dialog_x.save_file(
                allowed_extensions=["xml"], file_name=f"mchd_{o_mchd.id}.xml"
            )
            self._temp_path_xml = temp_path
            self.page.update()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {str(ex)}"))
            self.page.snack_bar.open = True
            self.page.update()

    def save_file_result_sig(self, e: ft.FilePickerResultEvent):
        try:
            if e.path and hasattr(self, "_temp_path_sig"):
                shutil.copy(self._temp_path_sig, e.path)
                snack = ft.SnackBar(
                    ft.Text(f"Файл успешно сохранен: {str(e.path)}"), duration=5000
                )
                self.page.overlay.append(snack)
                snack.open = True
        except Exception as ex:
            snack = ft.SnackBar(ft.Text(f"Ошибка при сохраниении: {str(ex)}"))
            self.page.overlay.append(snack)
            snack.open = True
        finally:
            if hasattr(self, "_temp_path_sig"):
                if os.path.exists(self._temp_path_sig):
                    os.unlink(self._temp_path_sig)
                del self._temp_path_sig
            self.page.update()

    def save_file_result_xml(self, e: ft.FilePickerResultEvent):
        try:
            if e.path and hasattr(self, "_temp_path_xml"):
                shutil.copy(self._temp_path_xml, e.path)
                snack = ft.SnackBar(
                    ft.Text(f"Файл успешно сохранен: {str(e.path)}"), duration=5000
                )
                self.page.overlay.append(snack)
                snack.open = True
        except Exception as ex:
            snack = ft.SnackBar(ft.Text(f"Ошибка при сохраниении: {str(ex)}"))
            self.page.overlay.append(snack)
            snack.open = True
        finally:
            if hasattr(self, "_temp_path_xml"):
                if os.path.exists(self._temp_path_xml):
                    os.unlink(self._temp_path_xml)
                del self._temp_path_xml
            self.page.update()

    def close_dialog_mchd(self, e):
        self.page.close(self.delete_mchd_dialog)
        # self.reset_state()
        self.page.go("/employees_info")

    def add_mchd_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)
        self.page.go(f"/add_mchd")
        self.page.update()

    def close_dialog_with_delete_mchd(self, e):
        self.delete_mchd_(self.selected_mchd_id)
        self.page.close(self.delete_mchd_dialog)
        self.page.go("/employees_info")

    def open_delete_mchd_dialog(self, mchd_id):
        self.selected_mchd_id = mchd_id
        self.page.open(self.delete_mchd_dialog)

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

    def edit_employee(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.go(f"/update_employees")
        self.page.update()

    def add_ecp_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)
        self.page.go(f"/add_ecp_find_empl")
        self.page.update()

    def add_kpr_page(self, employee_id, employee_name):
        self.page.session.set("employee_id", employee_id)
        self.page.session.set("employee_name", employee_name)

        self.page.go(f"/add_kriptopro_find_empl")
        self.page.update()

    def delete_ecp_(self, ecp_id):
        try:
            delete_ecp(ecp_id)
            self.result_text.value = f"ЭЦП успешно удален."
            self.result_text.color = ft.Colors.GREEN
            self.page.update()
        except Exception as ex:
            print(f"Ошибка при удалении ЭЦП: {str(ex)}")
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
        self.submit_form()

    def delete_kpr_(self, kpr_id):
        try:
            delete_kpr(kpr_id)
            self.result_text.value = f"КПР успешно удален."
            self.result_text.color = ft.Colors.GREEN
            self.delete_employee_dialog.open = False
            self.page.update()
        except Exception as ex:
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        self.submit_form()

    def delete_mchd_(self, mchd_id):
        try:
            delete_mchd(mchd_id)
            self.result_text.value = f"МЧД успешно удален."
            self.result_text.color = ft.Colors.GREEN
            self.delete_employee_dialog.open = False
            self.page.update()

        except Exception as ex:
            print(f"Ошибка при удалении МЧД: {str(ex)}")
            self.result_text.value = f"Ошибка при удалении: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        self.submit_form()

    def delete_employee(self):
        emp = get_one_employee_with_relation(
            employee_id=self.page.session.get("empl_id")
        )
        employee_id = emp.id
        delete_employee(employee_id=employee_id)  # Удаление из БД
        self.page.open(self.delete_employee_dialog)

    def submit_form(self):
        self.employee_info_right.controls.clear()
        self.employee_info_left.controls.clear()
        try:
            employee_id = self.page.session.get("empl_id")
            employee = get_one_employee_with_relation(employee_id=employee_id)

            self.result_text.color = ft.Colors.GREEN
            self.add_ecp_button.visible = True
            self.add_kpr_button.visible = True
            self.add_mcd_button.visible = True
            self.employee_info_left.controls.extend(
                [
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Сотрудник:",
                                color=ft.Colors.BLUE_ACCENT_700,
                                size=22,
                                expand=2,
                            ),
                            ft.Text(
                                f"{employee.full_name}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Должность: ", color=ft.Colors.BLUE, size=18, expand=2
                            ),
                            ft.Text(
                                f"{employee.position}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Имя компьютера: ",
                                color=ft.Colors.BLUE,
                                size=18,
                                expand=2,
                            ),
                            ft.Text(
                                f"{employee.com_name}",
                                color=defaultFontColor,
                                size=18,
                                expand=2,
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=2,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                icon_color="pink600",
                                icon_size=30,
                                tooltip="удалить сотрудника",
                                on_click=lambda e: self.page.open(
                                    self.delete_employee_dialog
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=2,
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
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=2,
                        controls=[
                            ft.FilledButton(
                                "Добавить эцп",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый эцп",
                                on_click=lambda e: self.add_ecp_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=2,
                        controls=[
                            ft.FilledButton(
                                "Добавить кпр",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый криптопро",
                                on_click=lambda e: self.add_kpr_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=2,
                        controls=[
                            ft.FilledButton(
                                "Добавить мчд",
                                icon=ft.Icons.ADD_BOX,
                                bgcolor=defaultBgColor,
                                tooltip="Добавить новый мчд",
                                on_click=lambda e: self.add_mchd_page(
                                    employee_id=employee.id,
                                    employee_name=employee.full_name,
                                ),
                            )
                        ],
                    ),
                    ft.Divider(color=defaultBgColor),
                ]
            )

            self.page.update()
            if employee.ecp:
                for ecp_record in employee.ecp:
                    finish_date = ecp_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )

                    self.employee_info_right.controls.extend(
                        [
                            ft.Row(
                                expand=2,
                                controls=[
                                    ft.Text(
                                        "ЭЦП:", color=ft.Colors.BLUE_ACCENT_700, size=18
                                    )
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Тип ЭЦП:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.type_ecp}",
                                        color=defaultFontColor,
                                        expand=2,
                                        size=18,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Статус ЭЦП:",
                                        color=ft.Colors.BLUE,
                                        expand=2,
                                        size=18,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.status_ecp}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Место установки:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.install_location}",
                                        color=defaultFontColor,
                                        expand=2,
                                        size=18,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Место хранения:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.storage_location}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к СБИС:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.sbis}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к ЧЗ:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.chz}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к Диадок:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.diadok}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к ФНС:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.fns}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к отчетности:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.report}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Прим. к фед.рес:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.fed_resours}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{ecp_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                            ),
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="pink600",
                                        icon_size=30,
                                        tooltip="Удалить ЭЦП",
                                        on_click=lambda e: self.open_delete_ecp_dialog(
                                            ecp_record.id
                                        ),
                                    ),
                                ],
                            ),
                        ]
                    )
                self.page.update()

            # Если у сотрудника есть КриптоПро
            if employee.kriptos:
                self.employee_info_right.controls.append(
                    ft.Divider(color=defaultBgColor)
                )

                for kriptos_record in employee.kriptos:
                    finish_date = kriptos_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )

                    self.employee_info_right.controls.extend(
                        [
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.Text(
                                        "Кпр-csp",
                                        color=ft.Colors.BLUE_ACCENT_700,
                                        size=18,
                                    )
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "Место установки:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.install_location}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Имя комп:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.licens_type}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Версия лицензии:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.version}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        f"{kriptos_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                expand=2,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="pink600",
                                        icon_size=30,
                                        tooltip="Удалить криптопро",
                                        on_click=lambda e: self.open_delete_kpr_dialog(
                                            kriptos_record.id
                                        ),
                                    ),
                                ],
                            ),
                        ]
                    )

            if employee.mchd:
                self.employee_info_right.controls.append(
                    ft.Divider(color=defaultBgColor)
                )

                for mchd_record in employee.mchd:
                    finish_date = mchd_record.finish_date
                    days_left = (finish_date - datetime.now().date()).days
                    finish_date_color = (
                        ft.Colors.RED if days_left <= 20 else defaultFontColor
                    )

                    self.employee_info_right.controls.extend(
                        [
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.Text(
                                        "МЧД",
                                        color=ft.Colors.BLUE_ACCENT_700,
                                        size=18,
                                    )
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Внутренний номер доверенност:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        value=f"{mchd_record.organiazation_dov_num}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Номер доверенности ФНС:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        value=f"{mchd_record.fns_dov_num}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Дата начала:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        value=f"{mchd_record.start_date.strftime('%d.%m.%Yг.')}",
                                        color=defaultFontColor,
                                        size=18,
                                        expand=2,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Дата окончания:",
                                        color=ft.Colors.BLUE,
                                        size=18,
                                        expand=2,
                                    ),
                                    ft.Text(
                                        value=f"{mchd_record.finish_date.strftime('%d.%m.%Yг.')}",
                                        color=finish_date_color,
                                        size=18,
                                        expand=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="pink600",
                                        icon_size=30,
                                        tooltip="Удалить мчд",
                                        on_click=lambda e: self.open_delete_mchd_dialog(
                                            mchd_record.id
                                        ),
                                    ),
                                ],
                            ),
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.ElevatedButton(
                                        text="сохранить xml",
                                        icon=ft.Icons.DOWNLOAD,
                                        tooltip="загрузить xml файл",
                                        on_click=lambda e, mchd_id=mchd_record.id: self.download_mchd_xml(
                                            e, mchd_id=mchd_record.id
                                        ),
                                    )
                                ],
                            ),
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.ElevatedButton(
                                        text="сохранить sig",
                                        icon=ft.Icons.DOWNLOAD,
                                        on_click=lambda e, mchd_id=mchd_record.id: self.download_mchd_sig(
                                            e, mchd_id=mchd_record.id
                                        ),
                                    )
                                ],
                            ),
                        ]
                    )
                    result_info_mchd = self.show(mchd_id=mchd_record.id)
                    for val in result_info_mchd.values():
                        code_power = val.get("code_power", "-")
                        code_full = val.get("code_full", "-")
                        description = val.get("description", "-")

                        self.employee_info_right.controls.extend(
                            [
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            "Код классификатора",
                                            color=defaultFontColor,
                                            size=16,
                                            expand=2,
                                        ),
                                        ft.Text(
                                            code_power,
                                            color=defaultFontColor,
                                            size=16,
                                            expand=3,
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            "Код полномочия",
                                            color=defaultFontColor,
                                            size=16,
                                            expand=2,
                                        ),
                                        ft.Text(
                                            code_full,
                                            color=defaultFontColor,
                                            size=16,
                                            expand=3,
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            "Описание",
                                            color=defaultFontColor,
                                            size=16,
                                            expand=2,
                                        ),
                                        ft.Text(
                                            description,
                                            color=defaultFontColor,
                                            size=16,
                                            expand=3,
                                        ),
                                    ]
                                ),
                                ft.Divider(color=defaultBgColor),
                            ]
                        )

            self.page.update()

        except Exception as ex:
            self.result_text.value = f"Произошла ошибка: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            self.page.update()

        self.result_text = ft.Text("")

    def reset_state(self):
        self.employee_info_right.controls.clear()
        self.employee_info_left.controls.clear()
        self.employee_info_right.clean()
        self.employee_info_left.clean()
        self.result_text.value = ""
        self.result_text.value = ""
        self.selected_ecp_id = None
        self.selected_kpr_id = None
        self.selected_mchd_id = None
        empl_id = self.page.session.get("empl_id")
        if empl_id is not None:
            self.page.session.remove("empl_id")

    def go_home(self, e):
        self.reset_state()
        self.page.go("/")
        self.page.session.clear()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Информация о сотруднике"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        self.submit_form()

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
            "/employees_info",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Левая часть
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                controls=[
                                    ft.TextButton(
                                        "Домой",
                                        icon=ft.Icons.HOME,
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.ControlState.HOVERED: ft.Colors.BLUE,
                                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(12),
                                        ),
                                        on_click=lambda e: self.go_home(e),
                                    ),
                                    sidebar_menu,
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                        ),
                        ft.Container(
                            expand=7,
                            alignment=ft.alignment.bottom_left,
                            padding=ft.padding.Padding(
                                left=40, top=60, right=40, bottom=60
                            ),
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        self.result_text,
                                        self.employee_info_left,
                                        self.employee_info_right,
                                    ]
                                ),
                            ),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
