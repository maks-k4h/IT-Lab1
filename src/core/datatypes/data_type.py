from abc import ABC, abstractmethod


class DataType(ABC):
    @abstractmethod
    def __str__(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def from_string(s: str) -> 'DataType':
        ...

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @property
    @abstractmethod
    def value(self):
        ...
