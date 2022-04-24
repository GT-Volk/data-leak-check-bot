import tarantool

from tbot.config import TarantoolDBConfig


class TarantoolDB:

    def __init__(self, config: TarantoolDBConfig):
        self.conn = tarantool.connect(config.host, config.port, config.user, config.password)
        self.space_phones = self.conn.space('PHONES')
        self.space_emails = self.conn.space('EMAILS')
        self.space_datas = self.conn.space('DATAS')

    def close(self):
        self.conn.close()

    def find_by_phone(self, phone: str):
        return self.space_phones.select(phone)

    def find_by_email(self, email: str):
        return self.space_emails.select(email)

    def find_by_data_id(self, data_id: int):
        return self.space_datas.select(data_id)
