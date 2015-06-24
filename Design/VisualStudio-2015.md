Notes For Move To VS2015
========================

* Requires minimum of CMake v3.1
* We want the newest HDF5 to gain extra C++ features

Dependencies
------------

[NuGet](https://www.nuget.org/) provides a package manager for Windows binaries, a little like existing package managers for Linux distros.

The following table lists our current third party packages and whether or not they are available via existing NuGet channels. It only lists those available with a build against VS2015 RC as it is assumed that these will be built for the full release too.

| Package  | Available  | Version                 | 
|----------|:----------:|:-----------------------:|
| boost    | yes        | 1.58                    |  
| poco     | yes        | 1.4.6-p4 (pre-release)  |
