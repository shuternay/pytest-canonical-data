from typing import Callable, Any, List, Optional

import pytest
from _pytest.assertion import pytest_assertrepr_compare as original_compare

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


def pytest_assertrepr_compare(config, op: str, left: Any, right: Any) -> Optional[List[str]]:
    """
    Hook which provides error message for failed asserts.
    We extract canonical data from the file and pass it next to the pytest's implementation.

    Note that current implementation may conflict with other plugins which define that hook.
    """
    if isinstance(left, CanonicalData):
        left_data = left.get_data()
        if left_data == CanonicalData.Empty:
            return [
                'Canonical data with name `{}` does not exist. '
                'Run `pytest --canonize` to create it from current values'.format(left.file_name)
            ]
        left = left_data
    elif isinstance(right, CanonicalData):
        right_data = right.get_data()
        if right_data == CanonicalData.Empty:
            return [
                'Canonical data with name `{}` does not exist. '
                'Run `pytest --canonize` to create it from the test value'.format(right.file_name)
            ]
        right = right_data
    else:
        return
    explanation = original_compare(config, op, left, right)
    if explanation:
        return explanation + ['Note: run `pytest --canonize` to overwrite canonical data with current values']
