#--------------------------------------------------------------------------------
# jtlib: test_project.py
#
# Test code for the project module.
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
import jtlib
import pytest


def test_projects_valid_url_argument(runner, context):
    """Check project group command result for a JIRA server."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'projects', ], obj = context)
    assert 0 == result.exit_code
    assert 'CLOUD' in result.output


command_list = [
    'project',
]

@pytest.fixture(scope = 'module', params = command_list)
def command(request):
    return request.param


def test_command_with_missing_project(runner, context, server_url, command):
    """Check command without specifying a project."""
    result = runner.invoke(jtlib.scripts.jt, [ server_url, command ], obj = context)
    assert 2 == result.exit_code
    assert 'Usage:' in result.output


bad_project_list = [
    'CLOUDY', # Nonexistant project, match project key regular expression.
    '123', # Malformed project name.
]

@pytest.fixture(scope = 'module', params = bad_project_list)
def bad_project(request):
    return request.param


def test_command_with_nonexistent_project(runner, context, server_url, command, bad_project):
    """Check command specifying a nonexistant project."""
    result = runner.invoke(jtlib.scripts.jt, [ server_url, command, bad_project ], obj = context)
    assert 2 == result.exit_code
    assert 'Usage:' in result.output


def test_command_invalid_url_argument(runner, context, command):
    """Check project group command result for a server."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://www.example.com', command ], obj = context)
    assert 2 == result.exit_code
    assert 'Usage:' in result.output
