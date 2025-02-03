from telegram import Bot


from config import settings
from crud.notify import create_notification

# Инициализация бота
API_TOKEN = settings.API_TOKEN
CHAT_ID = settings.CHAT_ID

bot = Bot(token=API_TOKEN)


# Список ID чатов, кому нужно отправить уведомления
chat_ids = [1617521485]  # Добавьте сюда другие chat_id, если нужно


async def send_telegram_notification():
    message = create_notification()  # Предполагается, что эта функция создаёт текст уведомления
    print(message)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            print(f"Сообщение отправлено в чат {chat_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
