import tarantool

from storages.storage import Storage
from tbot.config import TarantoolDBConfig


class TarantoolDB(Storage):

    def __init__(self, config: TarantoolDBConfig):
        self.conn = tarantool.connect(config.host, config.port, config.user, config.password)
        self.space_phones = self.conn.space('PHONES')
        self.space_emails = self.conn.space('EMAILS')
        self.space_surnames = self.conn.space('SURNAMES')
        self.space_datas = self.conn.space('DATAS')

    def close(self) -> None:
        self.conn.close()

    def find_by_phone(self, phone: str) -> list:
        data = self.space_phones.select(phone).data
        if data:
            return data[0]

        return []

    def find_by_email(self, email: str) -> list:
        data = self.space_emails.select(email).data
        if data:
            return data[0]

        return []

    def find_by_surname(self, email: str) -> list:
        data = self.space_surnames.select(email).data
        if data:
            return data[0]

        return []

    def find_by_data_id(self, data_id: int) -> list:
        data = self.space_datas.select(data_id).data
        if data:
            return data[0]

        return []
