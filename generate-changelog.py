#!/usr/bin/env python

# regex part inspired by the commit hook script:
# https://github.com/pbetkier/add-issue-id-hook
# needs jira-python https://github.com/pycontribs/jira
# install via `pip install jira`
# https://jira.readthedocs.io/en/master/api.html#issue

import sys
import subprocess
import re
from jira import JIRA, JIRAError
from datetime import datetime

# point to your jira installation
jira_server = 'https://jira.yourdomain.com'

# configure authentication to your needs, see jira module docs for more auth modes
jira = JIRA(server=(jira_server), auth=('changelogbot', 'cryp71cp455w0rd'))

# configure your jira project or just leave it to find all
project_format = '[A-Z][A-Z\d]+'

# define jira projects to create version
projects = ['CORE', 'PAS','DC']

# configure possible issue types
bugTypes = ['Bug', 'InstaBug']
featureTypes = ['Story', 'Task']
refactoringTypes = ['Refactoring']
ignoredTypes = ['Sub-task']

# if you building different types (alpha,beta,production) and
# want to differ in the changelog, specify default here and/or
# pass it as first argument
buildType = "Release"
if len(sys.argv) > 1:
    buildType = sys.argv[1]

changelogFilename = "CHANGELOG.md"

# generate markdown with hyperlinks
render_link = False

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

def render(issue):
    if(render_link):
        issue_url = jira_server + "/browse/" + issue.key
        issue_line = " * [" + issue.key + "](" + issue_url + ") " + issue.fields.summary + "\n"
    else:
        issue_line = " * " + issue.key + " " + issue.fields.summary + "\n"
    return issue_line

props = load_properties('gradle.properties')
release_version = props['versionMajor'] + '.' + props['versionMinor'] + '.' + props['versionPatch']

for project in projects:
    version_exists = False
    versions = jira.project_versions(project)
    for version in versions:
        if version.name == release_version:
            version_exists = True
            break

    if(version_exists):
        print('version ' + release_version + ' in project ' + project + ' exists - dont create one\n')
    else:
        print('version ' + release_version + ' in project ' + project + ' not found - creating it!\n')
        try:
            version = jira.create_version(release_version, project)
        except JIRAError as e:
            print('Not able to create version for: ' + project.name + '! Please check if script has admin rights')

issues = []
added = []
bugs = []

issues = scan_for_tickets()
for issueCode in issues:
    try:
        issue = jira.issue(issueCode)
    except JIRAError as e:
        print(issueCode + "not found")
    set_fixVersions(issue, version)
    if issue.fields.issuetype.name in bugTypes:
        bugs.append(issue)
    elif issue.fields.issuetype.name in ignoredTypes:
        # This issue is of a type that we want to ignore; continue with the next one.
        continue
    elif issue.fields.issuetype.name in featureTypes:
        added.append(issue)
    else:
        added.append(issue)

changelogHeading = "## [" + release_version + "] " + buildType + " " + props['buildNumber'] + " - " + datetime.today().strftime("%Y-%m-%d") + "\n"
changelog = ""
if added:
    changelog += "### Added\n"
    for issue in added:
        changelog += render(issue)
    changelog += "\n"
if bugs:
    changelog += "### Fixed\n"
    for issue in bugs:
        changelog += render(issue)

changelog = changelog.encode('utf8', 'replace')
print(changelog)

# writing additional file with just the changes for custom usage
# e.g slack notifications, tweak for your needs
notificationHeading = ":android: " + release_version + " " + buildType + " (" + props['buildNumber'] + ") released\n"
f = open("CHANGES.md", "w+")
f.write(notificationHeading)
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
