import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    load_dotenv()
    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=list(map(int, os.getenv("ADMINS", []))),
        )
    )
