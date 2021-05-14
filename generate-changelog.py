#!/usr/bin/env python3

# script taken from: https://github.com/echorebel/generate-changelog
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

# ~^~^~^~ user config ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# point to your jira installation
jira_server = 'https://jira.yourdomain.com'

"""
configure authentication, see jira module docs for more auth modes
https://jira.readthedocs.io/en/latest/examples.html#authentication
"""
jira = JIRA(server=(jira_server), basic_auth=('changelogbot', 'cryp71cp455w0rd'))

changelogFilename = "CHANGELOG.md"

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

# generate markdown with hyperlinks
render_link = False

# ^-^-^ END user config ^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^


project_format = r'[A-Z][A-Z\d]+'
git_cmd = 'git log $(git describe --abbrev=0 --tag)..HEAD --format="%s"'

projects = []
issues = []
added = []
bugs = []


def load_properties(filepath, sep='=', comment_char='#'):
    """
    parse version this example uses a gradle property file
    load_properties taken from:
    https://stackoverflow.com/questions/3595363/properties-file-in-python-similar-to-java-properties#8220790
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            elements = line.strip()
            if elements and not elements.startswith(comment_char):
                key_value = elements.split(sep)
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
    issue_pattern = r'{}-[\d]+'.format(project_format)
    try:
        result = subprocess.check_output(git_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
    for line in result.decode('utf-8').splitlines():
        issue_id_match = re.search(issue_pattern, line)
        if issue_id_match:
            found_issue_id = issue_id_match.group()
            issues.append(found_issue_id)
            collect_project(found_issue_id)
    return list(set(issues))


def collect_project(issue_id):
    project_id = issue_id.split("-", 1)[0]
    if project_id not in projects:
        projects.append(project_id)


def create_versions(release_version):
    for project in projects:
        version_exists = False
        versions = jira.project_versions(project)
        for version in versions:
            if version.name == release_version.name:
                version_exists = True
                break

        sys.stdout.write('version ' + release_version.name
                         + ' in project ' + project)
        if(version_exists):
            print(' exists - not creating one')
        else:
            print(' not found - creating it!')
            try:
                jira.create_version(release_version.name, project).name
            except JIRAError as e:
                print('Not able to create version for: ' + project
                      + '! Please check if script user has admin rights')
                pass


def render(issue):
    if(render_link):
        issue_url = jira_server + "/browse/" + issue.key
        issue_line = (" * [" + issue.key + "](" + issue_url + ") "
                      + issue.fields.summary + "\n")
    else:
        issue_line = " * " + issue.key + " " + issue.fields.summary + "\n"
    return issue_line


props = load_properties('gradle.properties')
release = type('', (), {})()
release.name = (props['versionMajor'] + '.'
                + props['versionMinor']
                + '.' + props['versionPatch'])

issues = scan_for_tickets()
create_versions(release)
for issueCode in issues:
    try:
        issue = jira.issue(issueCode)
    except JIRAError as e:
        print(issueCode + "not found")
    set_fixVersions(issue, release)
    if issue.fields.issuetype.name in bugTypes:
        bugs.append(issue)
    elif issue.fields.issuetype.name in ignoredTypes:
        # ignore issue type; continue with the next one.
        continue
    elif issue.fields.issuetype.name in featureTypes:
        added.append(issue)
    else:
        added.append(issue)

changelogHeading = "## [" + release.name + "] " + buildType + " " \
                    + props['buildNumber'] + " - " \
                    + datetime.today().strftime("%Y-%m-%d") + "\n"
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

print(changelog)

# writing additional file with just the changes for custom usage
# e.g slack notifications, tweak for your needs
notificationHeading = ":android: " + release.name + " " + buildType \
    + " (" + props['buildNumber'] + ") released\n"
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

