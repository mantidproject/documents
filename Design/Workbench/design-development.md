# Development

## Coding Style

It is proposed we introduce a new Python style guide for Mantid. All new and refactored code should then follow this guide. The [IPython style guide][ipython-style] offers quite nice guidelines and it is suggested that we
follow these guidelines where applicable, including a template file for new code that could be used in the `class_maker` to generate new files.

## Static Analysis

We will no longer be able to rely on a compiler to catch simply errors - it is therefore imperative that we use static analysis to its fullest extent. While `flake8` is good it is not as thorough as `pylint` and given our
target is maximum reliability I propose that, at least on the gui components, we reinstate `pylint` for each pull request. Its configuration should be updated to remove some warnings that are too pedantic. As we are
starting from a clean slate with the workbench it should not be an issue to keep the warning level at 0. Special care should be taken by reviewers to assess when any warnings are suppressed to check if this is indeed valid.

## Documentation

User documentation for the workbench will be added to the standard `docs` build and organised into a navigible structure appropriately.

**Question: Where does developer documentation for this belong?**


<!-- Links -->
[ipython-style]: https://github.com/ipython/ipython/wiki/Dev:-Coding-style
