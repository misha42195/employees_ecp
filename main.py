import asyncio
import sys
import threading
import flet as ft
from router import Router
from pathlib import Path
from bot.telegram_message import send_telegram_notification
sys.path.append(str(Path(__file__).parent.parent))

def run_async():
    # Используем asyncio для вызова асинхронной функции
    asyncio.run(send_telegram_notification())

def main(page: ft.Page):
    page.title = "Основная страница"

    # check_trade = threading.Thread(target=run_async, daemon=True)
    # check_trade.start()

    Router(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assert")
