# -*-coding:Utf-8 -*


#--------------------------------------------------------------------------------
# jtlib: test_client.py
#
# jtlib module client test code.
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


import jtlib.client as client
import pytest
import re


@pytest.fixture(scope = 'session')
def timeout():
    """Time out for HTTP/HTTPS connections."""
    return 5.0 # seconds; see http://docs.python-requests.org/en/master/user/quickstart/#timeouts


def test_client_without_url_argument(timeout):
    """Check client when no server URL argument is provided."""
    with pytest.raises(client.InvalidUrl) as excinfo:
        client.Jira(str(), timeout=timeout)


def test_client_with_invalid_url_argument(timeout):
    """Check client when an invalid server URL argument is provided."""
    with pytest.raises(client.InvalidUrl) as excinfo:
        client.Jira('https://www.example.com', timeout=timeout)


def test_client_without_url_argument(timeout):
    """Check client when no server URL argument is provided.

    In most cases, this is going to look for a Jira server on the local host.
    """
    with pytest.raises(client.InvalidUrl) as excinfo:
        client.Jira(str(), timeout=timeout)


def test_client_with_invalid_url_argument(timeout):
    """Check client when an invalid server URL argument is provided."""
    with pytest.raises(client.InvalidUrl) as excinfo:
        client.Jira('https://www.example.com', timeout=timeout)


def test_client_with_valid_url_argument():
    """Check client when an invalid server URL argument is provided."""
    client.Jira('https://jira.atlassian.com')


@pytest.fixture(scope = 'module')
def the_client():
    """Return a usable JIRA client."""
    return client.Jira('https://jira.atlassian.com')


@pytest.fixture(scope = 'session')
def project_key_regex():
    """Regular expression for project key."""
    return re.compile(r"""^[A-Z][A-Z]+$""") # Default project key for JIRA Server 7.1.


def test_client_projects_method(the_client, project_key_regex):
    """Check the projects method."""
    projects = the_client.projects()
    assert isinstance(projects, list)
    for project in projects:
        assert project_key_regex.match(project.key)


def test_client_issue_method(the_client):
    issue = the_client.issue('CLOUD-10000')
    assert 'CLOUD-10000' in issue.key


def test_client_search_method(the_client):
    page_count = 0
    for issue in the_client.search('PROJECT = CLOUD'):
        if page_count > (client.Jira.maximum_search_results + 1): # Retrieve two pages of issues.
            break
        page_count += 1
    assert page_count > 0, "JIRA project has too few issues to test search algorithm."
