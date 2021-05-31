import requests
import os

repo = 'john-forrest/actions-test-repo'
repo_token = os.environ['REPO_TOKEN']
github_actor = os.environ['GITHUB_ACTOR']
github_repository = os.environ['GITHUB_REPOSITORY']
input_test_param = os.environ['INPUT_TEST_PARAM']
issue_number = 1

r = requests.put(
    'https://api.github.com/repos/{0}/issues/{1}/comments'.format(repo, str(issue_number)),
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'Bearer {0}'.format(repo_token)
    },
    json = {
        "body": "Posted by {0} from {1} ({2})".format(github_actor, github_repository, input_test_param)
    }
)
print(r.json())
print(r.status_code)
if r.status_code != 200:
    os.exit(-1)
