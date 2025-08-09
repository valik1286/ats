# C:\Users\Admin\Desktop\My_ATS_Project\run_ats_app.py

import json
import sys

try:
    import my_ats
    from my_ats import process_api_request, create_key # Імпортуємо create_key
    from my_ats import AI_NAME 
except ImportError:
    print("Помилка: Пакет 'my-ats-system' не знайдено.")
    print("Будь ласка, переконайтеся, що ви встановили ваш пакет АТС:")
    print("1. Перейдіть до папки 'C:\\Users\\Admin\\Desktop\\My_ATS_Project'")
    print("2. Виконайте команду 'pip install .'")
    sys.exit(1)

# Твій ключ АТС
# Заміни "PLACEHOLDER_KEY" на ключ, який ти згенеруєш.
# Якщо це "PLACEHOLDER_KEY", скрипт спершу згенерує ключ.
ats_key = "PLACEHOLDER_KEY" # <--- ЗАМІНИ ЦЕЙ ТЕКСТ НА СВІЙ ЗГЕНЕРОВАНИЙ КЛЮЧ!

if ats_key == "PLACEHOLDER_KEY":
    print("--- ПЕРШИЙ ЗАПУСК: ГЕНЕРАЦІЯ КЛЮЧА ---")
    print("Схоже, це ваш перший запуск або ключ ще не вставлено.")
    print("Зараз буде згенеровано новий АТС ключ.")
    
    generated_new_key = create_key() # Генеруємо ключ з пакета!
    
    print("\n-------------------------------------------------------------")
    print(f"ВАШ НОВИЙ АТС КЛЮЧ: {generated_new_key}")
    print("-------------------------------------------------------------")
    print("\nБудь ласка, скопіюйте цей ключ!")
    print(f"Потім відкрийте файл '{__file__}' (тобто цей файл),")
    print("знайдіть рядок `ats_key = \"PLACEHOLDER_KEY\"` і")
    print("ЗАМІНІТЬ `\"PLACEHOLDER_KEY\"` на ваш щойно згенерований ключ.")
    print("Збережіть файл і запустіть його знову.")
    sys.exit(0) # Виходимо, щоб користувач вставив ключ

print(f"--- Запуск додатка, що використовує {AI_NAME} ---")
print(f"Підключаємося до АТС з робочим ключем: {ats_key}\n")

# Приклад використання API для отримання інформації
print("Виклик: my_ats.process_api_request(ats_key, 'get_info')")
info_response = process_api_request(ats_key, "get_info")
print(f"Відповідь від АТС: {json.dumps(info_response, ensure_ascii=False, indent=2)}\n")

# Приклад використання API для чату
user_message = "Привіт, АТС! Як справи?"
print(f"Виклик: my_ats.process_api_request(ats_key, 'chat', '{user_message}')")
chat_response = process_api_request(ats_key, "chat", user_message)
print(f"Відповідь від АТС: {json.dumps(chat_response, ensure_ascii=False, indent=2)}\n")

user_message_2 = "Що ти можеш навчити?"
print(f"Виклик: my_ats.process_api_request(ats_key, 'chat', '{user_message_2}')")
chat_response_2 = process_api_request(ats_key, "chat", user_message_2)
print(f"Відповідь від АТС: {json.dumps(chat_response_2, ensure_ascii=False, indent=2)}\n")

# Приклад використання API для генерації нового ключа (через API з існуючим ключем)
print("Виклик: my_ats.process_api_request(ats_key, 'generate_key')")
new_key_response_via_api = process_api_request(ats_key, "generate_key")
print(f"Відповідь від АТС: {json.dumps(new_key_response_via_api, ensure_ascii=False, indent=2)}\n")

# Якщо потрібно, можна запустити інтерактивний чат
# print("\n--- Запуск інтерактивного чату АТС ---")
# my_ats.start_chat_session()