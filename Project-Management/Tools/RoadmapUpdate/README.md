- In `issue_template.xlsx` update assingment for the next release and make sure to add new starters to the assignee sheet.
- ISIS trialed creating testing issues earlier and assigning within teams, resulting in `issue_template_ISIS_11_2020.xlsx` and `issue_template_Non_ISIS_01_2021.xlsx`

- Create a Personal Access Token for PyGithub: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token This token then is used in place of a password
- Create a local file in the RoadmapUpdate directory called `login.txt` simply with your Github 
Username and PAToken on seperate lines. e.g.
```
abc12345
ff34885a86faketoken24460a8555...
```
 **Do not commit login.txt to the remote repo!**

- Firstly, comment out the penultimate line in `create_issues.py` to test the script runs successsfully, assigning Manual Testing to recognised Mantid developers on GitHub:
```
# issue = repo.create_issue(title, my_body, gh_assignee, gh_milestone, gh_labels)
```

- Then uncomment to run and create the issues!
- Check your handiwork!
