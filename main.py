import asyncio
import os.path
import sys
import threading

import shutil


import flet as ft
from router import Router
from pathlib import Path
from bot.telegram_message import send_telegram_notification

sys.path.append(str(Path(__file__).parent.parent))


def main(page: ft.Page):
    page.title = "Основная страница"

    # check_trade = threading.Thread(target=run_async, daemon=True)
    # check_trade.start()

    # check_trade = threading.Thread(target=run_async,daemon=True)
    # check_trade.start()
    # asyncio.create_task(send_telegram_notification())
    page.run_task(handler=send_telegram_notification)
    Router(page)


# if getattr(sys,'frozen',False):
#     base_path = sys._MEIPAS
# else:
#     base_path = os.path.dirname(os.path.abspath(__file__))

# db_source = os.path.join(base_path, "database_sqlite3.db")
# db_dest = os.path.join(os.getcwd(), "database_sqlite3.db")

# if not os.path.exists(db_dest):
#     print(f"Копирование базы данных из {db_source} в {db_dest}")
#     shutil.copyfile(db_source, db_dest)
# else:
#     print("База данных уже существует")

# db_path  = db_dest


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assert", upload_dir="assert/uploads")
