# from datetime import datetime
# from math import ceil
#
# import flet as ft
# from flet_route import Params, Basket
#
# from crud.ecpies import delete_ecp
# from crud.employees import get_all_employees_ecp_kripto, get_all_employees, get_one_employee_with_relation, \
#     delete_employee
# from crud.kriptoproies import delete_kpr
# from utils.style import *
# # большой класс
# # todo def show_detailed_employee_info - метод для отображения детальной информации о сотруднике
# # todo def show_employees_with_current_licenses - метод для отображения информации о сотруднике с его лицензиями ecp и kpr
# # todo def show_employees_with_expired_licenses - метод для отображения информации о сотруднике с истекшими лицензиями
# # todo def show_all_employees - отображение всех сотрудников
# class DashboardPage:
#
#     def __init__(self, page: ft.Page):
#         self.add_ecp_button = ft.ElevatedButton(
#             text="Добавить эцп",
#             on_click=self.add_ecp_page,  # переход на страницу добавлния эцп
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#             height=40,
#             # visible=False,
#         )
#
#         self.add_kpr_button = ft.ElevatedButton(
#             text="Добавить криптопро",
#             on_click=self.add_kpr_page,  # переход на страницу добавлния кпр
#             bgcolor=defaultBgColor,
#             color=defaultFontColor,
#             height=0,
#             # visible=False
#         )
#         self.employee_info_right = ft.ListView(
#             controls=[],
#             expand=True,
#             divider_thickness=True,
#             padding=ft.Padding(left=0, top=0, right=0, bottom=0),
#             # auto_scroll=True,  # Автопрокрутка
#         )
#         self.employee_info_left = ft.ListView(
#             controls=[],
#             divider_thickness=True,
#             # item_extent=300,a
#             padding=ft.Padding(left=0, top=0, right=0, bottom=0),
#         )
#         self.pagination_controls = ft.Row()
#         self.page = page  # основная страница приложения
#
#         # Элементы интерфейса
#         self.result_text = ft.Text("", color=ft.Colors.WHITE)
#         self.employee_info = ft.ListView(expand=True)  # список сотрудников
#         self.current_page = 1
#         self.page_size = 15
#         self.total_pages = 1
#         self.result_text = ft.Text()
#         self.show_employees_with_current_licenses()
#         self.filter_menu_bar = ft.MenuBar(
#             controls=[
#                 ft.SubmenuButton(
#                     # content=ft.Text("Действующие"),
#                     controls=[
#                         ft.MenuItemButton(
#                             content=ft.Text("действующие"),
#                             on_click=self.show_employees_with_current_licenses,
#                         ),
#                         ft.MenuItemButton(
#                             content=ft.Text("все сотрудники"),
#                             on_click=self.go_current_licenses  #
#                         ),
#                         ft.MenuItemButton(
#                             content=ft.Text("просроченные"),
#                             on_click=self.go_easisted_licenses  # todo реализовать
#                         ),
#                     ],
#                 )
#             ]
#         )
#         self.delete_employee_dialog = ft.CupertinoAlertDialog(
#             title=ft.Text("Удаление сотрудника"),
#             # modal=True,
#             content=ft.Text("Вы хотите удалить сотрудника?"),
#             actions=[
#                 ft.CupertinoDialogAction(
#                     text="Да",
#                     is_destructive_action=True,
#                     on_click=lambda e: self.delete_employee() # self.delete_employee
#                 ),
#                 ft.CupertinoDialogAction(
#                     text="Нет",
#                     is_default_action=True,
#                     on_click=lambda e: self.del_empl(e)),
#             ],
#
#         )
#     def del_empl(self,e):
#         # self.delete_employee_dialog.open = False
#         #self.page.go("/employees_info")
#         self.delete_employee_dialog.open = False
#         #self.page.go("/employees_info")
#         self.show_employee_info(empl_id=self.page.session.get("empl_id"))
#         self.page.update()
#
#     def delete_employee(self, emp):
#
#         try:
#             # Переменная для хранения найденного сотрудника
#             employee = emp
#             employee_id = employee.id
#             # Удаляем сотрудника
#             delete_employee(employee_id=employee_id)
#
#             self.delete_employee_dialog.open = False
#             # self.dashboard_page.show_employees_with_current_licenses()
#             # self.page.go("/")
#             self.show_employees_with_current_licenses() # отображение сотрудников с лицензиями
#
#         except Exception as ex:
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#         self.show_employees_with_current_licenses()
#
#     def delete_ecp_(self, ecp_id):
#         try:
#             print(f'delete_===', ecp_id)
#             print(f"Удаление с ID: {ecp_id}")
#
#             delete_ecp(ecp_id)  # Вызываем функцию удаления
#
#             # Успешное завершение
#             self.result_text.value = f"ЭЦП успешно удален."
#             self.result_text.color = ft.Colors.GREEN
#             self.page.update()
#         except Exception as ex:
#             print(f"Ошибка при удалении ЭЦП: {str(ex)}")
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#         # Обновляем форму после завершения
#         self.show_employees_with_current_licenses()
#
#     def add_ecp_page(self, employee_id, employee_name):
#         print(employee_id)
#         print(employee_name)
#
#         self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
#         self.page.session.set("employee_name", employee_name)  # установка имени для вывода на странице добавления
#         # self.page.go(f"/update_employees?employee_id={employee_id}")
#         self.page.go(f"/add_ecp_find_empl")
#         self.page.update()
#
#     # переход на страницу добавлния криптопро
#     def add_kpr_page(self, employee_id, employee_name):
#         print(employee_id)
#         print(employee_name)
#
#         self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
#         self.page.session.set("employee_name", employee_name)
#
#         # self.page.go(f"/update_employees?employee_id={employee_id}")
#         self.page.go(f"/add_kriptopro_find_empl")
#         self.page.update()
#
#     def open_dialog_delete_employee(self, employee):
#         # self.delete_employee_dialog.actions[0].on_click = delete_employee(employee_id=employee.id)
#         self.delete_employee_dialog.actions[0].on_click = lambda e: self.delete_employee(employee)
#         self.page.open(self.delete_employee_dialog)
#
#     # def go_home(self, e):
#     #     self.page.go("/") # отображение сотрудников с лицензиями
#
#     def go_current_licenses(self, e):
#         # self.page.go("/dashboard_current_licens") # todo запуск метода сотрудниками со всеми действующими лицензиям
#         self.show_employees_with_current_licenses() #
#
#     def go_easisted_licenses(self, e):
#         # self.page.go("/dashboard_easisted_licenses") # todo запуск метода сотрудниками со всеми просрченными лицензиям
#         self.show_employees_with_easisted_licenses()
#
#     def update_pagination_controls(self):
#         """Обновляет элементы управления пагинацией."""
#         self.pagination_controls.controls.clear()
#         self.pagination_controls.controls.extend([
#             ft.Button(
#                 "Предыдущая",
#                 color=menuFontColor,
#                 on_click=lambda e: self.go_to_page(self.current_page - 1),
#                 disabled=self.current_page <= 1  # Отключаем кнопку на первой странице
#             ),
#             ft.Text(f"Страница {self.current_page} из {self.total_pages}", color=ft.Colors.WHITE),
#             ft.ElevatedButton(
#                 "Следующая",
#                 color=menuFontColor,
#                 on_click=lambda e: self.go_to_page(self.current_page + 1),
#                 disabled=self.current_page >= self.total_pages  # Отключаем кнопку на последней странице
#             )
#         ])
#
#     # переход на страницу обновления данных сотрудника
#     def edit_employee(self, employee_id, employee_name):
#         print(employee_id)
#         print(employee_name)
#
#         self.page.session.set("employee_id", employee_id)  # установка id для глобальной страницы
#
#         # self.page.go(f"/update_employees?employee_id={employee_id}")
#         self.page.go(f"/update_employees")
#         self.page.update()
#
#     def show_employee_info(self, empl_id: int):
#         self.page.session.set("empl_id", empl_id)
#         # self.employee_info_right.controls.clear() # перед отобрж очищаем правую панель
#         self.show_detailed_employee_info()
#
#         # self.page.go(f"/employees_info")
#
#     # метод получения сотрудников с действующими лицензиями
#     def show_employees_with_current_licenses(self):
#         self.employee_info.controls.clear()
#         self.employee_info.controls.clear()
#         self.employee_info_right.controls.clear()
#         try:
#             employees_current_list = get_all_employees_ecp_kripto() # получение всех сотрудников со всеми лицензиями
#             # employees = get_all_employees()
#             if not employees_current_list:
#                 self.result_text.value = "Нет сотрудников в базе."
#                 self.result_text.color = ft.Colors.RED
#                 # self.employee_info.controls.clear()
#                 self.page.update()
#                 return
#
#
#             # Функция для получения минимальной даты окончания ЭЦП
#             def get_min_ecp_date(employee):
#                 dates = [
#                     ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                 datetime) else ecp_record.finish_date
#                     for ecp_record in (employee.ecp or [])  # Если нет записей, используем пустой список
#                 ]
#                 return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату
#
#             # Функция для получения минимальной даты окончания КриптоПро
#             def get_min_kripto_date(employee):
#                 dates = [
#                     kripto_record.finish_date.date() if isinstance(kripto_record.finish_date,
#                                                                    datetime) else kripto_record.finish_date
#                     for kripto_record in (employee.kriptos or [])
#                 ]
#                 return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату
#
#             # Функция для получения минимальной даты из ЭЦП и КриптоПро
#             def get_min_ecp_kripto_date(employee):
#                 ecp_date = get_min_ecp_date(employee)
#                 kripto_date = get_min_kripto_date(employee)
#
#                 return min(ecp_date, kripto_date)  # Берем минимальную из двух дат
#
#
#             # Сортировка сотрудников
#             employees_current_list.sort(key=lambda emp_tuple: get_min_ecp_kripto_date(emp_tuple[0]))
#
#
#             # Расчёт данных для текущей страницы
#             self.total_pages = ceil(len(employees_current_list) / self.page_size)
#             start_index = (self.current_page - 1) * self.page_size
#             end_index = start_index + self.page_size
#             page_employees = employees_current_list[start_index:end_index]
#
#             self.employee_info.controls.clear()
#
#             # Заголовки таблицы
#             data_table = ft.DataTable(
#                 columns=[
#                     ft.DataColumn(ft.Text("Сотрудник         ", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания эцп", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания кпр", color=ft.Colors.WHITE, size=22)),
#                 ],
#                 rows=[],
#             )
#
#             for employee_tuple in page_employees:
#                 employee = employee_tuple[0]
#
#                 # Сбор информации об ЭЦП
#                 ecp_data = []
#                 if employee.ecp:
#                     for ecp_record in employee.ecp:
#                         finish_date = (
#                             ecp_record.finish_date.date()
#                             if isinstance(ecp_record.finish_date, datetime)
#                             else ecp_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days # попадают только те, у которых дата больше нуля
#                         if days_left > 0:  # Фильтрация истекших записей
#                             ecp_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 ecp_info = "\n".join(ecp_data) if ecp_data else "Нет данных"
#
#                 # Сбор информации о КриптоПро
#                 kripto_data = []
#                 if employee.kriptos:
#                     for kripto_record in employee.kriptos:
#                         finish_date = (
#                             kripto_record.finish_date.date()
#                             if isinstance(kripto_record.finish_date, datetime)
#                             else kripto_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days
#                         if days_left > 0:  # Фильтрация истекших записей
#                             kripto_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"
#
#                 # Если у сотрудника нет активных лицензий, не добавлять его в таблицу
#                 if not ecp_data and not kripto_data:
#                     continue
#
#                 # Добавление строки с данными сотрудника
#                 data_table.rows.append(
#                     ft.DataRow(
#                         cells=[
#                             ft.DataCell(ft.Text(employee.full_name, color=ft.Colors.WHITE, size=18)),
#                             ft.DataCell(ft.Text(ecp_info,
#                                                 color=ft.Colors.GREEN if "дней осталось" in ecp_info else ft.Colors.RED,
#                                                 size=18)),
#                             ft.DataCell(ft.Text(kripto_info,
#                                                 color=ft.Colors.GREEN if "дней осталось" in kripto_info else ft.Colors.RED,
#                                                 size=18)),
#                         ],
#                         # Обработчик нажатия
#                         on_long_press=lambda e, emp_id=employee.id: self.show_employee_info(emp_id),
#                     )
#                 )
#
#             # Добавление таблицы в контейнер
#             self.employee_info.controls.append(data_table)
#
#             # Обновление пагинации и страницы
#             self.update_pagination_controls()
#             self.page.update()
#
#
#         except Exception as ex:
#             import traceback
#             self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             print(traceback.format_exc())  # Вывод трейсбэка для отладки
#             self.page.update()
#
#
#
#     def go_to_page(self, page_number):
#         """Переход к указанной странице."""
#         if 1 <= page_number <= self.total_pages:
#             self.current_page = page_number
#             self.load_employees()
#             # self.show_employees_with_current_licenses()
#
#
#     def view(self, page: ft.Page, params: Params, basket: Basket):
#         page.title = "Домашняя страница"
#         page.window.width = defaultWithWindow
#         page.window.height = defaultHeightWindow
#         page.window.min_width = 1000
#         page.window.min_height = 600
#         page.scroll = "adaptive"
#
#         style_menu = ft.ButtonStyle(color='#FBF0F0',
#                                     icon_size=30,
#                                     text_style=ft.TextStyle(size=16),
#                                     overlay_color=defaultBgColor,
#                                     shadow_color=defaultBgColor,
#                                     )
#
#         # Панель сайдбар
#         sidebar_menu = ft.Container(
#
#             padding=ft.padding.symmetric(0, 13),
#             content=ft.Column(
#                 controls=[
#                     ft.Text("МЕНЮ", color=menuFontColor, size=18),
#                     ft.TextButton("Поиск сотрудника", icon=ft.Icons.SEARCH, style=style_menu,
#                                   on_click=lambda e: self.page.go("/employees")),
#                     ft.TextButton("Добавить сотрудника", icon=ft.Icons.ADD, style=style_menu,
#                                   on_click=lambda e: self.page.go("/add_employees")),
#
#                 ]
#             )
#         )
#
#         return ft.View(
#             "/dashboard",
#             controls=[
#                 ft.Row(
#                     expand=True,
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     controls=[
#                         # Левая сторона
#                         ft.Container(
#                             expand=2,
#                             content=ft.Column(
#                                 controls=[
#                                     sidebar_menu
#                                 ]
#                             ),
#                             bgcolor=secondaryBgColor,
#                             # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
#                             padding=ft.padding.all(10),  # Внутренние отступы
#                         ),
#                         # Контейнер с данными сотрудников
#                         ft.Container(
#                             expand=4,
#                             content=ft.Column(
#                                 controls=[
#                                     ft.Row(
#                                         controls=[
#                                             self.filter_menu_bar
#                                         ]
#                                     ),
#                                     # self.filter_menu_bar,
#                                     self.result_text,
#                                     ft.Divider(),
#                                     self.employee_info,
#                                     ft.Divider(),
#                                     # self.employee_info_right,
#                                     # ft.Divider(),
#                                     self.pagination_controls
#                                 ]
#                             ),
#                             bgcolor=defaultBgColor,
#                             # border=ft.border.all(1, "#808080"),  # Рамка с серым цветом
#                             padding=ft.padding.all(10),  # Внутренние отступы
#                         )
#                     ]
#                 )
#             ],
#             bgcolor=defaultBgColor,
#             padding=0,
#         )
#
#     def show_detailed_employee_info(self):
#         self.employee_info_right.controls.clear()
#         self.employee_info.controls.clear() # очищаем таблицу сотрудников
#         self.result_text.value = ""
#
#         self.page.update()
#
#         try:
#             # Получаем данные о сотруднике
#             employee = self.page.session.get("empl_id")
#             employee = get_one_employee_with_relation(employee_id=employee)
#
#             print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")
#             print(f"Найден сотрудник: {employee.full_name}, {employee.position}, {employee.com_name}")
#             self.result_text.color = ft.Colors.GREEN
#             self.add_ecp_button.visible = True
#             self.add_kpr_button.visible = True
#             # Очистка предыдущего содержимого
#             self.employee_info_left.controls.clear()
#             self.employee_info_right.controls.clear()
#             self.employee_info.controls.clear()
#
#             # Заполняем левую панель с основной информацией
#             self.employee_info.controls.extend(
#                 [
#                     ft.Row(
#                         controls=[
#                             ft.Text(f"Сотрудник:              ", color=ft.Colors.BLUE_ACCENT_700, size=22, ),
#                             ft.Text(f"{employee.full_name}", color=defaultFontColor, size=18)
#                         ],
#                         alignment=ft.MainAxisAlignment.START,
#                         spacing=10
#                     ),
#                     ft.Row(
#                         controls=[
#                             ft.Text(f"Должность:                    ", color=ft.Colors.BLUE, size=18, ),
#                             ft.Text(f"{employee.position}", color=defaultFontColor, size=18)
#                         ],
#                         alignment=ft.MainAxisAlignment.START,
#                         spacing=10
#                     ),
#                     ft.Row(
#                         controls=[
#                             ft.Text(f"Имя компьютера:         ", color=ft.Colors.BLUE, size=18, ),
#                             ft.Text(f"{employee.com_name}", color=defaultFontColor, size=18)
#                         ],
#                         alignment=ft.MainAxisAlignment.START,
#                         spacing=10
#                     ),
#                     ft.Row(alignment=ft.MainAxisAlignment.START, controls=[
#                         ft.IconButton(
#                             icon=ft.Icons.DELETE_FOREVER_ROUNDED,
#                             icon_color="pink600",
#                             icon_size=30,
#                             tooltip="удалить сотрудника",
#                             on_click=lambda e: self.open_dialog_delete_employee(employee)
#                         ),
#                     ]),
#                     ft.Row(
#                         alignment=ft.MainAxisAlignment.START,
#                         controls=[
#                             ft.FilledButton(
#                                 "обновить данные",
#                                 bgcolor=defaultBgColor,
#                                 tooltip="обновление данных сотрудника",
#                                 icon=ft.Icons.UPDATE,
#                                 # bgcolor='#F5EEE6',
#                                 height=40,
#                                 on_click=lambda e: self.edit_employee(
#                                     employee_id=employee.id,
#                                     employee_name=employee.full_name
#                                 )
#
#                             )
#                         ]
#                     ),
#                     ft.Row(
#                         alignment=ft.MainAxisAlignment.START,
#                         controls=[
#                             ft.FilledButton(
#                                 "Добавить эцп",
#                                 icon=ft.Icons.ADD_BOX,
#                                 bgcolor=defaultBgColor,
#                                 tooltip="Добавить новый эцп",
#                                 on_click=lambda e: self.add_ecp_page(
#                                     employee_id=employee.id, employee_name=employee.full_name
#                                 ),
#                             )
#                             # self.add_ecp_button,
#                         ]),
#                     ft.Row(
#                         alignment=ft.MainAxisAlignment.START,
#                         controls=[
#                             # self.add_kpr_button
#                             ft.FilledButton(
#                                 "Добавить кпр",
#                                 icon=ft.Icons.ADD_BOX,
#                                 bgcolor=defaultBgColor,
#                                 tooltip="Добавить новый криптопро",
#                                 on_click=lambda e: self.add_kpr_page(
#                                     employee_id=employee.id, employee_name=employee.full_name
#                                 ),
#                             )
#                         ]),
#                     ft.Row(controls=[
#                         ft.Text("")
#                     ]),
#
#                     ft.Divider(color=defaultBgColor),
#                 ])
#
#             self.page.update()
#
#             # Если у сотрудника есть ЭЦП
#             if employee.ecp:
#                 for ecp_record in employee.ecp:
#                     finish_date = (
#                         ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                     datetime) else ecp_record.finish_date
#                     )
#                     days_left = (finish_date - datetime.now().date()).days
#                     finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
#
#                     self.employee_info.controls.extend([
#                         ft.Row(controls=[
#                             ft.Text("ЭЦП:", color=ft.Colors.BLUE_ACCENT_700, size=18)
#                         ]),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Тип ЭЦП                           ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.type_ecp}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Статус ЭЦП:                    ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.status_ecp}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Место установки:         ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.install_location}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Место хранения:          ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.storage_location}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к СБИС:               ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.sbis}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к ЧЗ:                     ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.chz}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к Диадок:           ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.diadok}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к ФНС:                 ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.fns}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к отчетности:   ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.report}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Прим. к фед.рес:          ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.fed_resours}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Дата начала:                 ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.start_date.strftime('%d.%m.%Yг.')}", color=defaultFontColor,
#                                         size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Дата окончания:         ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{ecp_record.finish_date.strftime('%d.%m.%Yг.')}", color=finish_date_color,
#                                         size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#
#                                 ft.IconButton(
#                                     icon=ft.Icons.DELETE_FOREVER_ROUNDED,
#                                     icon_color="pink600",
#                                     icon_size=30,
#                                     tooltip="Удалить ЭЦП",
#                                     on_click=lambda e: self.delete_ecp_(ecp_record.id)
#                                 ),
#                             ]
#                         ),
#                         ft.Divider(color=defaultBgColor),
#                     ])
#                 self.page.update()
#
#             # Если у сотрудника есть КриптоПро
#             if employee.kriptos:
#                 self.employee_info.controls.append(ft.Divider(color=defaultBgColor))
#
#                 for kriptos_record in employee.kriptos:
#                     finish_date = (
#                         kriptos_record.finish_date.date() if isinstance(kriptos_record.finish_date,
#                                                                         datetime) else kriptos_record.finish_date
#                     )
#                     days_left = (finish_date - datetime.now().date()).days
#                     finish_date_color = ft.Colors.RED if days_left <= 20 else defaultFontColor
#
#                     self.employee_info.controls.extend([
#                         ft.Row(
#                             controls=[
#                                 ft.Text("Кпр-csp", color=ft.Colors.BLUE_ACCENT_700, size=18)
#                             ]),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Место установки:         ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{kriptos_record.install_location}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Имя комп:                        ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{kriptos_record.licens_type}", color=defaultFontColor, size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Версия лицензии:        ", color=ft.Colors.BLUE, size=18),
#                                 ft.Text(f"{kriptos_record.version}", color=defaultFontColor, size=18)
#                             ]
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Дата начала:                  ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{kriptos_record.start_date.strftime('%d.%m.%Yг.')}", color=defaultFontColor,
#                                         size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.Text(f"Дата окончания:           ", color=ft.Colors.BLUE, size=18, ),
#                                 ft.Text(f"{kriptos_record.finish_date.strftime('%d.%m.%Yг.')}", color=finish_date_color,
#                                         size=18)
#                             ],
#                             alignment=ft.MainAxisAlignment.START,
#                             spacing=10
#                         ),
#                         ft.Row(
#                             controls=[
#                                 ft.IconButton(
#                                     icon=ft.Icons.DELETE_FOREVER_ROUNDED,
#                                     icon_color="pink600",
#                                     icon_size=30,
#                                     tooltip="Удалить криптопро",
#                                     on_click=lambda e: self.delete_kpr_(kriptos_record.id)
#                                 ),
#                             ]
#                         ),
#                         ft.Divider(color=defaultBgColor),
#                     ])
#                 self.page.update()
#
#         except ValueError as er:
#             self.result_text.value = str(er)
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#         except Exception as ex:
#             self.result_text.value = f"Произошла ошибка: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#         self.result_text = ft.Text("")
#         # self.found_employee = None
#
#
#     def delete_kpr_(self, kpr_id):
#         try:
#             print(f'delete_===', kpr_id)
#             print(f"Удаление с ID: {kpr_id}")
#
#             delete_kpr(kpr_id)  # Вызываем функцию удаления
#
#             # Успешное завершение
#             self.result_text.value = f"КПР успешно удален."
#             self.result_text.color = ft.Colors.GREEN
#             self.delete_employee_dialog.open = False,
#             self.page.update()
#         except Exception as ex:
#             print(f"Ошибка при удалении КПР: {str(ex)}")
#             self.result_text.value = f"Ошибка при удалении: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             self.page.update()
#
#         # Обновляем форму после завершения
#         self.load_employees()
#
#     def show_employees_with_easisted_licenses(self):
#         self.employee_info.controls.clear()
#         self.employee_info.controls.clear()
#         self.employee_info_right.controls.clear()
#         self.page.update()
#         try:
#             employees = get_all_employees_ecp_kripto()
#             if not employees:
#                 self.result_text.value = "Нет сотрудников в базе."
#                 self.result_text.color = ft.Colors.RED
#                 self.employee_info.controls.clear()
#                 self.page.update()
#                 return
#
#             # Фильтрация сотрудников с истекшими лицензиями
#             def license_expired(employee):
#                 # Проверяем, если хотя бы одна лицензия истекла
#                 for ecp_record in (employee.ecp or []):
#                     finish_date = ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                               datetime) else ecp_record.finish_date
#                     if (finish_date - datetime.now().date()).days <= 0:  # Если срок истек
#                         return True
#
#                 for kripto_record in (employee.kriptos or []):
#                     finish_date = kripto_record.finish_date.date() if isinstance(kripto_record.finish_date,
#                                                                                  datetime) else kripto_record.finish_date
#                     if (finish_date - datetime.now().date()).days <= 0:  # Если срок истек
#                         return True
#
#                 return False
#
#             # Фильтруем сотрудников по условию истечения срока лицензий
#             employees = [emp_tuple for emp_tuple in employees if license_expired(emp_tuple[0])]
#
#             if not employees:
#                 self.result_text.value = "Нет сотрудников с истекшими лицензиями."
#                 self.result_text.color = ft.Colors.RED
#                 self.employee_info.controls.clear()
#                 self.page.update()
#                 return
#
#             # Сортировка сотрудников по минимальной дате окончания ЭЦП
#             def get_min_ecp_date(employee):
#                 if employee.ecp:
#                     dates = [
#                         ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                     datetime) else ecp_record.finish_date
#                         for ecp_record in employee.ecp
#                     ]
#                     return min(dates) if dates else datetime.max.date()
#                 return datetime.max.date()
#
#             employees.sort(key=lambda emp_tuple: get_min_ecp_date(emp_tuple[0]))
#
#             # Расчёт данных для текущей страницы
#             self.total_pages = ceil(len(employees) / self.page_size)
#             start_index = (self.current_page - 1) * self.page_size
#             end_index = start_index + self.page_size
#             page_employees = employees[start_index:end_index]
#
#             self.employee_info.controls.clear()
#
#             # Заголовки таблицы
#             data_table = ft.DataTable(
#                 columns=[
#                     ft.DataColumn(ft.Text("Сотрудник", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания эцп", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания кпр", color=ft.Colors.WHITE, size=22)),
#                 ],
#                 rows=[],
#             )
#
#             for employee_tuple in page_employees:
#                 employee = employee_tuple[0]
#
#                 # Сбор информации об ЭЦП
#                 ecp_data = []
#                 if employee.ecp:
#                     for ecp_record in employee.ecp:
#                         finish_date = (
#                             ecp_record.finish_date.date()
#                             if isinstance(ecp_record.finish_date, datetime)
#                             else ecp_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days
#                         ecp_data.append(
#                             f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней прошло)" if days_left <= 0 else f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 ecp_info = "\n".join(ecp_data) if ecp_data else "Нет данных"
#
#                 # Сбор информации о КриптоПро
#                 kripto_data = []
#                 if employee.kriptos:
#                     for kripto_record in employee.kriptos:
#                         finish_date = (
#                             kripto_record.finish_date.date()
#                             if isinstance(kripto_record.finish_date, datetime)
#                             else kripto_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days
#                         kripto_data.append(
#                             f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней прошло)" if days_left <= 0 else f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"
#
#                 # Добавление строки с данными сотрудника
#                 data_table.rows.append(
#                     ft.DataRow(
#                         cells=[
#                             ft.DataCell(ft.Text(employee.full_name, color=ft.Colors.WHITE, size=18)),
#                             ft.DataCell(ft.Text(ecp_info,
#                                                 color=ft.Colors.RED if "дней прошло" in ecp_info else ft.Colors.GREEN,
#                                                 size=18)),
#                             ft.DataCell(ft.Text(kripto_info,
#                                                 color=ft.Colors.RED if "дней прошло" in kripto_info else ft.Colors.GREEN,
#                                                 size=18)),
#                         ],
#                         # Обработчик нажатия
#                         on_long_press=lambda e, emp_id=employee.id: self.show_employee_info(emp_id),
#                     )
#                 )
#
#             # Добавление таблицы в контейнер
#             self.employee_info.controls.append(data_table)
#
#             # Обновление пагинации и страницы
#             self.update_pagination_controls()
#             self.page.update()
#
#         except Exception as ex:
#             import traceback
#             self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             print(traceback.format_exc())  # Вывод трейсбэка для отладки
#             self.page.update()
#
#
#     def load_employees(self):
#
#         try:
#             employees = get_all_employees_ecp_kripto()
#             # employees = get_all_employees()
#             if not employees:
#                 self.result_text.value = "Нет сотрудников в базе."
#                 self.result_text.color = ft.Colors.RED
#                 self.employee_info.controls.clear()
#                 self.page.update()
#                 return
#
#
#             # Функция для получения минимальной даты окончания ЭЦП
#             def get_min_ecp_date(employee):
#                 dates = [
#                     ecp_record.finish_date.date() if isinstance(ecp_record.finish_date,
#                                                                 datetime) else ecp_record.finish_date
#                     for ecp_record in (employee.ecp or [])  # Если нет записей, используем пустой список
#                 ]
#                 return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату
#
#             # Функция для получения минимальной даты окончания КриптоПро
#             def get_min_kripto_date(employee):
#                 dates = [
#                     kripto_record.finish_date.date() if isinstance(kripto_record.finish_date,
#                                                                    datetime) else kripto_record.finish_date
#                     for kripto_record in (employee.kriptos or [])
#                 ]
#                 return min(dates, default=datetime.max.date())  # Если нет дат, возвращаем максимальную дату
#
#             # Функция для получения минимальной даты из ЭЦП и КриптоПро
#             def get_min_ecp_kripto_date(employee):
#                 ecp_date = get_min_ecp_date(employee)
#                 kripto_date = get_min_kripto_date(employee)
#
#                 return min(ecp_date, kripto_date)  # Берем минимальную из двух дат
#
#
#             # Сортировка сотрудников
#             employees.sort(key=lambda emp_tuple: get_min_ecp_kripto_date(emp_tuple[0]))
#
#
#             # Расчёт данных для текущей страницы
#             self.total_pages = ceil(len(employees) / self.page_size)
#             start_index = (self.current_page - 1) * self.page_size
#             end_index = start_index + self.page_size
#             page_employees = employees[start_index:end_index]
#
#             self.employee_info.controls.clear()
#
#             # Заголовки таблицы
#             data_table = ft.DataTable(
#                 columns=[
#                     ft.DataColumn(ft.Text("Сотрудник", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания эцп", color=ft.Colors.WHITE, size=22)),
#                     ft.DataColumn(ft.Text("Дата окончания кпр", color=ft.Colors.WHITE, size=22)),
#                 ],
#                 rows=[],
#             )
#
#             for employee_tuple in page_employees:
#                 employee = employee_tuple[0]
#
#                 # Сбор информации об ЭЦП
#                 ecp_data = []
#                 if employee.ecp:
#                     for ecp_record in employee.ecp:
#                         finish_date = (
#                             ecp_record.finish_date.date()
#                             if isinstance(ecp_record.finish_date, datetime)
#                             else ecp_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days
#                         if days_left > 0:  # Фильтрация истекших записей
#                             ecp_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 ecp_info = "\n".join(ecp_data) if ecp_data else "Нет данных"
#
#                 # Сбор информации о КриптоПро
#                 kripto_data = []
#                 if employee.kriptos:
#                     for kripto_record in employee.kriptos:
#                         finish_date = (
#                             kripto_record.finish_date.date()
#                             if isinstance(kripto_record.finish_date, datetime)
#                             else kripto_record.finish_date
#                         )
#                         days_left = (finish_date - datetime.now().date()).days
#                         if days_left > 0:  # Фильтрация истекших записей
#                             kripto_data.append(f"{finish_date.strftime('%d.%m.%Yг.')} ({days_left} дней осталось)")
#
#                 kripto_info = "\n".join(kripto_data) if kripto_data else "Нет данных"
#
#                 # Если у сотрудника нет активных лицензий, не добавлять его в таблицу
#                 if not ecp_data and not kripto_data:
#                     continue
#
#                 # Добавление строки с данными сотрудника
#                 data_table.rows.append(
#                     ft.DataRow(
#                         cells=[
#                             ft.DataCell(ft.Text(employee.full_name, color=ft.Colors.WHITE, size=18)),
#                             ft.DataCell(ft.Text(ecp_info,
#                                                 color=ft.Colors.GREEN if "дней осталось" in ecp_info else ft.Colors.RED,
#                                                 size=18)),
#                             ft.DataCell(ft.Text(kripto_info,
#                                                 color=ft.Colors.GREEN if "дней осталось" in kripto_info else ft.Colors.RED,
#                                                 size=18)),
#                         ],
#                         # Обработчик нажатия
#                         on_long_press=lambda e, emp_id=employee.id: self.show_employee_info(emp_id),
#                     )
#                 )
#
#             # Добавление таблицы в контейнер
#             self.employee_info.controls.append(data_table)
#
#             # Обновление пагинации и страницы
#             self.update_pagination_controls()
#             self.page.update()
#
#
#         except Exception as ex:
#             import traceback
#             self.result_text.value = f"Ошибка при загрузке данных: {str(ex)}"
#             self.result_text.color = ft.Colors.RED
#             print(traceback.format_exc())  # Вывод трейсбэка для отладки
#             self.page.update()
