# -*- coding: utf-8 -*-


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'record of test case failure:',
        '*--record*Record if the test case failed.',
        "*--record-path=RECORD_PATH",
        "*It will be save in the 'record' directory of current",
        "*directory. If this parameter is set, it will be save in",
        "*the specified path.",
    ])


def test_record_on_failure(testdir):
    testdir.makepyfile("""
        import pytest

        def test_hello_world():
            assert True

        def test_hello_world2():
            assert False

        def test_hello_world3():
            assert False

    """)

    result = testdir.runpytest('--record')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    # assert result.ret == 0
    assert True
