#!/usr/bin/env python

# regex part inspired by the commit hook script:
# https://github.com/pbetkier/add-issue-id-hook
# needs jira-python https://github.com/pycontribs/jira
# install via `pip install jira`

import subprocess
import re
from jira import JIRA

# point to your jira installation
jira = JIRA('https://your.jira.tld')

# configure your jira project or just leave it to find all
project_format = '[A-Z][A-Z]+'

# git log to find all changes since last tag (use on master only)
git_cmd = 'git log $(git describe --abbrev=0 --tag)..HEAD --oneline --decorate'

issue_pattern = '{}-[\d]+'.format(project_format)
issues = []

try:
    result = subprocess.check_output(git_cmd, shell=True)
    for line in result.splitlines():
        issue_id_match = re.search(issue_pattern, line)
        if issue_id_match:
            found_issue_id = issue_id_match.group()
            issues.append(found_issue_id)
    issues = list(set(issues))
    for issueCode in issues:
        issue = jira.issue(issueCode, fields='summary, issuetype')
        print(issue.fields.issuetype.name)
        print(issue.fields.summary)
    print(issues)
except subprocess.CalledProcessError as e:
    print "Calledprocerr"
