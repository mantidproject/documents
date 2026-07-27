# Repo template and release workflow

Goal: no memorized git command sequences to move a change through dev, qa,
and production, and no manual tagging or publishing steps.

## Structure

```
main                    ← the only long-lived branch, protected
  └── feature/xyz       ← short-lived, deleted after merge
```

Branches represent code differences, not deployment stages — conflating the
two is what forces manual merge choreography. Deployment stages are GitHub
Environments instead:

| Environment | Gate |
|---|---|
| `dev` | none — deploys automatically on merge to `main` |
| `qa` | one required reviewer |
| `production` | two required reviewers |

## Walking through a change

1. Branch off `main`, open a PR, click "Merge pull request" in the browser.
   This is the only merge that happens.
2. The build triggered by that merge deploys automatically to `dev`.
3. Promoting to `qa` is "Review deployments → Approve" on that same build —
   same artifact, nothing rebuilt, nothing merged.
4. Same for `production`.
5. "Draft a new release" in the GitHub web UI, publish — GitHub creates the
   tag at that moment, no local `git tag` needed.

## If dropping the visible branches is too much change at once

Keep `dev`, `qa`, `main` as actual branches for familiarity, but have CI
perform the merges, triggered by an environment approval rather than a human
running `git merge`:

```yaml
name: promote
on:
  push:
    branches: [dev]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh

  deploy-dev:
    needs: build
    environment: dev
    runs-on: ubuntu-latest
    steps: [{ run: echo deployed to dev }]

  promote-qa:
    needs: deploy-dev
    environment: qa          # pauses here for approval
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0, token: ${{ secrets.BOT_TOKEN }} }
      - run: |
          git checkout qa
          git merge --ff-only ${{ github.sha }}
          git push origin qa

  promote-main:
    needs: promote-qa
    environment: production  # pauses again
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0, token: ${{ secrets.BOT_TOKEN }} }
      - run: |
          git checkout main
          git merge --ff-only ${{ github.sha }}
          git push origin main
          gh release create "v$(date +%Y.%m.%d)" --generate-notes
```

The `environment:` key on a job is what makes Actions pause for the configured
reviewers. Clicking "Approve" is the entire action that used to be a manual
merge — the merge happens under a bot identity the instant someone approves.

**Setup, one time:**

- A bot/service account or GitHub App token, stored as a repo secret.
- Branch protection on `qa` and `main` blocking direct pushes from anyone
  except that bot identity.
- `--ff-only` guarantees fast-forwards only, so `qa` and `main` never diverge
  and there's never a conflict to resolve.

## Publishing to conda-forge

Once an extension is an accepted feedstock, conda-forge's autotick bot
watches the source repo and automatically opens a version-bump PR when it
detects a new release — no maintainer action required to initiate it. The
remaining step is reviewing and clicking merge, or enabling `bot automerge`
on the feedstock so even that happens automatically once CI passes.

Though there may need to be another mechanism for packages under other
channels.
