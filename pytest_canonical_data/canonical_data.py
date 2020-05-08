import os
from typing import Any

from pytest_canonical_data.drivers import get_driver
from pytest_canonical_data.exceptions import MismatchException, MissingFileException


class CanonicalData:
    def __init__(self, file_name: str, driver: str, canonize: bool = False) -> None:
        self.file_name = file_name
        test_path, self.test_name = os.getenv('PYTEST_CURRENT_TEST').split('::', 1)
        self.test_base_dir = os.path.dirname(os.path.abspath(test_path))
        self.canonical_data_path = os.path.join(self.test_base_dir, 'canonical_data', self.test_name, self.file_name)
        self.output_data_path = os.path.join(self.test_base_dir, '_output_data', self.test_name, self.file_name)
        self.canonize = canonize
        self.driver = get_driver(driver)

    def assert_equal(self, output_data: Any) -> None:
        """
        Checks input with canonical file.

        In canonize mode overwrites canonical file instead.

        .. todo::
            Implement pytest hook to overwrite ``==`` asserts in tests.
        """
        self.driver.write(self.output_data_path, output_data)

        try:
            canonical_data = self.driver.read(self.canonical_data_path)
            self.driver.assert_equal(canonical_data, output_data)
        except (MissingFileException, MismatchException):
            if self.canonize:
                self.driver.write(self.canonical_data_path, output_data)
            else:
                raise
