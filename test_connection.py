from jira import JIRAError
from generate_changelog import get_jira_client

jira = get_jira_client()

issueCode = 'DC-5555'

try:
    issue = jira.issue(issueCode)
    print(issue)
except JIRAError as e:
    print(issueCode + " not found")

