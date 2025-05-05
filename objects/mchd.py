
import os
import xml.etree.ElementTree as ET
import flet as ft
from datetime import datetime
from crud.mchd import create_mchd
from schemas.mchd import MchdAdd

UPLOAD_DIR = "assert/upload"

class Mchd:
    def __init__(self):

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        """Обработчик выбора файла"""

        if not e.files:
            self.result_text.value = "Файл не выбран"
            self.result_text.update()
            return
        file_path = e.files[0].path


        if not file_path.lower().endswith(".xml"):
            self.result_text.value = "Ошибка, загрузите xml-файл"
            self.result_text.update()
            return

            # Создаем директорию, если её нет
        os.makedirs(UPLOAD_DIR,exist_ok=True)

            # Сохраняем файл
        save_path = os.path.join(UPLOAD_DIR, os.path.basename(file_path))
        try:
            with open(save_path, "wb") as f:
                f.write(open(file_path, "rb").read())
        except IOError as err:
            self.result_text.value = f"Ошибка сохранения файла {err}"
            self.result_text.update()
            return

        # Парсим и сохраняем XML
        result = self.parse_and_save_xml(save_path)
        self.result_text.value = result
        self.result_text.update()



    def parse_and_save_xml(self, file_path):
        """Парсинг XML и сохранение в БД"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            ns = {"ns": "urn://x-artefacts/EMCHD_1"}

            doc = root.find("ns:Документ/ns:Довер/ns:СвДов", ns)
            if doc is None:
                return "Ошибка: Некорректный XML-файл!"

            # Извлекаем данные из XML
            fns_dov_num = doc.attrib.get("НомДовер") # номер доверенноси фнс
            start_date_str = doc.attrib.get("ДатаВыдДовер") # датат начала
            finish_date_str = doc.attrib.get("СрокДейст") # дата окончания

            # Преобразуем даты в datetime
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                finish_date = datetime.strptime(finish_date_str, "%Y-%m-%d").date()
            except ValueError:
                start_date = datetime(1900, 1, 1).date()
                finish_date = datetime(1900, 1, 1).date()

            org = root.find(".//ns:СвДов", ns)
            org_dov_num = org.attrib.get("ВнНомДовер") if org is not None else "0"

            powers = root.findall(".//ns:СвПолн/ns:МашПолн", ns)
            name_of_powers = ", ".join([p.attrib.get("НаимПолн", "") for p in powers])

            # Читаем содержимое файла для сохранения в БД
            with open(file_path, "rb") as f:
                file_content = f.read()

            # Получаем ID сотрудника из сессии
            employee_id = self.page.session.get("employee_id")
            print(f"IN MCHD ADD {employee_id}")
            oMcdAdd = MchdAdd(
                    employees_id=employee_id,
                    organiazation_dov_num=org_dov_num,
                    fns_dov_num=fns_dov_num,
                    start_date=start_date,
                    finish_date=finish_date,
                    file_mchd=file_content,
                    name_of_powers=name_of_powers,
                    )
            try:
                mcd = create_mchd(mchd_data=oMcdAdd)
                print(mcd)
                self.result_text.value = "Данные успешно добавлены"
            except Exception as e:
                self.result_text.value = f"Ошибка соединения: {str(e)}"
            finally:
                self.result_text.update()

        except Exception as e:
            return f"Ошибка обработки XML: {str(e)}"

    def view(self, page: ft.Page, params, basket):
        return ft.View(
            "/add_mchd",
            controls=[
                ft.ElevatedButton(
                    "Выбрать XML",
                    on_click=lambda _: self.pick_files_dialog.pick_files(
                    )
                ),
                self.result_text,
            ],
        )
