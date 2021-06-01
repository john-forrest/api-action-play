#!/usr/bin/env python3

# Main API reference https://docs.github.com/en/rest/reference/repos#update-branch-protection
# Also https://stackoverflow.com/questions/51020398/github-api-enable-push-restrictions-for-branch
# but that might be slightly old.

import requests
import os
import sys

repo = 'john-forrest/actions-test-repo'
repo_token = os.environ['REPO_TOKEN']
github_actor = os.environ['GITHUB_ACTOR']
github_repository = os.environ['GITHUB_REPOSITORY']
input_test_param = os.environ['INPUT_TEST_PARAM']

if input_test_param.upper() == "READ":
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

else:
    # normal operation - try and set the rules
    for pattern in ("develop", "release-*"):
        url = 'https://api.github.com/repos/{0}/branches/{1}/protection'.format(repo, pattern)
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
                    "required_approving_review_count": 1
                },
                "allow_deletions": False,
                "restrictions": {
                    "users": [],
                    "teams": []
                },
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
