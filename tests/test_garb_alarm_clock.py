#!/usr/bin/env python

"""Tests for `garb_alarm_clock` package."""


import unittest
from click.testing import CliRunner

from garb_alarm_clock import garb_alarm_clock
from garb_alarm_clock import cli


class TestGarb_alarm_clock(unittest.TestCase):
    """Tests for `garb_alarm_clock` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'garb_alarm_clock.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
