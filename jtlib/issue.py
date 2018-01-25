#--------------------------------------------------------------------------------
# jtlib: issue.py
#
# The issue command enables lookup of one or more issues hosted on a JIRA server.
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
import csv
import jira
import re
import sys
import types


project_key_regex = re.compile(r"""(?P<project_key>^[A-Z][A-Z]+)$""") # Default project key for JIRA Server 7.1.
issue_key_regex = re.compile(r"""(?P<issue_key>^[A-Z][A-Z]+-\d+)$""") # Default issue key for JIRA Server 7.1.


def get_attribute_value(field, attribute):
    """Recursively traverse the tuple list for accessing an attribute's value.
    """
    if types.TupleType == type(field):
        return get_attribute_value(get_attribute_value(field[0], field[1]), attribute)
    return getattr(field, attribute)


def canonify_value(field, attribute):
    """Inject 'Not Available' value for nonexistent issue fields."""
    try:
        return get_attribute_value(field, attribute).encode('ascii', errors='backslashreplace')
    except (AttributeError, TypeError):
        return 'N/A'


def emit_issue_fields(ctx, issue_list):
    """Print top-level Policy Holder issue fields."""
    writer = csv.writer(sys.stdout)
    writer.writerow([ 'issuekey', 'type', 'status', 'summary', 'created',
        'original estimate', 'remaining estimate',
    ])
    for item in issue_list:
        assert isinstance(item, jira.resources.Issue)
        issue = ctx.obj['jira client'].issue(item.key)
        writer.writerow(map(lambda x: canonify_value(*x), [ (issue, 'key'),
            (((issue, 'fields'), 'issuetype'), 'name'), (((issue, 'fields'), 'status'), 'name'),
            ((issue, 'fields'), 'summary'), ((issue, 'fields'), 'created'),
            (((issue, 'fields'), 'timetracking'), 'originalEstimate'),
            (((issue, 'fields'), 'timetracking'), 'remainingEstimate'),
        ]))


def emit_worklog_fields(ctx, issue_list):
    """Print worklog fields."""
    writer = csv.writer(sys.stdout)
    writer.writerow([ 'issuekey', 'type', 'status', 'created', 'start time',
        'time spent',
    ])
    for issue in issue_list:
        assert isinstance(issue, jira.resources.Issue)
        for worklog in ctx.obj['jira client'].issue(issue.key).fields.worklog.worklogs:
            writer.writerow(map(lambda x: canonify_value(*x), [ (issue, 'key'),
                ((worklog, 'updateAuthor'), 'name'), (worklog, 'started'),
                (worklog, 'timeSpent'),
            ]))


class MalformedKey(Exception):
    """Malformed key exception."""
    pass


@click.command()
@click.argument('key')
@click.option('--since', help = 'Return issues since the specified time stamp.')
@click.option('--until', help = 'Return issues until the specified time stamp.')
@click.option('--worklog/--no-worklog', help = 'Return issue worklogs, if any.', default = False)
@click.option('--order-by', help = 'Specify how to order search results.')
@click.pass_context
def main(ctx, key, since, until, worklog, order_by):
    """Obtain one or more issues using the provided search criteria.

    KEY must be a project key or issue key. If provided only a project key, then
    every issue in the project is returned.

    The SINCE and UNTIL times are applied to the issue creation time stamp.

    SINCE is interpreted as greater than or equal to and UNTIL as less than or
    equal to. Both options are provided directly to the JIRA's JQL query engine,
    so JQL functions specifying time stamps can be used with them (e.g., now()
    or startofday()).

    Specify the time stamp using one of these formats:

      - yyyy/MM/dd HH:mm

      - yyyy-MM-dd HH:mm

      - yyyy/MM/dd

      - yyyy-MM-dd

    The ORDER-BY option affects issue output order. The values provided to this
    option are provided directly to JIRA's JQL query engine (e.g., 'rank asc',
    'rank desc' or created).

    The WORKLOG option affects the issue content. By default, this option is
    disabled. When enabled, the output contains only the issue work log, if
    any. When disabled. it contains other issue information.

    To obtain all ticket information, the issue command must be run with and
    without the WORKLOG option.
    """
    clause = list()
    project_key = project_key_regex.match(key)
    if project_key:
        clause.append('PROJECT = "{}"'.format(project_key.group('project_key')))
    issue_key = issue_key_regex.match(key)
    if issue_key:
        clause.append('ISSUEKEY={}'.format(key))
    if not (issue_key or project_key):
        raise MalformedKey("KEY must be a valid project key or issue key.")
    if since:
        clause.append('CREATED >= {}'.format(since))
    if until:
        clause.append('CREATED <= {}'.format(until))
    if order_by:
        order_by_clause = ' ORDER BY {}'.format(order_by)
    else:
        order_by_clause = ""
    result_list = ctx.obj['jira client'].search(' AND '.join(clause) + order_by_clause)
    if worklog:
        emit_worklog_fields(ctx, result_list)
    else:
        emit_issue_fields(ctx, result_list)
