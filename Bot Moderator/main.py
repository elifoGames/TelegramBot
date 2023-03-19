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

# принудительное завершение программы
def stop():
    sys.exit()

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # This handler will be called when user sends /start command
    await message.reply("Привет! Я бот, который готов помочь тебе. Чем я могу быть полезен?")

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
