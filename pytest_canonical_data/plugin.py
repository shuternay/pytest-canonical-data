from typing import Callable

import pytest

from pytest_canonical_data.canonical_data import CanonicalData


def pytest_addoption(parser) -> None:
    group = parser.getgroup('canonical_data')
    group.addoption(
        '--canonize',
        action='store_true',
        help='Makes current result canonical.'
    )


class CanonicalDataFixture:
    def __init__(self, canonize: bool = False) -> None:
        self.canonize = canonize

    def __call__(self, file_name: str, driver: str = 'bytes') -> CanonicalData:
        return CanonicalData(file_name, driver=driver, canonize=self.canonize)


@pytest.fixture
def canonical_data(request) -> Callable[[str], CanonicalData]:
    canonize = request.config.option.canonize
    return CanonicalDataFixture(canonize)
