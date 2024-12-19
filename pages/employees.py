import flet as ft
from flet_route import Params,Basket
from utils import *
from utils.style import defaultWithWindow, defaultHeightWindow


class EmployeesPage:
    def __init__(self,page:ft.Page):
        self.page = page # основная страница приложения


    def view(self, page: ft.Page,params:Params,basket:Basket):
        page.title = "Список сотрудников"
        page.window.width = defaultWithWindow
        page.window.height= defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        return ft.View(
            "/",
            controls=[
                ft.Text("Главная страница"),
                ft.ElevatedButton("Добавить", on_click=lambda e: page.go("/add")),
                ft.ElevatedButton("Удалить", on_click=lambda e: page.go("/delete")),
                ft.ElevatedButton("Обновить", on_click=lambda e: page.go("/update"))
            ]
        )
