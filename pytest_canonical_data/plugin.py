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


@pytest.fixture
def canonical_data(request) -> Callable[[str], CanonicalData]:
    canonize = request.config.option.canonize

    def canonical_data_factory(file_name: str, driver: str = 'bytes') -> CanonicalData:
        return CanonicalData(file_name, driver=driver, canonize=canonize)
    return canonical_data_factory
