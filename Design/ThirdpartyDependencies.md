# Third Party Dependencies

This document aims to describe
the current issues surrounding the use of third-party libraries
within the mantid codebase,
along with proposals for solutions to the current problems.

# Overview of the Problem

Mantid uses several third-party libraries
in order to avoid reinventing the wheel,
where an approved solution already exists in the wild.
The dependencies are managed in very different ways
on the three platforms that are supported.

Please note that during all discussions below ParaView is to be treated,
effectively, as our source code as we build and ship our own version
on all platforms.

## Linux

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
 
## Windows

Windows uses a collection of custom-built libraries managed
by a homegrown set of [scripts](https://github.com/mantidproject/thirdparty-msvc2015).
For developers, all of the libraries are pulled down by
the [cmake configure step](https://github.com/mantidproject/mantid/blob/master/buildconfig/CMake/Bootstrap.cmake#L13)
thereby minimizing the effort required for developers to get up and running.
It also includes a bundled version of Python as none is available by default
on Windows.

The package provided to users contains all required dependencies and is a
self-contained bundle.
