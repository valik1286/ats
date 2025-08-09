# C:\Users\Admin\Desktop\My_ATS_Project\ats\chat.py

import datetime
import os
import json
import re

# Імпортуємо core з поточного пакету 'ats'
from .core import ATSCore

# --- Конфігурація ---
AI_NAME = "AT-S"
VERSION = "1.6.1"
AUTHOR = "valik1286"
# Шляхи до файлів тепер відносні до кореня пакету 'ats'
# Важливо: використовуємо os.path.dirname(__file__) для коректного шляху
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(PACKAGE_ROOT, "data")
LOGS_FOLDER = os.path.join(PACKAGE_ROOT, "logs")

KNOWLEDGE_BASE_FILE = os.path.join(DATA_FOLDER, "ai_knowledge.txt")
LEARNED_DATA_FILE = os.path.join(DATA_FOLDER, "learned_data.json")
LOG_FILE = os.path.join(LOGS_FOLDER, "chat_log.txt")

# --- Глобальні змінні ---
chat_history = []
custom_commands = {}
learned_data = {}

# Створюємо екземпляр твоєї бібліотеки
ats_core = ATSCore()

# --- Константи для кольору ---
RED = "\033[91m"
RESET = "\033[0m"

# --- Функції для роботи з логом ---
def log_message(message, sender="User"):
    # Перевіряємо існування папки logs
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender}: {message}\n")

# --- Завантаження бази знань ---
def load_knowledge_base():
    knowledge = {}
    # Перевіряємо існування папки data
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    try:
        with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    knowledge[key.lower()] = value.strip()
    except FileNotFoundError:
        print(f"Попередження: Файл бази знань '{KNOWLEDGE_BASE_FILE}' не знайдено. Буде створено новий.")
        with open(KNOWLEDGE_BASE_FILE, "w", encoding="utf-8") as f:
            pass
    return knowledge

# --- Збереження бази знань ---
def save_knowledge_base(knowledge):
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    with open(KNOWLEDGE_BASE_FILE, "w", encoding="utf-8") as f:
        for key, value in knowledge.items():
            f.write(f"{key}: {value}\n")

# --- Завантаження вивчених даних ---
def load_learned_data():
    global learned_data
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    try:
        if os.path.exists(LEARNED_DATA_FILE):
            with open(LEARNED_DATA_FILE, "r", encoding="utf-8") as f:
                learned_data = json.load(f)
        else:
            print(f"Попередження: Файл вивчених даних '{LEARNED_DATA_FILE}' не знайдено. Буде створено новий.")
            learned_data = {}
            save_learned_data()
    except json.JSONDecodeError:
        print(f"Помилка: Файл '{LEARNED_DATA_FILE}' пошкоджений. Створюємо новий.")
        learned_data = {}
        save_learned_data()
    return learned_data

# --- Збереження вивчених даних ---
def save_learned_data():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    with open(LEARNED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(learned_data, f, ensure_ascii=False, indent=4)

# --- Функція для генерації ключа (використовує ats_core) ---
def generate_key_command(args):
    generated_key = ats_core.generate_unique_key()
    return f"Згенерований ключ: {generated_key}"

custom_commands["згенерувати ключ"] = generate_key_command

# --- Обробка відповіді ---
def get_chat_response(user_input):
    global learned_data
    user_input_lower = user_input.lower().strip()
    knowledge_base = load_knowledge_base() # Завантажуємо щоразу, щоб були актуальні дані

    if user_input_lower.startswith("навчи "):
        parts = user_input[len("навчи "):].strip().split(" це ", 1)
        if len(parts) == 2:
            phrase = parts[0].strip()
            meaning = parts[1].strip()
            learned_data[phrase.lower()] = meaning
            save_learned_data()
            return f"Запам'ятовано: '{phrase}' означає '{meaning}'."
        else:
            return "Невірний формат. Використовуйте: навчи слово це значення."

    # Перевірка на кастомні команди
    for command_name, command_func in custom_commands.items():
        if user_input_lower.startswith(command_name):
            args = user_input[len(command_name):].strip()
            return command_func(args)

    if user_input_lower == "вийти":
        return "До побачення! Був радий поспілкуватися."
    elif user_input_lower == "про мене":
        return f"{AI_NAME} - версія {VERSION} від {AUTHOR}. Я твій персональний помічник."
    elif user_input_lower == "допомога":
        help_text = (
            "Доступні команди:\n"
            "вийти - завершити розмову\n"
            "про мене - інформація про АТС\n"
            "допомога - цей список команд\n"
            "навчи слово це значення - додати нове слово\n"
            "згенерувати ключ - згенерувати унікальний ключ у форматі ATS####S#####E####D####\n"
        )
        if custom_commands:
            help_text += "Кастомні команди: " + ", ".join(custom_commands.keys())
        return help_text

    for phrase, meaning in learned_data.items():
        if phrase in user_input_lower:
            return meaning

    for key, value in knowledge_base.items():
        if key in user_input_lower:
            return value

    return "Не розумію. Скористайся командою 'допомога', якщо щось забув."

# --- Функція для запуску чату (для прямого використання, якщо потрібно) ---
def start_chat_session():
    print(f"Привіт! Я {AI_NAME}. Пиши мені або 'допомога' для списку команд.")
    load_learned_data() # Завантажуємо дані при старті сесії

    while True:
        user_input = input("Ти: ").strip()
        log_message(user_input, "User")

        if user_input.lower() == "вийти":
            response = get_chat_response(user_input)
            print(f"{AI_NAME}: {response}")
            log_message(response, AI_NAME)
            break

        response = get_chat_response(user_input)
        print(f"{AI_NAME}: {response}")
        log_message(response, AI_NAME)

        chat_history.append({"role": "user", "text": user_input})
        chat_history.append({"role": "assistant", "text": response})