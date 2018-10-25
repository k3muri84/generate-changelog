# generate-changelog
generates changelog from git

## Goals
Create a changelog for a release listing all Jira tickets since last release (in this case the last tag)
Also set the fix version in Jira so one can see later if he finds the ticket in which release it was included.
Existing solutions use npm which i would like to avoid and therefore use python.

## Open ToDos
- [ ] get auth for jira, see https://jira.readthedocs.io/en/latest/examples.html#authentication
- [ ] query type and summary for the collected jira issues
- [ ] generate changelog file - following https://keepachangelog.com/en/1.0.0/
- [ ] read current release version
- [ ] set release / fix version in jira

## Requirements
- python 2.x
- [jira-python](https://github.com/pycontribs/jira)
    - install via `pip install jira`
