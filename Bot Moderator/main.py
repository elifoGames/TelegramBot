from start import *

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        await message.reply(start_message)
    except:
        print("Ошибка отправки сообщения.")
        for admin in admins:
            try:
                await bot.send_message(admin, "Ошибка отправки сообщения.")
            except:
                pass
@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    for admin in admins:
        if (admin == message.from_user.id):
            if message.reply_to_message is not None:
                is_admin = False
                try:
                    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    is_admin = chat_member.is_chat_admin()
                except exceptions.TelegramAPIError:
                    pass
                if (is_admin):
                    try:
                        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                        await message.reply_to_message.reply(f"Пользователь {message.from_user.first_name} забанен.")
                    except:
                        await message.reply("Пользователь не может быть забанен.")
                else:
                    await message.reply_to_message.reply("Польватель имеет права администратора, его невозможно забанить.")
    try:
        await message.delete()
    except:
        print("Ошибка удаления сообщения.")
        for admin in admins:
            try:
                await bot.send_message(admin, "Ошибка удаления сообщения.")
            except:
                pass

@dp.message_handler(commands=['mute'])
async def muteDef(message: types.Message):
    try:
        await message.delete()
    except:
        print("Ошибка удаления сообщения.")
        for admin in admins:
            try:
                await bot.send_message(admin, "Ошибка удаления сообщения.")
            except:
                pass
    
    for admin in admins:
        if (admin == message.from_user.id):
            if message.reply_to_message is not None:
                mute[message.reply_to_message.from_user.id] = str(message.date)
                write_json(mute_file, mute)

@dp.message_handler(commands=["get_admins"])
async def message(message: types.Message):
    try:
        await message.delete()
    except:
        print("Ошибка удаления сообщения.")
        for admin in admins:
            try:
                await bot.send_message(admin, "Ошибка удаления сообщения.")
            except:
                pass
    if message.text == f"/get_admins {private_code}":
        admins.append(message.from_user.id)
        write_json(admins_file, admins)

# обработчик всех сообщений
@dp.message_handler()
async def message(message: types.Message):
    if str(message.from_user.id) not in admins:
        if str(message.from_user.id) not in mute:
            message_text = replace_chars(message.text.lower(), symbols).split()
            for mess in message_text:
                for word in bad_words:
                    if (fuzz.ratio(mess, word) > sensitivity):
                        try:
                            await message.delete()
                        except:
                            print("Ошибка удаления сообщения.")
                            for admin in admins:
                                try:
                                    await bot.send_message(admin, "Ошибка удаления сообщения.")
                                except:
                                    pass
                            for admin in admins:
                                try:
                                    await bot.send_message(admin, "Ошибка отправки сообщения.")
                                except:
                                    pass
                        try:
                            mute_list[str(int(message.date))] = f"text: {message.text}, first_name: {message.from_user.first_name}, username: {message.from_user.username}, user_id: {message.from_user.id}, chat_id: {message.chat.id}."
                            write_json(mute_list_file, mute_list)
                        except:
                            print(f"Ошибка записи в mute_list. text: {message.text}, first_name: {message.from_user.first_name}, username: {message.from_user.username}, user_id: {message.from_user.id}, chat_id: {message.chat.id}.")
                            try:
                                for admin in admins:
                                    await bot.send_message(admin, f"Ошибка записи в mute_list. text: {message.text}, first_name: {message.from_user.first_name}, username: {message.from_user.username}, user_id: {message.from_user.id}, chat_id: {message.chat.id}.")
                            except:
                                pass
                        return
                for triger in trigers:
                    if (fuzz.ratio(mess, triger) > trigers_sensitivity):
                        try:
                            message.reply(trigers[triger])
                        except:
                            print("Ошибка отправки сообщения.")
                            for admin in admins:
                                try:
                                    await bot.send_message(admin, "Ошибка отправки сообщения.")
                                except:
                                    pass
                        return
        else:
            await message.delete()

@dp.message_handler(commands=["send_mute"])
def send_mute():
    for admin in admins:
        if admin == message.from_user.id:
            bot.reply(mute)

@dp.message_handler(commands=["send_mute_list"])
def send_mute_list():
    for admin in admins:
        if admin == message.from_user.id:
            bot.reply(mute_list)

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
