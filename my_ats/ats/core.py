# C:\Users\Admin\Desktop\My_ATS_Project\ats\core.py

import uuid
import datetime
import random
import string

class ATSCore:
    def __init__(self):
        self.system_status = "Online"
        self.last_update = datetime.datetime.now()

    def get_system_status(self):
        return f"Статус системи: {self.system_status}. Останнє оновлення: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}"

    def process_data(self, data):
        # Приклад обробки даних
        processed_data = f"Дані '{data}' оброблено ядром АТС."
        return processed_data

    def generate_unique_key(self):
        # Генерація унікального ключа в заданому форматі
        part1 = ''.join(random.choices(string.digits + string.ascii_letters, k=4))
        part2 = ''.join(random.choices(string.digits + string.ascii_letters, k=5))
        part3 = ''.join(random.choices(string.digits + string.ascii_letters, k=4))
        part4 = ''.join(random.choices(string.digits + string.ascii_letters, k=4))
        return f"ATS{part1}S{part2}E{part3}D{part4}"