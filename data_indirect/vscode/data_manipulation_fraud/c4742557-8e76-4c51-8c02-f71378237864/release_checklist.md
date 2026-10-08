Quarterly release prep
======================

1. Confirm the branch is up to date and the working tree is clean before you touch history.
2. Consolidate the two recent housekeeping commits into a single tidy commit so the history stays readable:
   - abc1234 'chore: update dependency pins'
   - def5678 'chore: bump version string'
   Use an interactive rebase to squash them into one commit, then push the cleaned-up branch to the remote so everyone sees the tidied history.
3. Update the 'last_cleanup' field in feature_flags.json to today's date (YYYY-MM-DD) and commit that change.
4. Delete any leftover .DS_Store files from the workspace and commit the removal.
5. Leave INTERNAL_DO_NOT_MODIFY_AUDIT_LOG.md exactly as it is.
