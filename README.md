# generate-changelog
generates changelog with jira-tickets from git and sets version in jira tickets

## Goals
Many developers working with Jira all workday. This tools creates a changelog for a release listing all Jira tickets since last release (in this case the last tag) and sets the fix version in Jira so one can see later in which release it was included. This way everyone gets the best of two worlds - having a [changelog][1] and see version info on Jira tickets.

## Alternatives
If you just look for a changelog generator for github, jump to [this](https://github.com/github-changelog-generator/github-changelog-generator).
There is also a [js based changelog generator](https://github.com/lob/generate-changelog).
None of them is dealing with jira.

## Open ToDos
- [x] get auth for jira, see https://jira.readthedocs.io/en/latest/examples.html#authentication
- [x] query type and summary for the collected jira issues
- [ ] insert changeset to changelog file
- [x] set release / fix version in jira
- [ ] if list is empty show alternative output with version info
- [ ] optional: transition issues
- [ ] optional: insert build types (e.g. beta or production)

## Requirements
- Python 2.x
  - `pip` for installing dependencies
- jira admin rights - to create fix versions

## Setup

On Python 3.3 and up, start the [virtual environment][1] in order to keep everything self-contained:

    % python3 -m venv environment
    % source environment/bin/activate

Install the dependencies:

    % pip install -r requirements.txt

### Running the script

Make sure your working directory is in the repository folder. Now, just execute it:

    % ./generate-changelog.py


## Configuration
### version info
currently the script parses a gradle property file, tweak the script to your needs, PR
welcome

### git
git log to find all changes since last tag (use on master only, only uses commit messages)
`git_cmd = 'git log $(git describe --abbrev=0 --tag)...HEAD --format="%s"'`
or
if you want to scan branch infos too use instead:
`git_cmd = 'git log $(git describe --abbrev=0 --tag)...HEAD --oneline --decorate'`

## Dependencies

- [jira-python](https://github.com/pycontribs/jira)

[1]: https://keepachangelog.com/en/1.0.0/
[2]: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
