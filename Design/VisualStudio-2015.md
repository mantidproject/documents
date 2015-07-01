Notes For Move To VS2015
========================

Will be released [20th July 2015](http://blogs.msdn.com/b/somasegar/archive/2015/06/29/save-the-date-visual-studio-2015-rtm-on-july-20th.aspx)

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

We no longer support x86 and Mac this way so they are not considered in this proposal.

The enforced separation of the libaries and includes was intended to ensure consistent versioning but actually makes some things harder as libraries like Qt need to know where their header files are. This is currently done with a `qt.conf` file that **assumes** a final layout when both repositories are cloned. In addition the layout of the repositories is non-standard and makes it more difficult to keep cross platform compatability with things like include paths.

The proposal for the Visual Studio 2015 dependencies is that the includes and libraries go into a single new repository named after the version of VS that they support. This will mean that the history of old versions does not start slowing down the repository. It is proposed that the layout of this new repository, named `3rdparty-msvc2015`, follow the standard unix style, i.e.

```
--
 - bin
 - include
 - lib
 - share
```

The `include` directory will only have subdirectories for those that have sub directories on Linux. This should make it easier to ensure that the headers can be included in the same way for both systems.

The runtime libraries (dlls) and executables will be put under `bin` and the archive libraries (.lib) will be under `lib`. This will allow developers to simply add the bin directory to the `PATH`. The debug libraries will need to be compiled in such away that their names don't clash with the release versions. 

New scripts will be generated to wrap the startup of Visual Studio & MantidPlot and set the appropriate paths so that these are not required to be present in global environment variables to avoid confliciting with them when running from a package.

### Python

The bundled python distribution is a slightly special case. Our current bundle is just a direct copy of an installed copy of one of the official releases (actually the debug copy is built by us). This means that the layout of its directories is fixed and not optimal for what we require. It is also still linked to `msvcr90.dll` and is causing other problems ([#12301](https://github.com/mantidproject/mantid/issues/12301)).

It is proposed that both release & debug builds are compiled to be dependent only on VS 2015 and the layout of the components follow the layout on RedHat (Debian seems to add complication with `dist-packages`: https://wiki.debian.org/Python#Deviations_from_upstream) using a `pythonX.X` directory under `lib` and `share`.

**To do**: I am not 100% sure that this will work when bundling with the installer. It needs investigation.

These [instructions](https://wiki.python.org/moin/VS2012) could be useful and should apply to VS2015 as the same things about lack of manifests applies.

Submodule
=========

Is it worth considering having the 3rdparty dependencies as a submodule of the main repository?



