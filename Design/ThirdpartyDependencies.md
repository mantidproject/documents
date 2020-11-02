# Third Party Dependencies

This document aims to describe the current issues surrounding the use of 
third-party libraries within the mantid codebase,
along with proposals for solutions to these problems.

## Motivation

Mantid uses a wide variety of third-party libraries
and takes different approaches for managing them on each operating system - 
this vastly increases the management overhead for any library used. 
Furthermore each OS uses a different version of given package
making it impossible to define a single version across the whole project.

The motivation behind this work is to vastly reduce the dependency management
overhead across the project.

## Current Situation

The following sections describe the current state of play for 
3rd-party library management for each of our supported operating systems.

### Linux (RHEL 7 & Ubuntu)

Linux-based platforms use OS-provided system packages from distro repositories
or custom builds of libraries where distro-provided versions are
too old.
See 
[copr for RPM](https://copr.fedorainfracloud.org/coprs/mantid/mantid/)
and 
[launchpad PPA for Ubuntu](https://launchpad.net/~mantid/+archive/ubuntu/mantid).
[Developer packages](https://github.com/mantidproject/mantid/tree/master/buildconfig/dev-packages)
are provided for developers to easily install the required dependencies.

Upgrading libraries is possible by placing newer versions in the above locations.
For some libraries, such as HDF5 or sip, 
this is not advised due to conflicts with other applications requiring
different versions.
A real example is with the rebuilt `sip` package for RHEL7,
which conflicts with other packages such as `Octave` and causes users troubles
when installing these packages alongside Mantid.

The package provided for users depends on the system libraries leaving the
mantid package to just ship the mantid libraries.

In addition, 
for RHEL 7 (and its variants CentOS, Scientfic Linux) a
[Software Collection](https://www.softwarecollections.org/en/) is used to provide
a gcc-7 allowing C++17-enabled builds.

Pros:
* Easier developer setup.
* Smaller user packages. The system libraries are shared for all packages resulting
  in a much smaller package to install.
* (Mostly) managed for us.
* Simple, well-known commands to install packages (apt/yum)


Cons:
* Dependencies not versioned with the main code. Hard to track versions used.
* Versions become outdated very quickly. Facilities tend to use
  older distributions that do not have up to date versions of packages.
* Upgrading/rebuilding package versions can cause conflicts with other packages
  not related to mantid and even old mantid versions.
* New dependencies have to be installed manually on developers and builders machines.


### Windows

Windows uses a collection of custom-built libraries managed
by a homegrown set of [scripts](https://github.com/mantidproject/thirdparty-msvc2015).
The binaries are stored using the [git lfs](https://git-lfs.github.com/)
extension for managing large binaries with git.
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
* Dependencies not versioned with the main code. Hard to track versions used.
* Homegrown set of scripts are very clunky.
* Maintenance of build scripts adds overhead.
* Complete bundling of dependencies gives a much larger user installer package.
* ABI changes require a complete rebuild
* Initial download (~5GB) takes quite some time


### MacOS

MacOS uses the [Homebrew](https://brew.sh/) package manager for C++ dependencies.
A custom [tap](https://github.com/mantidproject/homebrew-mantid) provides a
[mantid-developer](https://github.com/mantidproject/homebrew-mantid/blob/master/mantid-developer.rb)
meta-formula to install all of the dependencies in one shot. 
Python dependencies are installed with `pip` and a 
[requirements file](https://github.com/mantidproject/homebrew-mantid/blob/master/requirements.txt).
Homebrew either downloads a prebuilt binary or builds it locally from the formula.
A developer formula is provided to easily install the required dependencies.

The package provided for users contains all required dependencies
much like Windows.

Pros:
* Formula for dependencies (mostly) maintained for us.
* Simple commands to install packages

Cons:
* Dependencies not versioned with the main code. Hard to track versions used.
* No way to set deployment target. We have to build on the earliest OS we intend
  to support causing issues with hardware availability.
* New dependencies have to be installed by hand on developers
  and builders machines.
* Versions can be pinned but Homebrew really likes to have everything at HEAD.
  This has recently caused issues when Python-based formula, like PyQt, were migrated
  to Python 3.9 but many other Python dependencies such as matplotlib were
  not yet available for 3.9. Homebrew has to be pinned to we receive no more updates
  in this case.

## General Concerns

While each approach has the drawbacks described above
there are also general issues with the current approach:

1. It is not possible to define a version of a given
   library as the version used across the whole project.
   This can cause confusion for developers
   where their platform might have a newer api
   yet their code does not work on other platforms.
   This slows down development and ties us to the oldest
   LTS for years.
2. Using a new library takes a lot of overhead and
   in some cases is basically impossible
3. Three different methods requires much additional overhead
   in understanding how things are managed.
4. Pushing new dependencies to build servers requires
   co-ordination and potential downtime.

## Requirements

The following is a list of requirements that must be met by any solution:

1. Supports C++ & Python packages
2. allow mantid to select any version of a given dependency
3. version definitions alongside the code in the repository
4. use the same version of a dependency across all platforms
5. provide users a single "package" to install self-contained Workbench
   application along with all required libraries. 
6. must be able to install versions side-by-side
   including nightly and unstable versions.

## Use Cases

1. Ship a self-contained desktop application
   with the latest versions of required libraries,
   also allowing users to install their own Python packages
2. Provide a `mantid` framework library for users to use in
   their own projects, e.g mslice, PyRS + other SNS GUIs

## Solutions

Here we describe possible solutions to the problems outlined above.
The solutions considered in detail are:

* [Conan](#Conan)
* [Conda](#Conda)

Other solutions not considered:

* Flatpak/Snap:
  * Would only work for Linux and still be a large effort.
* Singularity/Docker:
  * Unsure about desktop applications & would not work for macOS.
  * Docker on Windows requires the Hyper-V role, so users would
    have to get admin access and have a processor capable of 
    exposing the required instructions - so it's not universally compatible
* WSL:
  * Needs to be installed separately. Barrier to high for non-technical users.

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

Conan would satisfy the requirements 2-4 through the
[conanfile.txt](https://docs.conan.io/en/latest/reference/conanfile_txt.html)
or [conanfile.py](https://docs.conan.io/en/latest/reference/conanfile.html).

For user packaging purposes the dependencies would be bundled in with each of
the user packages on all of the platforms, much like the current approach
for Windows/macOS.
User packages would still be created in the appropriate format for that
platform, e.g. rpm for RHEL/CentOS etc.
Each package would ship with its own dependencies then the final requirement of
side-by-side installs will be taken care of automatically.
QtCreator does this and is able to ship a standalone version with the latest
Qt version regardless of the system version of Qt.

Another option to consider would be static linking but this may well
be worth considering separately after the dependency management issue
is settled.

On Linux this would also have the advantage of supporting additional Linux
distributions or newer versions of existing distributions almost trivially.

#### CMake

Conan has built in support for
[CMake](https://docs.conan.io/en/latest/integrations/cmake.html)
along with a [CMake Wrapper](https://github.com/conan-io/cmake-conan/)
to enable configuring dependencies completely in CMake.

Developers would continue to work as they do now with their favourite IDEs
and tools but would need to install Conan first.
Release packages are [provided](https://github.com/conan-io/conan)
that have no other dependencies and are easy to install.

#### Python Packages

Conan was designed as a framework to package C/C++ dependencies.
While it is written in Python itself it does not possess the capability
to manage Python dependencies.
In our current solution on Windows/macOS we already ship a bundled Python
distribution to users and the proposal is to do the same for linux
for the workbench application bundle.

Bundling of Python is managed differently for Windows/macOS:

* Windows: The [third party](https://github.com/mantidproject/thirdparty-msvc2015/)
  repository contains a Python version installed by hand along with 
  [scripts](https://github.com/mantidproject/thirdparty-msvc2015/blob/master/build-scripts/fixup-python3.bat)
  to fix up links so the bundle is relocatable.
  CMake scripts copy the bundle to the Mantid user package.
* macOS: Homebrew is used to install Python to a dev machine as part
  of the developer package. A [ruby script](https://github.com/mantidproject/mantid/blob/master/installers/MacInstaller/make_package.rb)
  copies the bundle to the user package.

Here it is proposed that we create our own Python Conan package
that can be used like any other dependency for the desktop
application bundle.
This has been [prototyped](https://github.com/martyngigg/conan-python3)
and seems to work well.
It would require some patching of `site.py` or using `sitecustomize.py`
to ensure packaging doesn't interfere with system versions
but this is something supported by Python
and done by other systems like `Conda`.
Python requirements could be easily supported by a requirements file
or some newer system like
[pipenv](https://packaging.python.org/key_projects/#pipenv) to properly
define a frozen set of dependencies.
Some packages such as `PyQt` do not provide the headers and link
libraries required for the C++ build.
The easiest solution would be a Conan package for `PyQt` much like macOS
Homebrew does. 

The availability of `mantid` to other Python libraries would be the cause
of the most concern if we adopted the Conan approach as it is
about creating a self-contained package.


### Conda

*"A conda package is a binary tarball containing
system-level libraries,
Python modules,
executable programs,
or other components"*.

[Conda](https://docs.conda.io/en/latest/)
is another cross-platform package manager but with support for a
variety of languages including Python and C++.
Alongside `pip` many popular Python packages support distribution through Conda.
In fact `mantid` already has [Conda packages](https://anaconda.org/mantid/repo)
for workbench and the framework for Linux.
Mac packages are currently effectively abandoned.

[Anaconda](https://repo.continuum.io/pkgs/) hosts many prebuilt packages for
various combinations of compilers and operating systems.
[Conda build](https://conda.io/projects/conda-build/en/latest/resources/commands/conda-build.html)
is provided to enable building custom packages.
Compilers are somewhat limited., getting latest versions of compilers on all platforms is
problematic/hacky at best.

The [meta.yaml](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#requirements-section)
file provides a central place to define dependencies and would satisfy requirements 2-4.
The requirements file allows builds tools such as CMake to be used.

It is unclear how the build process would fit into current tools such as IDEs.
The current CLI workflow is documented [here](https://github.com/mantidproject/conda-recipes/blob/master/Developer.md).

Conda would possibly a better solution for providing just the `mantid` framework
as a library for other users to import and not considering this as a solution
for providing the full desktop application bundle. We also already have a
working conda build of the framework so this is low overhead. This needs
proper support though.

## Summary + Questions

After consideration I would suggest be that we adopt both options for supporting
the two use cases presented. Both cases have different needs so there is no
reason to expect one system to support both.

Questions: 

1. Do we need to still support a build against system libraries on Linux?

   * Would SNS need an RPM framework build for their GUIs linked to system Python?

2. Is it sensible to consider maintaining Conan packages as suggested?

  * Where would we store binary artifacts? Or just store recipes?
  * Bintray has been considered but its price could be prohibitive.
  * What would be the rough time to build locally per machine as an estimate?
    * If it's an hour per developer per say 6-12 months, configuring remote
      artefacts / storage / retention vs building locally would become a factor


3. Other things not considered here?
