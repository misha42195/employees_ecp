from telegram import Bot

from config import settings
from bot.notify import create_notification

# Инициализация бота
API_TOKEN = "7733544557:AAE7gTzxBrrjNgKF1XGBJzXxZN_XzN0A2fU" # тимура
# API_TOKEN = "7293241408:AAFxMuHHYqo6u6my89vF8J7n4NplwmSM2SI" # мой
# API_TOKEN = settings.API_TOKEN

CHAT_ID = settings.CHAT_ID

bot = Bot(token=API_TOKEN)

# Список ID чатов, кому нужно отправить уведомления
chat_ids = [1617521485]  # мой


# chat_ids = [590070274]

async def send_telegram_notification():
    message = create_notification()  # Предполагается, что эта функция создаёт текст уведомления
    if not message:
        print("Нет новых уведомлений")
    print(f"Сообщение для отправки: {message}")  # Отладочная печать message)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            print(f"Сообщение отправлено в чат {chat_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
