# -*- coding: utf-8 -*-

import delegator


def test_simple_usage(monkeypatch):
    """Check that cli shows prefixed variables."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator.run('dump-env -p SOM_TT_')
    assert variables.out == 'VALUE=1\n'


def test_both_options(monkeypatch, env_file):
    """Check with template and prefix.

    Cli must show all prefixed variables by template.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator.run('dump-env -p SOM_TT_ -t ' + env_file)
    assert variables.out == 'NORMAL_KEY=SOMEVALUE\nVALUE=1\n'


def test_multiple_prefixes(monkeypatch):
    """Check that cli with multiple prefixes.

    Cli must show all prefixed variables correctly.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('ANOTHER_TT_VALUE', '2')

    variables = delegator.run('dump-env -p SOM_TT_ -p ANOTHER_TT_')
    assert variables.out == 'VALUE=2\n'


def test_simple_usage_file_output(monkeypatch, tmpdir):
    """Check that cli puts prefixed variables into file correctly."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    filename = tmpdir.mkdir('tests').join('.env').strpath

    delegator.run('dump-env -p SOM_TT_ > ' + filename)

    with open(filename) as env_file:
        assert env_file.read() == 'VALUE=1\n'


def test_strict_no_option():
    """Strict option without other options should give an error."""
    error = delegator.run('dump-env --strict')
    assert error.err == (
        'For --strict option either strict variables ' +  # noqa: W504
        'or template should be given.\n'
    )


def test_strict_with_template(env_file):
    """All variables from template should exists in os envs."""
    error = delegator.run('dump-env --strict -t ' + env_file)
    assert error.err == (
        'Environment variables for keys: NORMAL_KEY - does not set\n'
    )
