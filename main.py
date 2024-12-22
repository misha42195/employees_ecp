import sys

import flet as ft
from router import Router
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def main(page: ft.Page):
    page.title = "Основная страница"


    Router(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
