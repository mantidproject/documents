Pre-Commit Implementation detail and developer install

**The implementation of pre-commit framework version 1 will have multiple things**

- Create individual hooks for each of the main static analysis tools using the static analysis docker container.
- Integration of Yapf with pre-commit means moving forward with integrating yapf in our developer workflows.
    - Jenkins job including yapf static analysis
      - Update jenkins static analysis docker container to include yapf
      - Advise developers to run a simple command in their repo to fix any jenkins issues e.g. ```python -m yapf -i -p -r .```
    - Include yapf in the developer packages
    - Generally informing the team about the usage of yapf and why it is nessercary and good for overally productivity.
    - Yapf when ran in pre-commit should just fix the issues for developers instead of needing follow up commands. 
   
- Support for Flake8
    - Informs a developer where an issue has arisen in code using the flake8 settings of the repo.
    - To run after yapf as yapf will fix some flake8 issues on it's own.

- Support for Clang-format
    - Informs developers where an issue has arisen in code and then fixes it based on the settings of the repo ensuring that for example it adheres to our repo specific settings including future changes such as 120 characters per line.
    - We will be supporting this hook as we can then control the clang-format version, this will be in a separate repo.

- Basic support for checking committed yaml and xml files.
    - Should catch yaml and xml violations in commits before they become a problem, on the build servers.

- Order for pre-commit
    - Check XML/YAML
    - Yapf - In place fixes
    - Clang-format - In place fixes
    - Flake8

**Potential future feature plans**

- Any newly added feature will be ran on the whole repo at the same time to avoid random things being added to new PRs and ideally should be enforced by Jenkins, but many suggested features won't require jenkins enforcement.

- Support more things in pre-commit slowly introducing helpful features
    - Cppcheck support (Requires more investigation, and likely support in our own hooks to control version and enforce config usage)
    - Enforce branch security with a second layer (Aimed at more senior developers with access to push to master/main and release-next, maybe ornl-next?)
    - Remove trailing whitespace (Enforce support for markdown)
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

##Installation instructions

We will be installing pre-commit and setting it up with the git hooks so that it runs before each time you commit.

###Linux Installation

For Ubuntu 16.04+ we do not need to install snap. CentOS/RHEL install Snap and enable classic snap support, to allow Pre-commit to be installed without pre-commit.

#### CentOS/RHEL Installation

To install snap for CentOS and RHEL to support the use of pre-commit, without using pip. Navigate to your repo and run:
```shell
sudo yum install epel-release
sudo yum install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
pre-commit install
```

#### Ubuntu 16.04+ Installation
Navigate to your Repo and run:
```shell
sudo snap install pre-commit --classic
pre-commit install
```

###MacOS Installation
We install pre-commit via homebrew on MacOS. Navigate to your repo and run:
```shell
sudo brew install pre-commit
pre-commit install
```

###Windows Installation
On Windows this is installed and initialised for them via CMake, just pull the latest changes from master, re-run CMake and it will sort it for you.
