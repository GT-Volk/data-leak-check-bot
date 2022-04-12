import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand

from tbot.bot_state import BotState
from tbot.config import load_config

logger = logging.getLogger(__name__)


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
    asyncio.create_task(check_data(5, event))
    await state.finish()


async def message_email_handler(event: types.Message, state: FSMContext):
    await event.answer(f"🔎 Начинаю поиск, {event.text}!")
    asyncio.create_task(check_data(5, event))
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


async def check_data(delay, event: types.Message):
    await asyncio.sleep(delay)
    markup = get_keyboard()
    await event.reply(event.text, reply_markup=markup)


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

    config = load_config()

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
