from enum import Enum
from typing import List, Type

from . import datatypes


class TypeNames(Enum):
    STRING = 'string'
    CHAR = 'char'
    INT = 'int'
    REAL = 'real'
    MONEY = 'money'
    MONEY_INTERVAL = 'money_interval'


class TableSchema:
    def __init__(self, type_names: List[TypeNames], id_type_name: TypeNames):
        self._type_names = type_names
        self._id_type_name = id_type_name

    @property
    def id_type_name(self) -> TypeNames:
        return self._id_type_name

    @property
    def id_type(self) -> Type[datatypes.DataType]:
        return self._type_name_to_type(self._id_type_name)

    @property
    def type_names(self) -> List[TypeNames]:
        return self._type_names

    @property
    def types(self) -> List[Type[datatypes.DataType]]:
        return [self._type_name_to_type(n) for n in self._type_names]

    @staticmethod
    def _type_name_to_type(name: TypeNames) -> Type[datatypes.DataType]:
        return {
            TypeNames.STRING: datatypes.String,
            TypeNames.CHAR: datatypes.Char,
            TypeNames.INT: datatypes.Integer,
            TypeNames.REAL: datatypes.Real,
            TypeNames.MONEY: datatypes.Money,
            TypeNames.MONEY_INTERVAL: datatypes.MoneyInterval,
        }[name]
