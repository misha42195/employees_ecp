import flet as ft
from flet_route import Params,Basket

class UpdateEmployeesPage:
    def __init__(self,page:ft.Page):
        self.page = page # основная страница приложения
    def view(self, page: ft.Page,params:Params,basket:Basket):
        page.title = "Обновление сотрудников"
        return ft.View(
            "/update",
            controls=[
                ft.Text("Добавим логику обновления сотрудников позже"),
                ft.ElevatedButton("На главную", on_click=lambda e: page.go("/"))
            ]
        )
