# Smoke Testing Issue Creation

This directory contains a script and accompanying files to create and assign the Smoke testing issues, by operating system for a Mantid release.

# Usage

- Create a Personal Access Token for GitHub if you do not already have one: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

- In `issue_template.xlsx` make sure to assign testers to each main OS issue.

- Create and activate a conda environment for running the script. Use the ``.yml`` file in the parent directory ``RoadmapUpdate``.

```
cd here/..
conda env create -f manual-tests.yml
conda activate manual-tests
```

- Remember to ``cd`` back into the ``SmokeTesting`` directory. Run the script with the appropriate arguments:

```
./create_smoke_issues_OS.py milestone spreadsheet --dry-run
```

.e.g

```
./create_smoke_issues_OS.py "Release 6.2" issue_template.xlsx --dry-run
```

- Check the output with the `--dry-run` flag and if it looks okay then rerun the same command but remove `--dry-run`.
