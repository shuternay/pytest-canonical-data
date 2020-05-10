import os
from typing import Any

from pytest_canonical_data.drivers import get_driver


class CanonicalData:
    def __init__(self, file_name: str, driver: str, canonize: bool = False) -> None:
        self.file_name = file_name
        # TODO: better test name extraction
        test_path, self.test_name = os.getenv('PYTEST_CURRENT_TEST').split('::', 1)
        self.test_name = self.test_name.replace(' (call)', '')

        self.test_base_dir = os.path.dirname(os.path.abspath(test_path))
        self.canonical_data_path = os.path.join(self.test_base_dir, 'canonical_data', self.test_name, self.file_name)
        self.output_data_path = os.path.join(self.test_base_dir, '_output_data', self.test_name, self.file_name)
        self.canonize = canonize
        self.driver = get_driver(driver)

    class Empty:
        """
        ``None`` is a valid value for the data stored in a file,
        so we return ``CanonicalData.Empty`` if a file does not exist.
        """
        pass

    def get_data(self) -> Any:
        """Returns data stored in canonical data file"""
        if self.driver.exists(self.canonical_data_path):
            return self.driver.read(self.canonical_data_path)
        return self.Empty

    def __eq__(self, output_data: Any) -> bool:
        """
        Compares ``output_data`` with data in canonical file.

        In canonize mode overwrites canonical file with actual data.
        """
        self.driver.write(self.output_data_path, output_data)

        canonical_data = self.get_data()
        if output_data == canonical_data:
            # canonical data exists and is equal to output_data
            return True
        if self.canonize:
            self.driver.write(self.canonical_data_path, output_data)
            return True
        return False


