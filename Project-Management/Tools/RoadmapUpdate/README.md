# Manual Testing Issue Creation

This directory contains a script and accompanying files to create and assign the manual testing issues for a Mantid release.

# Usage

The Issues will be created automatically by running the script in this directory.  To do this, you must first setup a token and the needed environment.

- You need to clone this repo, ``mantidproject/documents``.  Note that the repo name may conflict with your user Documents directory if you attempt to clone directly into your home folder.

- Create and activate a conda environment for running the script:

```
cd ~/documents/Project-Management/Tools/RoadmapUpdate
mamba env create -f manual-tests.yml
mamba activate manual-tests
```

- Create a Personal Access Token for GitHub if you do not already have one: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
*Note*: You need to use a classic token, as fine-grained tokens are not currently supported in the Mantid Project organization.  The minimal scope needed is ``public_repo``.
You can test that your token works with

```
./create_issues.py milestone spreadsheet --check-token
```

- In `issue_template_ISIS.yml` and `issue_template_Non_ISIS.yml`, update assignments for the upcoming release and make sure to add new starters to the assignee sheet. Make sure to raise issues for ISIS and Non-ISIS manual tests.

- For Ensemble Testing, look at `Ensemble Manual Testing.pptx` for advice allocating people to testing teams.

- Run the script with the appropriate arguments:

```
./create_issues.py milestone spreadsheet --dry-run
```

.e.g

```
./create_issues.py "Release 6.14" issue_template_ISIS.yml --dry-run
```

- Check the output with the `--dry-run` flag and if it looks okay then rerun the same command but remove `--dry-run`.


Please note:

If you are using Windows, you will also need to prepend python to the command above and remove ./ from the ``create_issues.py`` part of the command

.e.g

```
python create_issues.py "Release 6.14" issue_template_ISIS.yml --dry-run
```
