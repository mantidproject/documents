- In `issue_template.xlsx` update assingment for the next release and make sure to add new starters to the assignee sheet.

- Create a local file in the RoadmapUpdate directory called `login.txt` simply with your Github
Username and Password on seperate lines. e.g.
```
abc12345
password
```

- Firstly, test the script runs successsfully, assigning Unscripted Testing to recognised Mantid developers on GitHub, by commenting out the penultimate line in `create_issues.py`:
```
# issue = repo.create_issue(title, my_body, gh_assignee, gh_milestone, gh_labels)
```

- Then uncomment to run and create the issues!
- Check your handiwork!



