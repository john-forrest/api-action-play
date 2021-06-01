#!/usr/bin/env -S bash -l

# Post comment to Issue #1 of john-forrest/actions-test-repo

if [ -z "$REPO_TOKEN" ] ; then
  echo "REPO_TOKEN is not set"
  exit 1
fi

python3 /post_comment.py
