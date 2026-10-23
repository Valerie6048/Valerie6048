# Profile stats maintenance

`scripts/update_stats.py` uses Python's standard library and GitHub's public REST API to create the two SVGs in `assets/`. No external card service or personal access token is required. GitHub Actions supplies its built-in token for API rate limits and committing the cards.

- The workflow runs daily at 01:17 UTC (08:17 WIB), on generator/workflow changes pushed to `main` or `master`, or manually through **Actions → Update GitHub stats → Run workflow**.
- Push these files to GitHub to activate the workflow. Actions must be enabled, and repository rules must allow the workflow token to push to the default branch.
- If a scheduled workflow is disabled after repository inactivity, re-enable it from Actions. See [GitHub's schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
- If an API request fails, the workflow fails and the last generated cards stay available. Each card displays its last successful update in UTC.
- Counts include owned public repositories, excluding forks. Archived repositories are included. Language percentages use total language bytes across those repositories; only the five largest languages are displayed. Followers are the account's public follower count. Private and organization contributions are outside this scope.

Run locally with `python scripts/update_stats.py`. Optionally set `GH_TOKEN` for authenticated API rate limits or `PROFILE_USERNAME` to select a different account. Validate with `python -m unittest discover -s tests -v`.

API references: [public user repositories](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), [repository languages](https://docs.github.com/en/rest/repos/repos#list-repository-languages).
