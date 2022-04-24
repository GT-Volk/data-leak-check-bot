import asyncio
import hashlib
import json
import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand

from storages.tarantool_db import TarantoolDB
from tbot.bot_state import BotState
from tbot.config import load_config

logger = logging.getLogger(__name__)

config = load_config()
db = TarantoolDB(config.tarantool_db)


async def start_handler(event: types.Message):
    markup = get_keyboard()
    await event.answer(f"Привет, {event.from_user.get_mention(as_html=True)} 👋!", reply_markup=markup)


async def help_handler(event: types.Message, state: FSMContext):
    markup = get_keyboard()
    await event.answer('ℹ️ Справка', reply_markup=markup)


async def message_handler(event: types.Message, state: FSMContext):
    markup = get_keyboard()
    await event.answer('Выберите тип поиска', reply_markup=markup)


async def message_phone_handler(event: types.Message, state: FSMContext):
    await event.answer(f"🔎 Начинаю поиск, {event.text}!")
    asyncio.create_task(check_phone(event))
    await state.finish()


async def message_email_handler(event: types.Message, state: FSMContext):
    await event.answer(f"🔎 Начинаю поиск, {event.text}!")
    asyncio.create_task(check_email(event))
    await state.finish()


async def check_phone_command_handler(event: types.Message, state: FSMContext):
    await event.answer('📱 Введите номер телефона')
    await BotState.waiting_for_phone.set()


async def check_email_command_handler(event: types.Message, state: FSMContext):
    await event.answer('📧 Введите адрес электронной почты')
    await BotState.waiting_for_email.set()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/check_phone', description='📱 Проверить номер телефона'),
        BotCommand(command='/check_email', description='📧 Проверить адрес email'),
        BotCommand(command='/help', description='ℹ️ Справка'),
    ]
    await bot.set_my_commands(commands)


async def check_phone(event: types.Message):
    md5 = hashlib.md5(str(event.text).encode('utf-8')).hexdigest()
    start_time = time.time()
    phone_data = db.find_by_phone(md5)
    data_str = 'К сожалению ничего не найдено'
    if phone_data:
        data = db.find_by_data_id(phone_data[0][1])
        if data:
            data_dict = json.JSONDecoder().decode(data[0][1])
            data_str = '\n'.join(key + ': ' + value for key, value in data_dict.items())
    logger.info("--- %s ms ---" % ((time.time() - start_time) * 1000))

    markup = get_keyboard()
    await event.reply(data_str, reply_markup=markup)


async def check_email(event: types.Message):
    md5 = hashlib.md5(str(event.text).encode('utf-8')).hexdigest()
    start_time = time.time()
    email_data = db.find_by_email(md5)
    data_str = 'К сожалению ничего не найдено'
    if email_data:
        data = db.find_by_data_id(email_data[0][1])
        if data:
            data_dict = json.JSONDecoder().decode(data[0][1])
            data_str = '\n'.join(key + ': ' + value for key, value in data_dict.items())
    logger.info("--- %s ms ---" % ((time.time() - start_time) * 1000))

    markup = get_keyboard()
    await event.reply(data_str, reply_markup=markup)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands={'start', 'restart'}, state="*")
    dp.register_message_handler(help_handler, commands={'help'}, state="*")
    dp.register_message_handler(check_phone_command_handler, commands={'check_phone'}, state="*")
    dp.register_message_handler(check_email_command_handler, commands={'check_email'}, state="*")
    dp.register_message_handler(message_phone_handler, state=BotState.waiting_for_phone)
    dp.register_message_handler(message_email_handler, state=BotState.waiting_for_email)
    dp.register_message_handler(message_handler, state="*")


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(
        types.KeyboardButton(text='/check_phone'),
        types.KeyboardButton(text='/check_email'),
    )
    markup.add(types.KeyboardButton(text='/help'))
    return markup


async def main():
    logging.basicConfig(level=logging.INFO, format=u'[%(asctime)s] #%(levelname)-8s %(message)s')
    logger.info('Starting bot')

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    register_handlers_common(dp)

    await set_commands(bot)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
