from telegram import Bot


from config import settings
from crud.notify import create_notification

# Инициализация бота
API_TOKEN = settings.API_TOKEN
CHAT_ID = settings.CHAT_ID

bot = Bot(token=API_TOKEN)

# chat_ids = [123456789, 987654321, 1122334455]
async def send_telegram_notification():
    message = create_notification()
    # for chat_id in chat_ids:
    # await send_telegram_notification(chat_id, message)
    await bot.send_message(chat_id=CHAT_ID, text=message)
