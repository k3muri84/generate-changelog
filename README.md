# generate-changelog
generates changelog with jira-tickets from git and
create/set version in jira tickets

## Goals
Many developers working with Jira all workday. This tools creates a changelog
for a release listing all Jira tickets since last release (in this case the
last tag) and sets the fix version in Jira so one can see later in which
release it was included. This way everyone gets the best of two worlds:
having a [changelog][1] and see version info on Jira tickets.

## Alternatives
If you just look for a changelog generator for github, jump to [this](https://github.com/github-changelog-generator/github-changelog-generator).
There is also a [js based changelog generator](https://github.com/lob/generate-changelog).
None of them is dealing with jira.

## ToDos
- [x] get auth for jira, see https://jira.readthedocs.io/en/latest/examples.html#authentication
- [x] query type and summary for the collected jira issues
- [x] insert changeset to changelog file
- [x] set release / fix version in jira
- [x] support unicode in jira titles
- [x] optional: insert build types (e.g. beta or production)
- [x] migrate to python3
- [ ] if list is empty show alternative output with version info
- [ ] detect shallow clone and error
- [ ] optional: transition issues
- [ ] jira cloud support

## Requirements
- python 3.x
- `pip` for installing jira module
- [jira-python](https://github.com/pycontribs/jira)
    - install via `pip install jira`
- user with jira project admin rights - to create fix versions
- or api token https://id.atlassian.com/manage-profile/security/api-tokens
  see also https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
  and https://jira.readthedocs.io/examples.html#authentication

## Usage

### basic configuration
- setup jira url
- define jira projects in which fix version should be created
- configure possible issue type for your project
- export JIRA_SERVER url, JIRA_USER and JIRA_PASSWORD to environment


### getting version info
currently the script parses a gradle property file, tweak the script to your needs: e.g. pass info via argument, PR
welcome

### git history
Default: using git log to find all changes since last tag (use on master only, only uses commit messages)
`git_cmd = 'git log $(git describe --abbrev=0 --tag)...HEAD --format="%s"'`
or if you want to scan branch infos too use instead:
`git_cmd = 'git log $(git describe --abbrev=0 --tag)...HEAD --oneline --decorate'`

### Quick Usage
execute `./generate-changelog.py` in the repository folder


[1]: https://keepachangelog.com/en/1.0.0/

