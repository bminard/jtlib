# JIRA Tool Library (jtlib)

JIRA tool library is a command-line tool leveraging [JIRA Python Library](https://pypi.python.org/pypi/jira/).
Run `jt` without any arguments to obtain help.

`jt` provides project and issue searches against a JIRA server.

## Projects

To obtain a list of projects hosted by a JIRA server use:

  > jt https://jira.atlassian.com projects

Produces a result like:

  > CLOUD
  > COMMUNITY
  > NPS
  > ...
  > STRIDE

## Issues

The issue command creates a comma-separated-value listing of issues matching the specified search criteria.
Each listing has a header row whose column names identify the column values.
Heading names are the JQL keyword generating the value or the issue attribute containing it.

Columns contain the values obtained from the JIRA server or N/A.
N/A indicates the value was not returned by the JQL query.

Issue queries support restrictions imposed by since and until using the creation time.
Since uses greater than or equal to the provided time; until is less than or equal.

Issue queries support order by operations using JQL functions and keywords.

### List All Issues

To obtain a list of all issues assigned to a project use:

 > jt https://jira.atlassian.com issue TRANS

Produces a result like:

 > issuekey,type,status,summary,created,original estimate,remaining estimate
 > TRANS-2523,Bug,Open,Korean translation mistake for TO in Team Calendar ,2018-01-22T23:02:09.230+0000,N/A,N/A
 > TRANS-2522,Bug,Open,Czech translation is incomplete in Service Desk,2017-10-11T15:25:41.321+0000,N/A,N/A
 > ...

### Obtain an Issue

To obtain an issue use:

 > jt https://jira.atlassian.com issue TRANS-1234

Produces a result like:

 > issuekey,type,status,summary,created,original estimate,remaining estimate
 > TRANS-1234,Bug,Resolved,Investigate performance issues with PrepopulateWithSuggestedEntriesJob,2015-05-13T11:00:41.666+0000,N/A,N/A

### Obtain Issue Work Logs

To obtain an issue work log use:

 > jt https://jira.atlassian.com issue --worklog SRCTREEDEV-221

Produces a result like:

 > issuekey,type,status,created,start time,time spent
 > SRCTREEDEV-221,bganninger,2015-11-20T21:14:00.000+0000,4d
 > SRCTREEDEV-221,bganninger,2015-11-23T21:04:00.000+0000,8m
 > SRCTREEDEV-221,bganninger,2015-11-23T21:05:00.000+0000,7h 52m


# Why a command-line tool for JIRA?

This tool arose out of an exploration of the Python JIRA package API.

Thanks to everyone who worked on the [JIRA Python Library](https://github.com/pycontribs/jira)
