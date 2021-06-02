#!/usr/bin/env python3

# Main API reference https://docs.github.com/en/rest/reference/repos#update-branch-protection
# Also https://stackoverflow.com/questions/51020398/github-api-enable-push-restrictions-for-branch
# but that might be slightly old.
# See https://gist.github.com/pelson/47c0c89a3522ed8da5cc305afc2562b0 for github app access gists

import requests
import jwt
import os
import sys
import re
import time

repo = 'john-forrest/actions-test-repo'
app_key = os.environ['APP_KEY']
github_actor = os.environ['GITHUB_ACTOR']
github_repository = os.environ['GITHUB_REPOSITORY']
input_test_param = os.environ['INPUT_TEST_PARAM']

app_id = 118400 # hardwire for the moment

# Whatever we do, get repo_token from the app so we can access the test repo

time_since_epoch_in_seconds = int(time.time())
payload = {
  # issued at time
  'iat': time_since_epoch_in_seconds,
  # JWT expiration time (10 minute maximum)
  'exp': time_since_epoch_in_seconds + (10 * 60),
  # GitHub App's identifier
  'iss': app_id
}
repo_token = jwt.encode(payload, app_key, algorithm='RS256')

if input_test_param and input_test_param.upper() == "READ":
    # as a test, read all the branches and then read the entries for the designed patterns
    url = 'https://api.github.com/repos/{0}/branches'.format(repo)
    print(url)

    r = requests.get(
        url,
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'Bearer {0}'.format(repo_token)
        }
    )
    print(r.status_code)
    print(r.json())
    if r.status_code not in (200,):
            sys.exit(-1)

    branch_info = r.json()

    for b_info in branch_info:
        # for each branch, get the protection info
        branch_name = b_info["name"]
        print(branch_name)
        protected = b_info["protected"]
        if not protected:
            continue
        url = 'https://api.github.com/repos/{0}/branches/{1}/protection'.format(repo, branch_name)
        r = requests.get(
            url,
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'Bearer {0}'.format(repo_token)
            }
        )
        print(r.status_code)
        print(r.json())
        if r.status_code not in (200,):
            sys.exit(-1)

else:
    # normal operation - try and set the rules. Need to search for branches first so we know which
    # ones exist

    url = 'https://api.github.com/repos/{0}/branches'.format(repo)
    print(url)

    r = requests.get(
        url,
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'Bearer {0}'.format(repo_token)
        }
    )
    print(r.status_code)
    print(r.json())
    if r.status_code not in (200,):
            sys.exit(-1)

    match_trunk_name = re.compile(r"^(develop|release-.*)$")
    branch_info = r.json()
    branch_names = (b_info["name"] for b_info in branch_info)
    trunk_names = [branch_name for branch_name in branch_names if match_trunk_name.match(branch_name)]

    for branch in trunk_names:
        url = 'https://api.github.com/repos/{0}/branches/{1}/protection'.format(repo, branch)
        print(url)

        r = requests.put(
            url,
            headers = {
                'Accept': 'application/vnd.github.luke-cage-preview+json', # enable further features (see doc)
                'Authorization': 'Bearer {0}'.format(repo_token)
            },
            json = {
                "enforce_admins": True,
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": True,
                    "required_approving_review_count": 1,
                    "require_code_owner_reviews": False
                },
                "allow_deletions": False,
#                "restrictions": {
#                    "users": [],
#                    "teams": []
#                },
                "restrictions": None,
                "required_status_checks": {
                    "strict": False,
                    "contexts": []
                }
            }
        )
        print(r.json())
        print(r.status_code)
        if r.status_code not in (200, 201):
            # 201 seems normal exit but 200 too
            sys.exit(-1)
