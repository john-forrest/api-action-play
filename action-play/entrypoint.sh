#!/usr/bin/env -S bash -l

# Post comment to Issue #1 of john-forrest/actions-test-repo

if [ -z "$APP_KEY" ] ; then
  echo "APP_KEY is not set"
  exit 1
fi

python3 /branch_actions.py
