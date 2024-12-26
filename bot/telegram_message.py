from telegram import Bot


from config import settings
from crud.notify import create_notification

# Инициализация бота
API_TOKEN = settings.API_TOKEN
CHAT_ID = settings.CHAT_ID

bot = Bot(token=API_TOKEN)


async def send_telegram_notification():
    message = create_notification()
    await bot.send_message(chat_id=CHAT_ID, text=message)
