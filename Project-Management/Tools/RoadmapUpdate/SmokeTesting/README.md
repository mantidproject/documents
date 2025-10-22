# Smoke Testing Issue Creation

This directory contains a script and accompanying files to create and assign the Smoke testing issues, by operating system for a Mantid release.

# Usage

The Issues will be created automatically by running the script in this directory.  To do this, you must first setup a token and the needed environment.

- You need to clone this repo, ``mantidproject/documents``.  Note that the repo name may conflict with your user Documents directory if you attempt to clone directly into your home folder.

- Create and activate a conda environment for running the script. Use the ``manual_tests.yml`` file in the parent directory ``RoadmapUpdate``.

```
cd ~/documents/Project-Management/Tools/RoadmapUpdate
mamba env create -f manual-tests.yml
mamba activate manual-tests
```
Remember to ``cd`` back into the ``SmokeTesting`` directory.

- Create a Personal Access Token for GitHub if you do not already have one: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token.
*Note*: You need to use a classic token, as fine-grained tokens are not currently supported in the Mantid Project organization.  The minimal scope needed is ``public_repo``.  
You can test that your token works with

```
./create_smoke_issues_OS.py milestone --check-token
```

- In `issue_template_os.yml` make sure to assign testers to each main OS issue and update the version number of Mantid at the top of the file.

- Run the script with the appropriate arguments:

```
./create_smoke_issues_OS.py milestone --dry-run
```

.e.g

```
./create_smoke_issues_OS.py "Release 6.14" --dry-run
```

- Check the output with the `--dry-run` flag and if it looks okay then rerun the same command but remove `--dry-run`.

Please note:

If you are using Windows it is recommended that you ``cd`` back into the ``SmokeTesting`` directory using the Command Prompt rather than any other CLI e.g. Git Bash. 
You will also need to prepend python to the command above and remove ./ from the ``create_smoke_issues_OS.py`` part of the command

.e.g

```
python create_smoke_issues_OS.py "Release 6.14" --dry-run
```
