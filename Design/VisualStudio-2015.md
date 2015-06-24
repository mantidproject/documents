Notes For Move To VS2015
========================

* Requires minimum of CMake v3.1
* We want the newest HDF5 to gain extra C++ features

Dependencies
------------

[NuGet](https://www.nuget.org/) provides a package manager for Windows binaries, a little like existing package managers for Linux distros.

The following table lists our current third party packages and whether or not they are available via existing NuGet channels.

| Package            | Available  | Version                 | Visual Studio Version |
|--------------------|:----------:|:-----------------------:|:---------------------:|
| nexus              |            |                         |                       |
| poco               | yes        | 1.4.6-p4 (pre-release)  | unknown               |
| qt                 |            |                         |                       |
| open cascade       |            |                         |                       |
| boost              | yes        | 1.58                    |  2015 RC              |
| cblas              |            |                         |                       |
| gsl                |            |                         |                       |
| hdf5               |            |                         |                       |
| hdf4               |            |                         |                       |
| jsoncpp            |            |                         |                       |
| openssl (libeay32) |            |                         |                       |
| szip               |            |                         |                       |
| zlib               |            |                         |                       |
| muparser           |            |                         |                       |
| mxml               |            |                         |                       |
| qscintilla         |            |                         |                       |
| qwt                |            |                         |                       |
| qwtplot3d          |            |                         |                       |

Once thing to consider strongly is that we will require debug builds of all of these libraries
