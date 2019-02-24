from pytest_check import check

# properly formatted tests in
# multiline strings contain blank lines with spaces, freaks out flake8

# flake8: noqa

def test_context_manager():
    with check:
        x = 3
        assert 1 < x < 4


def test_context_manager_fail(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_failures():
            with check: assert 1 == 0
            with check: assert 1 > 2
            with check: assert 1 < 5 < 4
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines([
        "*FAILURE: assert 1 == 0*",
        "*FAILURE: assert 1 > 2*",
        "*FAILURE: assert 5 < 4*",
        "* assert 1 < 5 < 4*",
        "*Failed Checks: 3*",
    ])


def test_stop_on_fail(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_failures():
            with check: assert 1 == 0
            with check: assert 1 > 2
            with check: assert 1 < 5 < 4
    """
    )

    result = testdir.runpytest('-x')
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines([
        "*assert 1 == 0*",
    ])
