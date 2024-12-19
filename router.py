import flet as ft
from flet_route import Routing, path
from pages.employees_add_page import AddEmployeesPage
from pages.employees_delete_page import DeleteEmployeesPage
from pages.employees import EmployeesPage
from pages.employess_update_page import UpdateEmployeesPage
from pages.dashboard import DashboardPage

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url="/", clear=False, view=DashboardPage(page=self.page).view),
            path(url="/add", clear=False, view=AddEmployeesPage(page=self.page).view),
            path(url="/delete", clear=False, view=DeleteEmployeesPage(page=self.page).view),
            path(url="/update", clear=False, view=UpdateEmployeesPage(page=self.page).view),
            path(url="/dashboard", clear=False, view=DashboardPage(page=self.page).view),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
