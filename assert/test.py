import sqlite3

# Определение функции ru_lower
def ru_lower(s):
    if s is None:
        return None
    return s.lower()

# Подключение к базе данных SQLite
conn = sqlite3.connect("database_sqlite3")

# Регистрация функции ru_lower
conn.create_function("ru_lower", 1, ru_lower)
