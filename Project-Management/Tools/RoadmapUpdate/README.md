# Manual Testing Issue Creation

This directory contains a script and accompanying files to create and assign the manual testing issues for a Mantid release.

# Usage

- Create a Personal Access Token for GitHub if you do not already have one: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
- *Note*: You need to use a classic token, as fine-grained tokens are not currently supported in the Mantid Project organization.

- In `issue_template____.xlsx` update assignments for the upcoming release and make sure to add new starters to the assignee sheet. Make sure to raise issues for ISIS and Non-ISIS manual tests.
- For Ensemble Testing, look at `Ensemble Manual Testing.pptx` for advice allocating people to testing teams.

- Create and activate a conda environment for running the script:

```
cd here
conda env create -f manual-tests.yml
conda activate manual-tests
```

- Run the script with the appropriate arguments:

```
./create_issues.py milestone spreadsheet --dry-run
```

.e.g

```
./create_issues.py "Release 6.2" issue_template.xlsx --dry-run
```

- Check the output with the `--dry-run` flag and if it looks okay then rerun the same command but remove `--dry-run`.


Please note:

If you are using Windows it is recommended that you ``cd`` back into the ``SmokeTesting`` directory using the Command Prompt rather than any other CLI e.g. Git Bash. 
You will also need to prepend python to the command above and remove ./ from the ``create_issues.py`` part of the command

.e.g

```
python create_issues.py "Release 6.2" issue_template.xlsx --dry-run
```
