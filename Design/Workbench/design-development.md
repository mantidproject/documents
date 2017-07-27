# Development

## Coding Style

It is proposed we introduce a new Python style guide for Mantid. All new and refactored code should then follow this guide. The [IPython style guide][ipython-style] offers quite nice guidelines and it is suggested that we
follow these guidelines where applicable, including a template file for new code that could be used in the `class_maker` to generate new files.

## Static Analysis

We will no longer be able to rely on a compiler to catch simply errors - it is therefore imperative that we use static analysis to its fullest extent. `flake8` will be run on the pull request jobs
and `pylint` run on `master`. The tolerance levels & configuration for `pylint` should be reexamined and the job place on the critical Jenkins tab.

## Documentation

User documentation for the workbench will be added to the standard `docs` build and organised into a navigible structure appropriately.

**Question: Where does developer documentation for this belong?**


<!-- Links -->
[ipython-style]: https://github.com/ipython/ipython/wiki/Dev:-Coding-style
