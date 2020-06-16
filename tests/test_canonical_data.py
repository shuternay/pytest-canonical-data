# -*- coding: utf-8 -*-
import os

from _pytest.pytester import Testdir


SIMPLE_TEST = """
    def test_sth(canonical_data):
        assert canonical_data('result.txt', 'str') == '123'
"""


CLASS_TEST = """
    class TestClass:
        def test_sth(self, canonical_data):
            assert canonical_data('result.txt', 'str') == '123'
"""


def read_file(testdir: Testdir, base_dir: str, test_name: str = 'test_sth') -> str:
    """Reads file with canonical data or output data"""
    return testdir.tmpdir.join('{}/{}/result.txt'.format(base_dir, test_name)).read()


def write_file(testdir: Testdir, base_dir: str, data: str) -> None:
    """Writes file with canonical data or output data"""
    os.makedirs('{}/test_sth'.format(base_dir), exist_ok=True)
    testdir.tmpdir.join('{}/test_sth/result.txt'.format(base_dir)).new().write(data.encode())


def test_no_canonical_data(testdir: Testdir) -> None:
    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['FAILED*::test_sth*'])
    result.stdout.fnmatch_lines(['*Canonical data with name `result.txt` does not exist*'])

    assert read_file(testdir, '_output_data') == '123'
    assert result.ret == 1


def test_mismatching_canonical_data(testdir: Testdir) -> None:
    write_file(testdir, 'canonical_data', '345')

    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['FAILED*::test_sth*'])
    result.stdout.fnmatch_lines([
        "*AssertionError: assert '345' == '123'*",
        "*- 123",
        "*+ 345",
    ])

    assert read_file(testdir, '_output_data') == '123'
    assert result.ret == 1


def test_matching_canonical_data(testdir: Testdir) -> None:
    write_file(testdir, 'canonical_data', '123')

    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['*::test_sth PASSED*'])
    assert read_file(testdir, '_output_data') == '123'
    assert result.ret == 0


def test_canonize(testdir: Testdir) -> None:
    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v', '--canonize')

    result.stdout.fnmatch_lines(['*::test_sth PASSED*'])
    assert read_file(testdir, 'canonical_data') == '123'
    assert read_file(testdir, '_output_data') == '123'
    assert result.ret == 0


def test_json_driver(testdir: Testdir) -> None:
    write_file(testdir, 'canonical_data', '{"x" : 123}')

    testdir.makepyfile("""
        def test_sth(canonical_data):
            assert canonical_data('result.txt', 'json') == {'x': 123}
    """)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['*::test_sth PASSED*'])
    assert read_file(testdir, '_output_data') == '{"x": 123}'
    assert result.ret == 0

    testdir.makepyfile("""
        def test_sth(canonical_data):
            assert canonical_data('result.txt', 'json') == {'y': 1234}
    """)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['*::test_sth FAILED*'])
    result.stdout.fnmatch_lines(["*AssertionError: assert {'x': 123} == {'y': 1234}*"])
    assert read_file(testdir, '_output_data') == '{"y": 1234}'
    assert result.ret == 1


def test_class_test_filename(testdir: Testdir) -> None:
    testdir.makepyfile(CLASS_TEST)
    result = testdir.runpytest('-v', '--canonize')

    result.stdout.fnmatch_lines(['*TestClass::test_sth PASSED*'])
    assert read_file(testdir, 'canonical_data', 'TestClass_test_sth') == '123'
    assert read_file(testdir, '_output_data', 'TestClass_test_sth') == '123'
    assert result.ret == 0


def test_help_message(testdir: Testdir) -> None:
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'canonical_data:',
        '*--canonize*Makes current result canonical.',
    ])
