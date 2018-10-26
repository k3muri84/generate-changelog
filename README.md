# generate-changelog
generates changelog with jira-tickets from git and sets version in jira tickets

## Goals
Create a changelog for a release listing all Jira tickets since last release (in this case the last tag)
Also set the fix version in Jira so one can see later in which release it was included.

## Alternatives
If you just look for a changelog generator for github, jump to [this](https://github.com/github-changelog-generator/github-changelog-generator).
There is also a [js based changelog generator](https://github.com/lob/generate-changelog).

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
