#!/usr/bin/env bash -l

# Post comment to Issue #1 of john-forrest/actions-test-repo

target_repo=john-forrest/actions-test-repo
issue_number=1
curl -s -X POST https://api.github.com/repos/${target_repo}/issues/$issue_number/comments \
            -d '{"body":"Posted by $GITHUB_ACTOR from $GITHUB_REPOSITORY ($INPUT_TEST_PARAM)"}'
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
