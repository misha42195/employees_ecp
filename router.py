
# database_sqlite3
import flet as ft
from flet_route import Routing, path

from pages.add_ecp_find_empl import AddEcpFindEmpl
from pages.add_kriptopro_find_empl import AddKriptoproFindEmpl
from pages.dashboard_current_licens import DashboardCurrentLicensPage
from pages.dashboard_easisted_licens import DashboardEasistedPage
from pages.employees_add_page import AddEmployeesPage
from pages.employees_all import EmplAllPage
from pages.employees_info_page import  EmployeesInfoPage
from pages.employees import EmployeesPage
from pages.employess_update_page import UpdateEmployeesPage
from pages.dashboard import DashboardPage


class Router:
    def __init__(self, page: ft.Page):
        self.page = page

        self.app_routes = [
            path(url="/", clear=False, view=DashboardPage(page=self.page).view),
            path(url="/employees", clear=False, view=EmployeesPage(page=self.page).view),
            path(url="/add_employees", clear=False, view=AddEmployeesPage(page=self.page).view),
            # path(url="/add_ecp", clear=False, view=AddEcpPage(page=self.page).view),
            # path(url="/add_crypto", clear=False, view=AddKriptoproPage(page=self.page).view),
            path(url="/update_employees", clear=False, view=UpdateEmployeesPage(page=self.page).view),
            path(url="/employees_info", clear=False, view=EmployeesInfoPage(page=self.page).view),
            path(url="/add_kriptopro_find_empl", clear=False, view=AddKriptoproFindEmpl(page=self.page).view),
            path(url="/add_ecp_find_empl", clear=False, view=AddEcpFindEmpl(page=self.page).view),
            path(url="/dashboard_current_licens", clear=False, view=DashboardCurrentLicensPage(page=self.page).view),
            path(url="/dashboard_easisted_licenses",clear=False,view=DashboardEasistedPage(page=self.page).view),
            path(url="/all_employees", clear=False, view=EmplAllPage(page=self.page).view),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
