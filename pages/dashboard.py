import flet as ft
from flet_route import Params, Basket
from utils.style import *


class DashboardPage:

    def __init__(self, page: ft.Page):
        self.page = page  # основная страница приложения

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Панель управления"
        page.window.width = defaultWithWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.scroll = "adaptive"

        def input_form(label):
            return ft.TextField(
                label=f"{label}",
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor
            )

        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.Colors.WHITE},
                                    icon_size=14,
                                    overlay_color=hoverBgColor,
                                    shadow_color=hoverBgColor
                                    )

        # Панель сайдбар
        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=12),
                    ft.TextButton("Список сотрудников", icon=ft.Icons.WORK, style=style_menu,
                                  on_click=lambda e: self.page.go("/")),
                    ft.TextButton("Добавить нового сотрудника", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_employees")),
                    ft.TextButton("Добавить ЕЦП", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_ecp")),
                    ft.TextButton("Добавить Крипто ПРО", icon=ft.Icons.ADD, style=style_menu,
                                  on_click=lambda e: self.page.go("/add_crypto")),
                    ft.TextButton("Обновить данные сотрудника", icon=ft.Icons.UPDATE, style=style_menu,
                                  on_click=lambda e: self.page.go("/update_employees")),
                    ft.TextButton("Удалить сотрудника на хуй", icon=ft.Icons.DELETE, style=style_menu,
                                  on_click=lambda e: self.page.go("/delete_employees")),
                     ft.TextButton("Панель управления", icon=ft.Icons.DELETE, style=style_menu,
                                  on_click=lambda e: self.page.go("/dashboard")),
                ]
            )

        )

        return ft.View(
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # left side
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                controls=[
                                    sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBgColor
                        ),
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0, )
