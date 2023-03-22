import json
from fuzzywuzzy import fuzz

# Импорт библиотеки aiogram
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Импортирование библиотеки sys для завершения кода.
import sys 

# установка уровня логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token='6091667438:AAF16BIpbGKVtq5maxwX_Ruj5GDSzptsHLE')
dp = Dispatcher(bot)

dispute = 0
ban_percent = 75

with open('symbols.json', 'r') as file:
    symbols = json.load(file) 

with open('bad_words.json', 'r') as file:
    bad_words = json.load(file) 

with open('admins.json', 'r') as file:
    admins = json.load(file) 

with open('mute.json', 'r') as file:
    mute = json.load(file) 


def replace_chars(input_string, char_dict):
    output_string = ""
    for char in input_string:
        if char in char_dict:
            output_string += char_dict[char]
        else:
            output_string += char
    return output_string

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # This handler will be called when user sends /start command
    await message.reply("Elifo Moderator Bot - Официальный бот модератор от Elifo Games для их чата.")

@dp.message_handler(commands=['stop'])
async def start(message: types.Message):
    message.delete()
    if message.from_user.id == 136817688:
        sys.exit()


@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    for admin in admins:
        if (admin == message.from_user.id):
            if message.reply_to_message is not None:
                message.reply_to_message.delete()
                await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)

@dp.message_handler(commands=['mute'])
async def muteDef(message: types.Message):
    for admin in admins:
        if (admin == message.from_user.id):
            if message.reply_to_message is not None:
                mute[message.reply_to_message.from_user.id] = str(message.date)
                with open('mute.json', 'w') as f:
                    json.dump(mute, f)

# обработчик всех сообщений
@dp.message_handler()
async def message(message: types.Message):
    if str(message.from_user.id) not in admins:
        if str(message.from_user.id) not in mute:
            message_text = replace_chars(message.text.lower(), symbols).split()
            for mess in message_text:
                for word in bad_words:
                    if (fuzz.ratio(mess, word) > ban_percent):
                        await message.delete()
                        #await bot.send_message(message.from_user.id, "Извините, но бот посчитал это сообщение неприемлимым. Ниже предоставленно сообщение на которое ругается бот.")
                        #await bot.send_message(message.from_user.id, message.text)
                        for admin in admins:
                            await bot.send_message(admin, message)
                        return
        else:
            """
            mute_date = mute[message.from_user.id].split().split("-").split(":")
            date = str(message.date).split().split("-").split(":")
            if mute_date[3] - date[3] > 2 or mute_date[2] < date[2] or mute_date[1] < date[1] or mute_date[0] < date[0]:
                mute.pop(message.from_user.id)
                with open('mute.json', 'w') as f:
                    json.dump(mute, f)
                message_text = replace_chars(message.text.lower(), symbols).split()
                for mess in message_text:
                    for word in bad_words:
                        if (fuzz.ratio(mess, word) > 70):
                            message.delete()
                            await bot.send_message(message.from_user.id, message.text)
                            for admin in admins:
                                await bot.send_message(admin, message)
                            await bot.send_message(message.from_user.id, "Извините, но бот посчитал это сообщение неприемлимым. Ниже предоставленно сообщение на которое ругается бот.")

                            
            else:
                message.delete()
                await bot.send_message(message.from_user.id, f"Извините, но у вас временный мут. Время до конца мута: {2 - mute_date[3] - date[3]}")
            """
            #await bot.send_message(message.from_user.id, "Извините, но у вас мут.")
            await message.delete()

@dp.message_handler(commands=['mute'])
async def muteDef(message: types.Message):
    for admin in admins:
        if (admin == message.from_user.id):
            if message.reply_to_message is not None:
                mute[message.reply_to_message.from_user.id] = str(message.date)
                with open('mute.json', 'w') as f:
                    json.dump(mute, f)

# обработчик всех сообщений
@dp.edited_message_handler()
async def edited_message(message: types.Message):
    if str(message.from_user.id) not in admins:
        if str(message.from_user.id) not in mute:
            message_text = replace_chars(message.text.lower(), symbols).split()
            for mess in message_text:
                for word in bad_words:
                    if (fuzz.ratio(mess, word) > ban_percent):
                        await message.delete()
                        #await bot.send_message(message.from_user.id, "Извините, но бот посчитал это сообщение неприемлимым. Ниже предоставленно сообщение на которое ругается бот.")
                        #await bot.send_message(message.from_user.id, message.text)
                        for admin in admins:
                            await bot.send_message(admin, message)
                        return
        else:
            """
            mute_date = mute[message.from_user.id].split().split("-").split(":")
            date = str(message.date).split().split("-").split(":")
            if mute_date[3] - date[3] > 2 or mute_date[2] < date[2] or mute_date[1] < date[1] or mute_date[0] < date[0]:
                mute.pop(message.from_user.id)
                with open('mute.json', 'w') as f:
                    json.dump(mute, f)
                message_text = replace_chars(message.text.lower(), symbols).split()
                for mess in message_text:
                    for word in bad_words:
                        if (fuzz.ratio(mess, word) > 70):
                            message.delete()
                            await bot.send_message(message.from_user.id, message.text)
                            for admin in admins:
                                await bot.send_message(admin, message)
                            await bot.send_message(message.from_user.id, "Извините, но бот посчитал это сообщение неприемлимым. Ниже предоставленно сообщение на которое ругается бот.")

                            
            else:
                message.delete()
                await bot.send_message(message.from_user.id, f"Извините, но у вас временный мут. Время до конца мута: {2 - mute_date[3] - date[3]}")
            """
            #await bot.send_message(message.from_user.id, "Извините, но у вас мут.")
            await message.delete()
# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
