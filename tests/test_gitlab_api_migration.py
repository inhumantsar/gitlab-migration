#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gitlab_migration` package."""

import pytest
from click.testing import CliRunner

from gitlab_migration import gitlab_migration
from gitlab_migration import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    pass


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    pass


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    # test no args
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'gitlab_migration.cli.main' in result.output

    # test help command
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
