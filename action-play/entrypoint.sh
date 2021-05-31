#!/usr/bin/env -S bash -l

# Post comment to Issue #1 of john-forrest/actions-test-repo

if [ -z "$REPO_TOKEN" ] ; then
  echo "REPO_TOKEN is not set"
  exit 1
fi

target_repo=john-forrest/actions-test-repo
issue_number=1
curl -s -X POST https://api.github.com/repos/${target_repo}/issues/$issue_number/comments \
            -d "{\"body\":\"Posted by $GITHUB_ACTOR from $GITHUB_REPOSITORY ($INPUT_TEST_PARAM)\"}" \
            -H "Authorization: Bearer $REPO_TOKEN"
