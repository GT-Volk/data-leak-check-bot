from storages.fake_db import FakeDB
from storages.storage import Storage
from storages.tarantool_db import TarantoolDB
from tbot.config import Config


class StorageFactory:
    def __new__(cls, config: Config) -> Storage:
        if config.storage == 'fake':
            return FakeDB()

        if config.storage == 'tarantool':
            return TarantoolDB(config.tarantool_db)
