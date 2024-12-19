import flet as ft
from flet_route import Params,Basket

class DeleteEmployeesPage:
    def __init__(self,page:ft.Page):
        self.page = page # основная страница приложения
    def view(self, page: ft.Page,params:Params,basket:Basket):
        page.title = "Удаление сотрудников"
        return ft.View(
            "/delete",
            controls=[
                ft.Text("Добавим логику удаления сотрудников позже"),
                ft.ElevatedButton("На главную", on_click=lambda e: page.go("/"))
            ]
        )
