# generate-changelog
generates changelog with jira-tickets from git and sets version in jira tickets

## Goals
Many developers working with Jira all workday. This tools creates a changelog for a release listing all Jira tickets since last release (in this case the last tag) and sets the fix version in Jira so one can see later in which release it was included. This way everyone gets the best of two worlds - having a [changelog][1] and see version info on Jira tickets.

## Alternatives
If you just look for a changelog generator for github, jump to [this](https://github.com/github-changelog-generator/github-changelog-generator).
There is also a [js based changelog generator](https://github.com/lob/generate-changelog).
None of them is dealing with jira.

## Open ToDos
- [ ] get auth for jira, see https://jira.readthedocs.io/en/latest/examples.html#authentication
- [ ] query type and summary for the collected jira issues
- [ ] generate changelog file - following [keepachangelog][1]
- [ ] read current release version
- [ ] set release / fix version in jira

## Requirements
- python 2.x
- [jira-python](https://github.com/pycontribs/jira)
    - install via `pip install jira`

[1]: https://keepachangelog.com/en/1.0.0/
