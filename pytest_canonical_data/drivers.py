import os
from typing import Any
from abc import abstractmethod


from pytest_canonical_data.exceptions import MismatchException, MissingFileException


class Driver:
    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @abstractmethod
    def read(self, path: str) -> Any:
        if not os.path.exists(path):
            raise MissingFileException('file {} does not exist'.format(path))
        with open(path, 'rb') as fp:
            return fp.read()

    @abstractmethod
    def write(self, path: str, data: Any) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fp:
            fp.write(data)

    def assert_equal(self, canonical_data: Any, output_data: Any) -> None:
        if not canonical_data == output_data:
            raise MismatchException("data doesn't match", canonical_data, output_data)


class BytesDriver(Driver):
    def read(self, path: str) -> bytes:
        return super().read(path)

    def write(self, path: str, data: bytes) -> None:
        super().write(path, data)


class TextDriver(Driver):
    def read(self, path: str) -> str:
        return super().read(path).decode()

    def write(self, path: str, data: str) -> None:
        super().write(path, data.encode())


DRIVERS = {
    'bytes': BytesDriver,
    'str': TextDriver,
    'text': TextDriver,
}


def get_driver(name: str) -> Driver:
    return DRIVERS[name]()
