# -*-coding:Utf-8 -*


#--------------------------------------------------------------------------------
# jtlib: test_jt.py
#
# Test file for package console and script entry point.
#--------------------------------------------------------------------------------
# BSD 2-Clause License
#
# Copyright (c) 2018, Brian Minard
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#--------------------------------------------------------------------------------


from click.testing import CliRunner
import click
import pkg_resources
import pytest
import subprocess
import jtlib


def check_call(*args):
    """Verify script return code.

    Args:
        args: command-line arguments

    Returns:
        return code.

    Raises:
        CalledProcessError: whenever the subprocess cannot be properly envoked.
    """
    try:
        return subprocess.check_call(list(args))
    except subprocess.CalledProcessError as e:
        return e.returncode


def check_output(*args):
    """Verify script text output.

    Args:
        args: command-line arguments

    Returns:
        return code.

    Raises:
        CalledProcessError: whenever the subprocess cannot be properly envoked.
    """
    try:
        return subprocess.check_output(list(args))
    except subprocess.CalledProcessError as e:
        return e.returncode


scripts = [ pkg_resources.resource_filename(__name__, "jt.py"), ]


@pytest.mark.parametrize("script", scripts)
def test_script_subcommand_no_arguments(script):
    """Basic validation of script without any command-line arguments."""
    assert 0 == check_call(script), "expected zero return code"


def test_main_without_url_argument():
    """Check main command when no server URL argument is provided."""
    runner = CliRunner()
    result = runner.invoke(jtlib.scripts.jt)
    assert 0 == result.exit_code
    assert 'Usage:' in result.output


def test_main_with_invalid_url_argument(runner, context, server_url):
    """Check main command when an invalid server URL argument is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ server_url ], obj = context)
    assert 2 == result.exit_code
    assert 'Usage:' in result.output
