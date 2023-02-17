# Merging Conda Recipes To Main Repository

This document describes the planned changes to integrate the
[Conda recipes](https://github.com/mantidproject/conda-recipes) for Mantid
into the main [mantid](https://github.com/mantidproject/mantid) repository.
In particular there needs to be agreement on how the versioning information
will be handled as we will want to leverage the Conda-provided
tools such as
[Git Jinja variables](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#templating-with-jinja)
as much as possible.

## Current Status

The Conda recipes for mantid are stored in a [repository](https://github.com/mantidproject/conda-recipes)
separate to the main source code. This is largely historical from the time when
Conda was not a fully supported distribution platform.
There had also been some thought that mantid would eventually make its way to
[conda-forge](https://conda-forge.org/) and we would benefit from keeping the
recipes separate to mimic it.

In reality the split currently causes more problems than it solves as:

- building the conda packages with the correct version number and git sha
  requires various machinations around cloning the repository and in-place modifying
  the [recipes](https://github.com/mantidproject/mantid/blob/main/buildconfig/Jenkins/Conda/update-conda-recipes.sh)
- when a successful nightly build is published the version number has to be actively updated again
- changes to the main code and the conda recipes are compplicated to synchronise
  and test for developers raising the likelihood of errors.

## Proposal

We propose the conda recipes be integrated with the main codebase and the existing conda-recipes
repository be archived. A ``conda/recipes`` folder will be introduced into the root
of the ``mantid`` repository with the content from ``conda-recipes/recipes`` initially copied
verbatim, including the folder structure.

Once copied, the head of the recipes meta.yml needs to be modified to work inside
the repository. The minimum change required is to change the `source` field as
so:

```yml
source:
  path: ../../
```

We could leave the version number handling as it is and simply keep the
[scripts](https://github.com/mantidproject/mantid/blob/main/buildconfig/Jenkins/Conda/update-conda-recipes.sh)
modifying the `meta.yaml` in place to update the version number and then building
the packages. This is a little messy though and not transparent from looking
at the recipes. We propose an adjustment to how/where we defining our versioning
information.

### Version Numbers

Mantid currently defines its version information in
[VersionNumber.cmake](https://github.com/mantidproject/mantid/blob/a290316450b429942b561694c4864abf6cfd670e/buildconfig/CMake/VersionNumber.cmake)
and [PatchVersionNumber.cmake.in](https://github.com/mantidproject/mantid/blob/a290316450b429942b561694c4864abf6cfd670e/buildconfig/CMake/PatchVersionNumber.cmake.in)
and is computed fully by CMake but in the case of a conda build this information is lifted from
environment in slightly obtuse manner.

We propose a simplification of the versioning system such that it be based on git tags
and the [versioningit](https://versioningit.readthedocs.io/en/stable/how.html) package.
`versioningit` uses the PEP-518 `pyproject.toml` file to store configuration
information relating to how the version number should be computed. We will introduce
the following files:

`pyproject.toml`:

```toml
[tool.versioningit.vcs]
method = "git"
default-tag = "0.0.0"

[tool.versioningit.next-version]
method = "minor"

[tool.versioningit.format]
distance = "{version}.dev{distance}"
dirty = "{version}+d{build_date:%Y%m%d}"
distance-dirty = "{version}.dev{distance}+d{build_date:%Y%m%d%H%M}"
```

`setup.py`:

```python
from setuptools import setup
import versioningit

# Minimal setuptools setup to allow calling `load_setup_py_data`
# from Conda meta.yaml
setup(
  version = versioningit.get_version()
)
```

The `meta.yaml` head information will be altered to:

```yaml
{% set data = load_setup_py_data() %}

package:
  name: mantid
  version: {{ data.get('version', '0.0.0') }}

build:
  number: 0
```

to use `versioningit` to compute the version information centrally based on
the git tags that are present.

The complicated version calculations in CMake can then be simplified  by
calling `versioningit` in
[VersionNumber.cmake](https://github.com/mantidproject/mantid/blob/a290316450b429942b561694c4864abf6cfd670e/buildconfig/CMake/VersionNumber.cmake),
removing [PatchVersionNumber.cmake.in](https://github.com/mantidproject/mantid/blob/a290316450b429942b561694c4864abf6cfd670e/buildconfig/CMake/PatchVersionNumber.cmake.in),
and removing the whole `if(GIT_FOUND)` block in [CommonSetup.cmake](https://github.com/mantidproject/mantid/blob/a290316450b429942b561694c4864abf6cfd670e/buildconfig/CMake/CommonSetup.cmake#L147).

Deploying a new version, whether nightly or a full release becomes the same process.
Tag the commit with the appropriate version number and let `versiongit` do the rest.
This will also remove the clunky step during a release where the current
`VersionNumber.cmake` file is merged from `release-next` to `main` and then
the patch number is commented out again.

For a nightly build the scripts will be simplified to push the new tag along with the
latest artefacts. A GitHub action will be introduced to prune the artefacts
older than a set number of releases.
