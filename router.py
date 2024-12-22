import flet as ft
from flet_route import Routing, path

from pages.ecp_add_page import AddEcpPage
from pages.employees_add_page import AddEmployeesPage
from pages.employees_delete_page import DeleteEmployeesPage
from pages.employees import EmployeesPage
from pages.employess_update_page import UpdateEmployeesPage
from pages.dashboard import DashboardPage
from pages.kriptopro_add_page import AddKriptoproPage


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url="/", clear=False, view=EmployeesPage(page=self.page).view),
            path(url="/add_employees", clear=False, view=AddEmployeesPage(page=self.page).view),
            path(url="/add_ecp", clear=False, view=AddEcpPage(page=self.page).view),
            path(url="/add_crypto", clear=False, view=AddKriptoproPage(page=self.page).view),
            path(url="/update_employees", clear=False, view=UpdateEmployeesPage(page=self.page).view),
            path(url="/delete_employees", clear=False, view=DeleteEmployeesPage(page=self.page).view),
            path(url="/dashboard", clear=False, view=DashboardPage(page=self.page).view),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
