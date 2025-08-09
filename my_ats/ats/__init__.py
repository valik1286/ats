# C:\Users\Admin\Desktop\My_ATS_Project\my_ats\__init__.py

# Імпортуємо основні класи та функції, які ти хочеш відкрити для зовнішнього використання
from .core import ATSCore
from .chat import get_chat_response, start_chat_session, AI_NAME, VERSION, AUTHOR

# Це робить функцію get_chat_response доступною як my_ats.get_response()
get_response = get_chat_response

# Створюємо глобальний екземпляр ATSCore для використання в API та генерації ключа
_ats_core_instance = ATSCore()

# Функція для генерації нового ключа АТС
def create_key(): # Змінено назву на create_key, як ти просив
    """Генерує та повертає новий унікальний ключ АТС."""
    return _ats_core_instance.generate_unique_key()

# Твоя функція API
def process_api_request(key, command=None, data=None):
    """
    Основна функція для обробки запитів до АТС через API з використанням ключа.
    """
    # Твій "майстер-ключ" для входу
    if key == "ваш_ключ": 
        
        if command == "get_info":
            return {"status": "success", "message": _ats_core_instance.get_system_status()}
        elif command == "chat":
            if data:
                return {"status": "success", "response": get_response(data)}
            else:
                return {"status": "error", "message": "Відсутній текст для чату."}
        elif command == "generate_key": # Це команда для генерації ключа ПІСЛЯ входу за "ваш_ключ"
            return {"status": "success", "key": _ats_core_instance.generate_unique_key()}
        else:
            return {"status": "error", "message": "Невідома команда API."}
    else:
        return {"status": "error", "message": "Невірний або відсутній ключ АТС."}

# Приклад, якщо хтось запустить 'python -m my_ats' напряму
if __name__ == "__main__":
    import json
    print(f"Пакет {AI_NAME} (версія {VERSION}) від {AUTHOR} успішно встановлено.")
    print("Ви можете імпортувати його як 'import my_ats'.")
    print("\nПриклад використання API:")
    print("from my_ats import process_api_request, create_key") # Оновлено імпорт на create_key
    
    # Демонстрація генерації ключа
    new_generated_key = create_key() # Викликаємо нову функцію!
    print(f"\nЗгенеровано новий ключ (без перевірки): {new_generated_key}")

    # Використання згенерованого ключа (для демонстрації)
    # Зверни увагу: для реального використання ти б ЗБЕРІГАВ цей ключ
    print(f'\nВикористання нового ключа: process_api_request("ваш_ключ", "get_info")')
    result_with_master_key = process_api_request("ваш_ключ", "get_info") # Все ще потрібен майстер-ключ для доступу до API
    print(json.dumps(result_with_master_key, ensure_ascii=False, indent=2))