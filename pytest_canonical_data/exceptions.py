from typing import Any


class CanonicalDataException(AssertionError):
    """Base exception for pytest-canonical-data"""


class MismatchException(CanonicalDataException):
    """Data mismatch exception"""

    def __init__(self, message: str, canonical_data: Any, output_data: Any, *args) -> None:
        self.canonical_data = canonical_data
        self.output_data = output_data

        super().__init__(message, *args)


class MissingFileException(CanonicalDataException):
    """Missing canonical data exception"""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)
