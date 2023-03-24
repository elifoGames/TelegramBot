import json
from fuzzywuzzy import fuzz
from list import *

# Импорт библиотеки aiogram
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.utils import exceptions

# Импортирование библиотеки sys для завершения кода.
import sys 

import tracemalloc
tracemalloc.start()

# установка уровня логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


def read_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file) 
    
def write_json(file_name, value):
    with open(file_name, 'w') as f:
        json.dump(value, f)

def replace_chars(input_string, char_dict):
    output_string = ""
    for char in input_string:
        if char in char_dict:
            output_string += char_dict[char]
        else:
            output_string += char
    return output_string

symbols = read_json(symbols_file)
bad_words = read_json(bad_words_file)
admins = read_json(admins_file)
mute = read_json(mute_file)
mute_list = read_json(mute_list_file)
trigers = read_json(trigers_file)

def send_error(error):
    print("Ошибка отправки сообщения пользователю.")
    for admin in admins:
        bot.send_message(admin, "Ошибка отправки сообщения пользователю.")