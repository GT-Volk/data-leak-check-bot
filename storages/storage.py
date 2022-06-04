from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> list:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> list:
        pass

    @abstractmethod
    def find_by_surname(self, email: str) -> list:
        pass

    @abstractmethod
    def find_by_data_id(self, data_id: int) -> list:
        pass
