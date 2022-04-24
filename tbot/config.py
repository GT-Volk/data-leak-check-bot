import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class TgBotConfig:
    token: str
    admin_ids: list[int]


@dataclass
class TarantoolDBConfig:
    host: str
    port: int
    user: str
    password: str


@dataclass
class Config:
    tg_bot: TgBotConfig
    tarantool_db: TarantoolDBConfig


def load_config():
    load_dotenv()
    return Config(
        tg_bot=TgBotConfig(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=list(map(int, os.getenv("ADMINS", []))),
        ),
        tarantool_db=TarantoolDBConfig(
            host=os.getenv("TARANTOOL_DB_HOST", "localhost"),
            port=os.getenv("TARANTOOL_DB_PORT", 3301),
            user=os.getenv("TARANTOOL_DB_USER"),
            password=os.getenv("TARANTOOL_DB_PASSWORD"),
        ),
    )
