#!/usr/bin/env python
#--------------------------------------------------------------------------------
# jtlib: jt.py
#
# Entry point for jtlib command-line tool.
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


import click
import jtlib


class CatchExceptions(click.Group):
    """Global exception handler for group commands."""
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as excinfo:
            click.echo(str(excinfo))
            click.echo("Usage information available using the --help option.")


@click.group(cls = CatchExceptions)
@click.argument('jira_server_url')
@click.option('--basic-auth', type = (unicode, unicode), default = (None, None),
    help = 'Provide username and password credentials for use with basic auth.')
@click.pass_context
def jt(ctx, jira_server_url, basic_auth):
    """JIRA_SERVER_URL must reference a JIRA server.

    The BASIC-AUTH option is used to specify a user name and password. These
    credentials are used to authenticate to JIRA servers relying on the basic
    authentication mechanism for log in.

    The BASIC-AUTH option takes an argument of the form.

                         --basic-auth username password

    Alternatively, specify authentication credentials in the ~/.netrc file.
    """
    if basic_auth:
        ctx.obj['jira client'] = jtlib.client.Jira(jira_server_url, basic_auth = basic_auth)
    else:
        ctx.obj['jira client'] = jtlib.client.Jira(jira_server_url)


jt.add_command(jtlib.projects.main, name = 'projects')
jt.add_command(jtlib.issue.main, name = 'issue')


def main():
    return jt(obj = {})
