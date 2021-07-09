# Future packaging with conda

## Current methodology
At present we have bespoke methodologies for packaging on each different OS we support (Windows, MacOSX, Ubuntu, and CentOS/RHEL7).

- On Windows, we create a packaged installer containing our dependencies and our compiled program as a .exe. We only link to some parts of System32 that provide Windows functionality required for Mantid, and the OpenGL shim to handle the graphics drivers. We install Mantid running the .exe installer by double clicking on the executable.

- On MacOSX, we create a package containing our dependencies and our compiled program in a .dmg app bundle. Only low level packages that are expected to exist on MacOSX. We install Mantid .dmg by running the installer by double clicking on the bundle.

- On Ubuntu, we create a package containing only our compiled program in a .deb format. We rely on the the currently available system packages to run Mantid. We install the Mantid .deb package using dpkg.

- On CentOS/RHEL7, we create a package containing only our compiled program in a .rpm format. We rely on the currently available system packages, optional packages from `rhel-7-workstation-optional-rpms` and some packages from EPEL to run Mantid. We install the Mantid .rpm package using the rpm command.

## Intended move forward

All operating systems should have a fully built and deployable conda-build implementation, where a use can in theory run a simple command in conda and it will install Mantid with all it's runtime dependencies, which with some small tweaks we can then package on all Operating Systems assuming that the conda-build recipe has been created and ran successfully.

The aim at this time is to create similar packages to what we have now on MacOSX and Windows, whilst shipping all dependencies in our Ubuntu and CentOS/RHEL7 which is a change. We will make a .exe for Windows, .dmg for MacOSX, .deb for Ubuntu, and a .rpm for CentOS/RHEL7 much like we do now on all operating systems.

### Conda build


### Producing Offline (None-Conda) packages

On all operating systems we will need to create the directory from which the package will be made, the command to do this will look something like this:
```bash
conda create -p package_dir mantid-workbench --copy -c mantid -c conda-forge-y
```
For Linux operating systems I suggest using FPM (`Effin Package Management - https://github.com/jordansissel/fpm) due to it's simplicity and ease of creating .deb and .rpm installers, from one machine, therefore in the future it should be possible to create all Linux distribution packages from one machine. At present it is not planned to use FPM for MacOSX as it doesn't support .dmg app bundles, and the support it does provide for .pkg files on MacOSX is less than ideal for the same reasons we already migrated away from .pkg files in the first place.

For MacOSX, we need to make .dmg files, we can use a very similar strategy to linux here but with hdiutil (Disk Utility built into MacOS used similarly to how FreeCAD has: https://github.com/FreeCAD/FreeCAD-Bundle/blob/master/conda/osx/create_bundle.sh)

For Windows, we intend to use Wix to produce a .exe installer. [IMPROVE WINDOWS BIT]

## Alternatives

Linux

MacOSX

Windows

## Looking to the future
Considering Mantid workbench is now becoming a bit of a behemoth like Mantid Plot was, it may be prudent to look at potential future project deliverables that don't include all parts of workbench.

Into the future, it would be possible to support many different packages of differing levels of support. It would be possible to have different levels of workbench specialisation utilising conda-build packages that incorporate different dependencies. For example, in the future different groups at ISIS would like to include python libraries that would only be useful for either Muons or Neutrons, in terms of analysis and reduction. 

In order to support multiple versions of Mantid a greater level of granularity will need to be achieved in the code base. The ability to actively seperate interfaces, algorithms, etc are all things that are possible given this proposed conda packaging implementation, given some tweaking and development time.

Proposed structure:
[DIAGRAM TO BE MADE]