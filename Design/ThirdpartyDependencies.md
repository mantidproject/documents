# Third Party Dependencies

This document aims to describe
the current issues surrounding the use of third-party libraries
within the mantid codebase,
along with proposals for solutions to the current problems.

## Motivation

The ESS will be using features from HDF5 such as variable-length strings,
[single writer multiple reader](https://support.hdfgroup.org/HDF5/docNewFeatures/NewFeaturesSwmrDocs.html)
that are not yet available on some of our platforms. These features are available in HDF5 1.10
but RHEL 7 (and variants) and Ubuntu 16.04 ony have HDF5 1.8 available.

Upgrading a library such as HDF5 that is used by many other system packages
is not a good idea as it could lead to a mess of package conflicts.
Furthermore, while this is an issue with a single package it points to
a more systemic issue with how we handle our dependencies across the project.

## Current Situation

Mantid uses several third-party libraries
in order to avoid reinventing the wheel,
where an approved solution already exists in the wild.
The dependencies are managed in very different ways
on the three platforms that are supported.

Please note that during all discussions below ParaView is to be treated,
effectively, as our source code as we build and ship our own version
on all platforms.

### Linux

Linux-based platforms use OS-provided system packages from distro repositories
or custom builds of libraries where distro versions are
too old. See [copr for RPM](https://copr.fedorainfracloud.org/coprs/mantid/mantid/)
and [launchpad PPA for Ubuntu](https://launchpad.net/~mantid/+archive/ubuntu/mantid).
[Developer packages](https://github.com/mantidproject/mantid/tree/master/buildconfig/dev-packages)
are provided for developers to easily install the required dependencies.

The package provided for users depends on the system libraries leaving the
mantid package to just ship the mantid libraries.

In addition, for RHEL 7 (and its variants CentOS, Scientfic Linux) a
[Software Collection](https://www.softwarecollections.org/en/) is used to provide
a gcc-7 allowing C++14-enabled builds.

Pros:
* Easy developer setup.
* Smaller user packages. The system libraries are shared for all packages resulting
  in a much smaller package to install.
* (Mostly) managed for us.
* Simply commands to install packages


Cons:
* Versions become outdated very quickly. Facilities tend to use
  older distributions that do not have up to date versions of packages.
* Upgrading/rebuilding package versions can cause conflicts with other packages
  not related to mantid and even old mantid versions.
* Python 3 on RHEL 7 will require a fair amount of effort.
* New dependencies have to be installed by hand on developers and builders machines.

 
### Windows

Windows uses a collection of custom-built libraries managed
by a homegrown set of [scripts](https://github.com/mantidproject/thirdparty-msvc2015).
The binaries are stored using the [git lfs](https://git-lfs.github.com/) extension for
managing large binaries with git.
For developers, all of the libraries are pulled down by
the [cmake configure step](https://github.com/mantidproject/mantid/blob/master/buildconfig/CMake/Bootstrap.cmake#L13)
thereby minimizing the effort required for developers to get up and running.
It also includes a bundled version of Python as none is available by default
on Windows.

The package provided to users contains all required dependencies and is a
self-contained bundle.

Pros:
* Easy developer setup.
* Complete freedom to choose package versions and apply patches etc.
* New dependencies are retrieved automatically for developers and build servers
* Self-contained user package.

Cons:
* Homegrown set of scripts are clunky.
* Maintenance of build scripts adds overhead
* Complete bundling of dependencies gives a much larger user installer package.


### MacOS

MacOS uses the [Homebrew](https://brew.sh/) package manager along with a custom
set of [formula](https://github.com/mantidproject/homebrew-mantid) for obselete
dependencies. Homebrew downloads the formulae and builds the libraries locally.
There is no single developer formula, instead there is a set of build instructions
for a new developer to follow to get there system setup.

The package provided for users contains all required dependencies
with the exception of Python. The system python interpreter
along with libraries such as `numpy`, `scipy` are presumed
to be present on the system. 

Pros:
* Build formula (mostly) maintained for us.
* Simply commands to install packages

Cons:
* No way to set deployment target therefore we have to build on the earliest OS we intend
  to support causing issues with hardware availability.
* Mix up between Homebrew Python and system Python can get messy.
* Lack of bundling Python for users can lead to verion mixups and application crashes
  for users.
* New dependencies have to be installed by hand on developers and builders machines.

## General Concerns

While each approach has the drawbacks described above
there are also general issues with the current approach:

1. It is not possible to define a version of a given
   library as the version used across the whole project.
   This can cause confusion for developers
   where their platform might have a newer api yet
   their code does not work on other platforms. 
2. Using new third party libraries is quite time consuming.
3. Three different methods requires much additional overhead
   in understanding how things are managed.

## Requirements

The following is a list of requirements that must be met any possible solution:

1. allow mantid to select a given version of a given dependency
2. version definition for a given library is in a central place
3. use the same version of a given dependency across all platforms
4. provide users a single "package" to install mantid
5. must be able to install versions side-by-side
   including nightly and unstable versions.

The following is a list of non-essential but desirable features that any solution could have:

1. common system on all platforms

## Solutions

Here we describe possible solutions to the problems outlined above. 
The solutions considered are:

* [Conan](#Conan)
* Conda
* Flatpak/Snap
* Singularity
* Docker

### Conan

[Conan](https://docs.conan.io/en/latest/introduction.html)
is a decentralized package manager for C/C++.
It aims to be cross-platform and build system agnostic.
The servers store packages that can be downloaded directly
if the required config matches the prebuilt versions.
Otherwise conan will build packages locally if the requested binaries
are not available to match the required configuration.

Conan allows for the conan server to be hosted "privately" to facilitate
sharing binaries across developers on the same project and avoids the overhead
of each developer rebuilding the dependency set.

Conan would satisfy the first 3 requirements through the
[conanfile.txt](https://docs.conan.io/en/latest/reference/conanfile_txt.html).

For user packaging purposes the dependencies would be bundled in with each of
the user packages on all of the platforms, much like is done on Windows. As long
as the `RPATH` settings are correct this should not be a problem on Linux.
