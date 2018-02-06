---
title: Do you even Git?
...

# Current Problems

## Current Git workflow

1. Branch
2. Write come code
3. Commit
4. Goto 2 until done
5. Commit CI fixes
6. Goto 6 until done
7. Review
8. Commit review changes
9. Goto 7 until done
10. Merge feature branch to master

Optional: merge `master` into your branch several
times along the way

## Why is this wrong?

You get:
- Non-atomic commits
- Commits that really shouldn't exist

Which lead to:
- Difficulty reading history
- Tracking changes and introduction of bugs becomes harder

(#17174)

# How to fix it

## Stop merging master into your branch

Instead of doing this: `git merge master`

Do this: `git rebase master`

Rebasing reapplies commits from your feature branch
onto the head of `master`.

Shouldn't be used on public/collaborative branches
(sort of).

## Start interactively rebasing

Instead of committing every change in a new commit.

Do this: `git rebase -i` (`git rebase -i master`)

Interactive rebase allows review changes, CI fixes, etc
to be rolled into the commit that introduced them.

# Demo
