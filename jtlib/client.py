#--------------------------------------------------------------------------------
# jtlib: client.py
#
# Interface to the JIRA client module.
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


import jira


class InvalidQuery(Exception):
    """Exception identifying an invalid query."""
    pass


class InvalidUrl(Exception):
    """Exception identifying an invalid URL."""
    pass


class Jira(object):
    """Encapsulate JIRA client instantiation."""

    maximum_search_results = 50 # Number of issues returned in a search.

    def __init__(self, url, **kwargs):
        """Contruct the JIRA client object.

        Args:
          url: JIRA server URL
          kwargs: keyword arguments passed directly to client
        """
        try:
            self._JIRA = jira.JIRA(url, kwargs)
            assert isinstance(self._JIRA, jira.client.JIRA)
        except:
            raise InvalidUrl("Provided URL isn't a JIRA server.")

    def projects(self):
        """Project accessor.

        Returns: list of JIRA projects host on the JIRA server
        """
        return self._JIRA.projects()


    def issue(self, key):
        """Return all fields for the issue with the specificed key.

        Use this method to collect time related information from a JIRA issue.
        """
        return self._JIRA.issue(key)


    def search(self, jql_query):
        """Search for issues using a JQL query.

        Some JIRA issue information requires using the issue() method to obtain.
        """
        startAt = 0
        while True:
            try:
                result = self._JIRA.search_issues(jql_query, startAt = startAt, maxResults = self.maximum_search_results)
            except jira.JIRAError as excinfo:
                raise JiraServerError(str(excinfo.text) + '.')
            except:
                raise InvalidQuery("Issue search failed.")
            assert isinstance(result, jira.client.ResultList)
            if startAt >= result.total:
                break
            else:
                for issue in result:
                    yield issue # Assume lots of issues.
                startAt += self.maximum_search_results
