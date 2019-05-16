#!/usr/bin/env python

# regex part inspired by the commit hook script:
# https://github.com/pbetkier/add-issue-id-hook
# needs jira-python https://github.com/pycontribs/jira
# install via `pip install jira`
# https://jira.readthedocs.io/en/master/api.html#issue

import subprocess
import re
from jira import JIRA, JIRAError
from datetime import datetime

# The base URL of your Jira installation.
# Must not have a trailing slash!
jiraBaseUrl = 'https://jira.yourdomain.com'

jira = JIRA(server=(jiraBaseUrl), auth=('changelogbot', 'cryp71cp455w0rd'))
# configure your jira project or just leave it to find all
project_format = '[A-Z][A-Z]+'
# define jira project to create version
project_version = 'CORE'

# Flag whether the script should automatically add the "version" information
# to the issues in Jira.
is_update_fix_versions_enabled = True

# configure possible issue types
bugTypes = ['Bug', 'InstaBug']
featureTypes = ['Story, Task']
refactoringTypes = ['Refactoring'] 

changelogFilename = "CHANGELOG.md"

# git log to find all changes since last tag (use on master only, only uses commit messages)
git_cmd = 'git log $(git describe --abbrev=0 --tag)..HEAD --format="%s"'
# if you want to print branch infos too use lightly different output
# git_cmd = 'git log $(git describe --abbrev=0 --tag)..HEAD --oneline --decorate'

# parse version this example uses a gradle property file
# load_properties taken from:
# https://stackoverflow.com/questions/3595363/properties-file-in-python-similar-to-java-properties#8220790
def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file and return as dict
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def set_fixVersions(issue, version):
    if not is_update_fix_versions_enabled:
        # The user chose not to update the fix version; don't continue.
        return

    fixVersions = []
    for existing_version in issue.fields.fixVersions:
        fixVersions.append({'name': existing_version.name})
    fixVersions.append({'name': version.name})
    try:
        issue.update(fields={'fixVersions': fixVersions})
    except JIRAError as e:
        print(e.status_code, e.text, issue.key)

def scan_for_tickets():
    issue_pattern = '{}-[\d]+'.format(project_format)
    try:
        result = subprocess.check_output(git_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
    for line in result.splitlines():
        issue_id_match = re.search(issue_pattern, line)
        if issue_id_match:
            found_issue_id = issue_id_match.group()
            issues.append(found_issue_id)
    return list(set(issues))

props = load_properties('gradle.properties')
release_version = props['versionMajor'] + '.' + props['versionMinor'] + '.' + props['versionPatch']
version_exists = False
versions = jira.project_versions(project_version)
for version in versions:
    if version.name == release_version:
        version_exists = True
        break

if(version_exists):
    print('version ' + release_version + ' exists - dont create one\n')
else:
    print('version ' + release_version + ' not found - creating it!\n')
    version = jira.create_version(release_version, project_version)

issues = []
added = []
bugs = []

issues = scan_for_tickets()
for issueCode in issues:
    issue = jira.issue(issueCode)
    set_fixVersions(issue, version)
    if issue.fields.issuetype.name in bugTypes:
        bugs.append(issue)
    elif issue.fields.issuetype.name in featureTypes:
        added.append(issue)
    else:
        added.append(issue)

def render_issue(issue):
    issue_url = jiraBaseUrl + "/browse/" + issue.key

    return " * [" + issue.key + "](" + issue_url + ") " + issue.fields.summary + "\n"

changelogHeading = "## [" + release_version + "] Beta " + props['buildNumber'] + " - " + datetime.today().strftime("%Y-%m-%d") + "\n"
changelog = ""
if added:
    changelog += "### Added\n"
    for issue in added:
        changelog += render_issue(issue)
    changelog += "\n"
if bugs:
    changelog += "### Fixed\n"
    for issue in bugs:
        changelog += render_issue(issue)

print(changelog)

f = open("CHANGES.md", "w+")
f.write(changelog)
f.close()

changelog += "\n"
f = open(changelogFilename, "r")
contents = f.readlines()
f.close()
contents.insert(8, changelog)
contents.insert(8, changelogHeading)
f = open(changelogFilename, "w+")
f.writelines(contents)
f.close()

