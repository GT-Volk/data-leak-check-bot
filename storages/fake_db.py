from storages.storage import Storage


class FakeDB(Storage):

    def close(self) -> None:
        pass

    def find_by_phone(self, phone: str) -> list:
        if phone == '9f3ffa0ab64f8273bc4b683af707c26c':  # 79111111111
            return ['asd', 1]
        return []

    def find_by_email(self, email: str) -> list:
        if email == '97c2fc39b67e0e5e5c0a33ddf53e0227':  # fake@fake.net
            return ['asd', 1]
        return []

    def find_by_data_id(self, data_id: int) -> list:
        if data_id == 1:
            return [1, '{"data": "fake"}']
        return []
