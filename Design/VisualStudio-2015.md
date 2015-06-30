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

Once thing to consider strongly is that we will require debug builds of all of these libraries, which NuGet does not seem to provide.

CMake Projects
--------------
For any 3rd party project that uses CMake we should write a cache file and store it in a the repo so that we have a reference to how it was built

Restructuring Dependency Layout
-------------------------------

The current 3rd party repositories are separated into

* [3rdpartyincludes](https://github.com/mantidproject/3rdpartyincludes)
* [3rdpartylibs-mac](https://github.com/mantidproject/3rdpartylibs-mac)
* [3rdpartylibs-win32](https://github.com/mantidproject/3rdpartylibs-win32)
* [3rdpartylibs-win64](https://github.com/mantidproject/3rdpartylibs-win64)

The enforced separation of the libaries and includes was intended to ensure consistent versioning but actually makes some things harder as libraries like Qt need to know where their header files are. This is currently done with a `qt.conf` file that **assumes** a final layout when both repositories are cloned. In addition the layout of the repositories is non-standard and makes it more difficult to keep cross platform compatability with things like include paths.

The proposal for the Visual Studio 2015 dependencies is that the includes and libraries go into a single new repository named after the version of VS that they support. This will mean that the history of old versions does not start slowing down the repository. It is proposed that the layout of this new repository follow the standard unix style, i.e.

```
--
 - bin
 - include
 - lib
 - share
```

The `include` directory will only have subdirectories for those that have sub directories on Linux. This should make it easier to ensure that the headers can be included in the same way for both systems

Submodule
=========

Is it worth considering having the 3rdparty dependencies as a submodule of the main repository?



