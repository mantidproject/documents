# SmokeTests
To create and update a script for Smoke Test issue creation

- In `issue_template.xlsx` update any links or text for each testing issue.

- Create a Personal Access Token for PyGithub: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token This token then is used in place of a password
- Create a local file in the RoadmapUpdate directory called `login.txt` simply with your Github 
Username and PAToken on seperate lines. e.g.
```
abc12345
ff34885a86faketoken24460a8555...
```
 **Do not commit login.txt to the remote repo!**

-`create_issues.py` creates an umbrella issue with 6 sub-issues describing each test.
-`create_issues_OS.py` does something similar, but creates separate issues for each OS to better track assignment.
- Firstly, comment out the two `repo.create()` lines in either create_issues script to test the script runs successsfully, assigning Manual Testing to recognised Mantid developers on GitHub:
```
# issue = repo.create_issue(title, my_body, gh_assignee, gh_milestone, gh_labels)
```

- Then uncomment to run and create the issues!
- Check your handiwork!
