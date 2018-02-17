# -*-coding:Utf-8 -*


#--------------------------------------------------------------------------------
# jtlib: test_issue.py
#
# Test cases for the issue module.
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
import jtlib.issue as issue
import jtlib
import pytest


#
# Handle get attribute value.
#


class A:
    a = 1
    class B:
        b = 2
        class C:
            c = 3


attribute_value_list = [
  (A, 'a', 1),
  ((A, 'B'), 'b', 2),
  (((A, 'B'), 'C'), 'c', 3),
]


@pytest.mark.parametrize("attribute, value, expected", attribute_value_list)
def test_get_attribute_value(attribute, value, expected):
    assert issue.get_attribute_value(attribute, value) == expected


#
# Handle canonify method.
#


class canonify(object):
    """A test class for canonifying the value of unavailable attribute-value pairs."""
    value = 'True'


def test_canonify_value_when_attribute_exists():
    """Test that canonify returns the correct value."""
    assert 'True' == issue.canonify_value(canonify(), 'value')


def test_canonify_value_when_attribute_do_not_exist():
    """Test that canonify returns a representative value when the attribute is not defined."""
    assert 'N/A' in issue.canonify_value(canonify(), 'missing_value')


#
# Handle key argument.
#


def test_issue_valid_url_argument_invalid_key(runner, context):
    """Check issue group command result when an invalid key is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', '123' ], obj = context)
    assert -1 == result.exit_code
    assert result.output.find('Usage')


key_list = [
    'TRANS-1871', # Issue key containing originalEstimate and remainingEstimate fields.
    'CLOUD-10000', # Issue key missing originalEstimate and remainingEstimate fields.
]


@pytest.fixture(scope = 'module', params = key_list)
def key(request):
    return request.param


trans_project_output_list = [
    'TRANS-2421,Task,Resolved,Create a script that finds all English i18n files and merges them into 1 big JIRA properties file,2017-06-29T03:59:55.237+0000,N/A,17h',
    'TRANS-2131,Bug,Resolved,New versions of JIRA-Software isnt appering in Português do Brasil,2016-05-12T00:45:51.793+0000,N/A,N/A', # UTF-8 test string.
    'TRANS-1898,Bug,Resolved,Grails-3: Some characters are encoded on product import popup,2016-02-05T15:00:20.533+0000,N/A,N/A',
    'TRANS-1871,Bug,Resolved,functionality issue,2016-01-25T05:15:35.706+0000,32h,32h',
]


@pytest.fixture(scope = 'module', params = trans_project_output_list)
def trans_project_output(request):
    return request.param


@pytest.fixture(scope = 'module')
def trans_key(runner, context):
    return runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', 'TRANS', '--since', '2016-01-25', '--until', '2017-06-30' ], obj = context)


def test_issue_valid_url_argument_valid_key_trans(trans_key, trans_project_output):
    assert 0 == trans_key.exit_code
    assert trans_project_output in trans_key.output


def test_issue_valid_url_argument_valid_key(runner, context, key):
    """Check issue group command result for an issue."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', key ], obj = context)
    assert 0 == result.exit_code
    assert key in result.output


#
# Handle time options.
#


time_option_list = [
    '--since',
    '--until',
]


@pytest.fixture(scope = 'module', params = time_option_list)
def time_option(request):
    return request.param


def test_issue_valid_url_argument_valid_key_invalid_time_stamp(runner, context, key, time_option):
    """Check issue group command when an invalid time stamp is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', key, time_option, '2018-14-01' ], obj = context)
    assert -1 == result.exit_code


def test_issue_valid_url_argument_valid_key_valid_time_stamp(runner, context, key, time_option):
    """Check issue group command when an invalid time stamp is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', key, time_option, '2018-01-14' ], obj = context)
    assert 0 == result.exit_code


@pytest.fixture(scope = 'module')
def stride_project_result(runner, context):
    return runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', 'STRIDE', '--since', '2018-01-01', '--until', '2018-01-02' ], obj = context)


stride_project_output_list = [
    'Issue key,Issue Type,Status,Summary,Created,Original Estimate,Remaining Estimate',
    'STRIDE-1786,Suggestion,To be reviewed,Google Calendar Integration,2018-01-01T19:53:30.305+0000,N/A,N/A',
    'STRIDE-1784,Suggestion,To be reviewed,Check post,2018-01-01T11:47:52.366+0000,N/A,N/A',
]


@pytest.fixture(scope = 'module', params = stride_project_output_list)
def stride_project_expected_output(request):
    return request.param


def test_issue_valid_url_argument_valid_project_valid_time_stamp_range(stride_project_result, stride_project_expected_output):
    """Check issue group command when an invalid time stamp is provided."""
    assert 0 == stride_project_result.exit_code
    assert stride_project_expected_output in stride_project_result.output


#
# Handle worklog option.
#


trans_1871_output_list = [
    'Issue key,Issue Type,Status,Summary,Created,Original Estimate,Remaining Estimate',
    'TRANS-1871,Bug,Resolved,functionality issue,2016-01-25T05:15:35.706+0000,32h,32h',
]


@pytest.fixture(scope = 'module', params = trans_1871_output_list)
def trans_1871_expected_output(request):
    return request.param


def test_issue_valid_url_argument_valid_key_estimates(runner, context, trans_1871_expected_output):
    """Check issue group command when an invalid time stamp is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', 'TRANS-1871', ], obj = context)
    assert 0 == result.exit_code
    assert trans_1871_expected_output in result.output


scrtreedev_project_output_list = [
    'Issue key,Issue Type,Status,Created,Start Time,Time Spent',
    'SRCTREEDEV-221,bganninger,2015-11-20T21:14:00.000+0000,4d',
    'SRCTREEDEV-221,bganninger,2015-11-23T21:04:00.000+0000,8m',
    'SRCTREEDEV-221,bganninger,2015-11-23T21:05:00.000+0000,7h 52m',
]


@pytest.fixture(scope = 'module', params = scrtreedev_project_output_list)
def scrtreedev_project_expected_output(request):
    return request.param


def test_issue_valid_url_argument_valid_key_worklog(runner, context, scrtreedev_project_expected_output):
    """Check issue group command when an invalid time stamp is provided."""
    result = runner.invoke(jtlib.scripts.jt, [ 'https://jira.atlassian.com', 'issue', '--worklog', 'SRCTREEDEV-221', ], obj = context)
    assert 0 == result.exit_code
    assert scrtreedev_project_expected_output in result.output


#
# Handle order by option.
#


order_by_list = [
    'https://jira.atlassian.com', 'issue', 'STRIDE', '--since', '2018-01-01', '--until', '2018-01-02',
]


def test_order_by(runner, context):
    ascending = runner.invoke(jtlib.scripts.jt, order_by_list + [ '--order-by', 'rank asc', ], obj = context).output.splitlines()
    descending = runner.invoke(jtlib.scripts.jt, order_by_list + [ '--order-by', 'rank desc', ], obj = context).output.splitlines()
    d = len(descending) - 1
    for a in range(1, len(ascending)):
        assert ascending[a] == descending[d]
        d -= 1
