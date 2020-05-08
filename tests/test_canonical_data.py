# -*- coding: utf-8 -*-
import os

from _pytest.pytester import Testdir


SIMPLE_TEST = """
    def test_sth(canonical_data):
        canonical_result = canonical_data('result.txt', 'text')
        canonical_result.assert_equal('123')
"""


def read_file(testdir: Testdir, base_dir: str) -> str:
    """Reads file with canonical data or output data"""
    return testdir.tmpdir.join('{}/test_sth (call)/result.txt'.format(base_dir)).read()


def write_file(testdir: Testdir, base_dir: str, data: str) -> None:
    """Writes file with canonical data or output data"""
    os.makedirs('{}/test_sth (call)'.format(base_dir), exist_ok=True)
    testdir.tmpdir.join('{}/test_sth (call)/result.txt'.format(base_dir)).new().write(data.encode())


def test_no_canonical_data(testdir: Testdir) -> None:
    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['FAILED*::test_sth*'])
    result.stdout.fnmatch_lines(['*MissingFileException*'])

    assert read_file(testdir, '_output_data') == '123'
    assert result.ret == 1


def test_mismatching_canonical_data(testdir: Testdir) -> None:
    write_file(testdir, 'canonical_data', '345')

    testdir.makepyfile(SIMPLE_TEST)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines(['FAILED*::test_sth*'])
    result.stdout.fnmatch_lines(['*MismatchException*'])

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


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'canonical_data:',
        '*--canonize*Makes current result canonical.',
    ])
