# Build Status

[![Build Status](https://travis-ci.org/bminard/jtlib.svg?branch=master)](https://travis-ci.org/bminard/jtlib)

# What is JTLIB?

`jtlib` is a Python package using the [JIRA Python Library](https://pypi.python.org/pypi/jira/).
It includes a command-line tool, called `jt`.
Use `jt` to access a JIRA server from the command-line.

# Install

Clone the project from [GitHub](https://github.com/bminard/jtlib).
Run:

 > python setup.py install

Or run the Make file:

 > make init install

# Running

Run `jt` without any arguments to obtain help.

`jt` provides project and issue searches against a JIRA server.

A design goal for `jt` is collect data returned by the JIRA server.
This implies that other tools need to be created to clean the data.
This version of `jt` achieves this goal except as follows.

  1. missing attributes are assigned a _not available_ value
  2. attribute values are encoded as ASCII using backslashes

If the JIRA server requries user authentication, add your credentials to the _.netrc_ file.

# Using

## Projects

To obtain a list of projects hosted by a JIRA server use:

  > jt https://jira.atlassian.com projects

This produces a result like:

```
CLOUD
COMMUNITY
NPS
...
STRIDE
```

## Issues

The issue command creates a comma-separated-value list of issues matching the search criteria.
This list includes a header row to identify columns.
Column names are JQL keywords or issue attribute names,

Columns contain the values obtained from the JIRA server or _N/A_.
_N/A_ identifies a missing value.

The issue command includes options for restricting issue selection by time and ordering issues.

Time is expressed using ithe since and until options.
Since uses greater than or equal to the time; until is less than or equal.
Issue Order uses JQL functions and keywords.

### List All Issues

To obtain all issues assigned to a project use:

 > jt https://jira.atlassian.com issue TRANS

This produces a result like:

```
issuekey,type,status,summary,created,original estimate,remaining estimate
TRANS-2523,Bug,Open,Korean translation mistake for TO in Team Calendar ,2018-01-22T23:02:09.230+0000,N/A,N/A
TRANS-2522,Bug,Open,Czech translation is incomplete in Service Desk,2017-10-11T15:25:41.321+0000,N/A,N/A
...
```

### Obtain an Issue

To obtain an issue use:

 > jt https://jira.atlassian.com issue TRANS-1234

This produces a result like:

```
issuekey,type,status,summary,created,original estimate,remaining estimate
TRANS-1234,Bug,Resolved,Investigate performance issues with PrepopulateWithSuggestedEntriesJob,2015-05-13T11:00:41.666+0000,N/A,N/A
```

### Obtain Issue Work Logs

To obtain an issue work log use:

 > jt https://jira.atlassian.com issue --worklog SRCTREEDEV-221

This produces a result like:

```
issuekey,type,status,created,start time,time spent
SRCTREEDEV-221,bganninger,2015-11-20T21:14:00.000+0000,4d
SRCTREEDEV-221,bganninger,2015-11-23T21:04:00.000+0000,8m
SRCTREEDEV-221,bganninger,2015-11-23T21:05:00.000+0000,7h 52m
```

# Why a command-line tool for JIRA?

This tool arose out of an exploration of the Python JIRA package API.
There are many tools for JIRA available at [PyPi](https://pypi.python.org/pypi?%3Aaction=search&term=jira&submit=search).

Thanks to everyone who worked on the [JIRA Python Library](https://github.com/pycontribs/jira).
