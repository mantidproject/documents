# Pre-commit Framework

## Motivation 
Currently, developers commit and push their code to github, create a PR and wait for jenkins to tell them that their code is poorly formatted. 
If a developer wants their code to pass first time they must set up some elaborate method for testing all their code before it reaches the commit stage. 
In order to reduce pressure on the jenkins server, remove dependency on OS, and ensure that the vast majority of code that is committed is correctly formatted, and doesn't have any glaring issues that can be pointed out via static analysis, the development team should switch to utilising a pre-commit framework. 
Further, from the already stated benefits we can retire the static analysis individual and utilise the pre-commit framework on a single Jenkins job. 
 
## The implementation of pre-commit framework 
This section will discuss the implementation detail of how the pre-commit framework is intended to run, and some pre-requisites required for it to fit into our workflow.

#### Yapf 
- Integration of Yapf with pre-commit means moving forward with integrating Yapf in our developer workflows. 
- Jenkins job including yapf static analysis 
    - Recommend using pre-commit run on all commands. 
- Include yapf in the developer packages 
- Generally informing the team about the usage of Yapf and why it is necessary and good for overall productivity. 
- Yapf when ran in pre-commit should just fix the issues for developers instead of needing follow-up commands. 
 
#### Flake8 
- Informs a developer where an issue has arisen in code using the flake8 settings of the repo. 
- To run after yapf as yapf will fix some flake8 issues on it's own. 
 
#### Clang-format 
- Informs developers where an issue has arisen in code and then fixes it based on the settings of the repo ensuring that for example it adheres to our repo specific settings including future changes such as 120 characters per line. 
- We will be maintaining this hook as we can then control the clang-format version, this will be in a separate repo. 
 
#### XML and YAML checking 
- Should catch yaml and xml violations in commits before they become a problem, on the build servers. 
 
#### Cppcheck 
- Run Cppcheck with errors displayed on the command line and output 
    - Cppcheck will only be present if the suppression of warnings is possible to implement simply, if not it will need to be added at a later date. 
    - We will be maintaining this hook as we can then control the cppcheck version 
 
####Pre-commit run order 
- Check XML/YAML 
- Yapf - In place fixes 
- Clang-format - In place fixes 
- Flake8 
- Cppcheck (Provisionally) 
 
An initial implementation has been made here: https://github.com/mantidproject/mantid/pull/30740 
 
##Installation instructions 
 
We will be installing pre-commit and setting it up with the git hooks so that it runs before each time you commit. 
 
#### CentOS/RHEL Installation 
 
To install snap for CentOS and RHEL to support the use of pre-commit, without using pip. Navigate to your repo and run: 
```shell 
pip install pre-commit 
pre-commit install 
``` 
 
#### Ubuntu 18.04+ Installation 
Navigate to your Repo and run: 
```shell 
sudo snap install pre-commit --classic 
pre-commit install 
``` 
 
### MacOS Installation 
We install pre-commit via homebrew on MacOS. Navigate to your repo and run: 
```shell 
sudo brew install pre-commit 
pre-commit install 
``` 
 
### Windows Installation 
On Windows this is installed and initialised for them via CMake, just pull the latest changes from master, re-run CMake and it will sort it for you. 
 
## Migration steps 
- Create a separate repo called mantidproject/pre-commit-hooks e.g. https://github.com/pocc/pre-commit-hooks 
    - Add clang-format 
    - Add cppcheck (provisionally, if too complex will leave to a later date) 
- Merge pre-commit framework PR (https://github.com/mantidproject/mantid/pull/30740) 
- Create pre-commit CI Job that will replace: 
    - Clang-format 
    - flake8 
    - cppcheck (If implemented at earlier step) 
 
### Final Migration Steps (TBD) 
All final tasks should be completed in one day on to minimise potential disruption to developers in the team 
- Update and apply clang-format and Yapf versions to the whole codebase, using the pre-commit hooks 
- Replace Jenkins static analysis jobs with the already made pre-commit CI job 
- Inform developers

## Potential future feature plans
Future development will be easy and not require significant updates to CMake for Windows or require custom installation, updating the .yaml config will allow future changes to not only the local developer machines but on Jenkins seamlessly.

- Any newly added feature will be run on the whole repo at the same time to avoid random things being added to new PRs and ideally should be enforced by Jenkins, but many suggested features won't require jenkins enforcement. 
- Support more things in pre-commit slowly introducing helpful features 
    - Cppcheck support (Requires more investigation, and likely support in our own hooks to control version and enforce config usage) 
    - Enforce branch security with a second layer (Aimed at more senior developers with access to push to master/main and release-next, maybe ornl-next?) 
    - Remove trailing whitespace (Enforce support for Markdown) 
    - Merge conflict support 
    - Find Python debug commands such as remote debug statements and debugging print statements. 
    - Enforce test file naming conventions 
    - Check for potential conflicts in case-insensitive filesystems 
    - Check JSON syntax 
    - MyPy static analysis support, had great success in mantid imaging. 
    - Reorder python imports 
    - dead - A dead python code detector 
    - markdown lint support and enforcement 
    - Dockerfile linter 
    - License insertion and detection, automatically updating licenses in files that have been edited. 
    - Cmake-format
    - Doxygen
