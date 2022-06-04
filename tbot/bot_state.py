from aiogram.dispatcher.filters.state import StatesGroup, State


class BotState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_surname = State()
