import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

from config import load_config

logger = logging.getLogger(__name__)


async def start_handler(event: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(
        types.KeyboardButton(text='/check_phone'),
        types.KeyboardButton(text='/check_email'),
    )
    markup.add(types.KeyboardButton(text='/help'))

    await event.answer(f"Привет, {event.from_user.get_mention(as_html=True)} 👋!", reply_markup=markup)


async def help_handler(event: types.Message, state: FSMContext):
    await event.answer('ℹ️ справка')


async def message_handler(event: types.Message, state: FSMContext):
    await state.set_state('state')
    state_name = await state.get_state()

    asyncio.create_task(check_data(10, event))

    await event.answer(f"🔎 Начинаю поиск, {event.text}!")


async def check_phone_handler(event: types.Message, state: FSMContext):
    await event.answer('📱 Введите номер телефона')


async def check_email_handler(event: types.Message, state: FSMContext):
    await event.answer('📧 Введите адрес электронной почты')


async def check_data(delay, event: types.Message):
    await asyncio.sleep(delay)
    await event.reply(event.text)


async def main():
    logging.basicConfig(level=logging.INFO, format=u'[%(asctime)s] #%(levelname)-8s %(message)s')
    logger.info('Starting bot')

    config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)

    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    dp.register_message_handler(start_handler, commands={'start', 'restart'}, state="*")
    dp.register_message_handler(check_phone_handler, commands={'check_phone'}, state="*")
    dp.register_message_handler(check_email_handler, commands={'check_email'}, state="*")
    dp.register_message_handler(help_handler, commands={'help'}, state="*")
    dp.register_message_handler(message_handler, state="*")

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
