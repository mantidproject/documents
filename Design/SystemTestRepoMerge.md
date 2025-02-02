Merging Code & System Testing Repositories
==========================================

Motivation
----------

We currently have two systems for testing:

* unit tests that reside in the main code repository: <http://www.github.com/mantidproject/mantid> and
* system tests that reside in a separate repository: <http://www.github.com/mantidproject/systemtests>.

The separation is solely due to the requirement for larger amounts of data at the system testing level. Storing this in the main code repository would bloat the size of the repository and make it difficult to work with.

Keeping the repositories separate is becoming increasing frustrating for several reasons:

* it is more difficult to ensure that the code and tests stay in lock step;
* the size of the `systemtests` repository, currently ~3.5Gb, can cause cloning problems;
* testers must remember to check for changes in the `systemtests` repository and
* links from [Trac](http://trac.mantidproject.org) to `systemtests` do not work.

Proposal
--------

It is proposed that all code portions of the `systemtests` repository be folded back into the main `mantid`repository, with the data (both input & reference) handled using [CMake's](www.cmake.org) [ExternalData](http://www.cmake.org/cmake/help/v3.0/module/ExternalData.html) system. A good overview of CMake's ExternalData can be found [here](http://www.kitware.com/source/home/post/107).

In addition, it is proposed that existing data within the main code repository be moved to the same system so that there is a single approach to dealing with testing data.

### ExternalData Setup

CMake's ExternalData module uses a hash of the file contents to unambigously reference a data file. This also allows it to effectively version the data files. The real data is expected to be stored in a remote location and referenced by its hash. CMake uses a list url templates, defined by `ExternalData_URL_TEMPLATES` such as

```
http://fileserver.org/%(algo)/%(hash)
```

where `%(algo)` is replaced by the hashing algorithm and `%(hash)` by the hash code itself, to access the data. We will use the MD5 algorithm so `%(algo)` will always resolve to `MD5`.

In the source tree the test data file is replaced with a text file containing the hash code. The file is named using the data file name with `.%(algo)` appended to it, e.g. CNCS\_7860\_event.nxs is replaced by CNCS\_7860\_event.nxs.md5. CMake defines a set of build rules to fetch the real content from the remote locations as required. The data is stored in object stores defined by the variable `ExternalData_OBJECT_STORES` with the same layout as the server. Symbolic links (copies on Windows) are created in the directory defined by `ExternalData_BINARY_ROOT` and named after the real file that then points to the real data in the object store. It is recommended that `ExternalData_BINARY_ROOT` be placed outside of the build tree so that it is not constantly cleared away by a clean build.

### Workflow for Adding a File

In order for the build servers to run correctly, care will need to be taken when adding a new file as it will have to be present in the central store **before** pushing the commits that reference it to the git remote. It is proposed that a git alias is created called `add-test-data` that will call a script `git-add-test-data` with paths to file(s) as argument(s). For each file, `filename.ext`, the script will

* compute the MD5 hash using `cmake -E md5sum`;
* rename the real file to `EXTERNALDATA_filename.ext.%(hash)`, where `%(hash)` is the MD5 hash;
* store the MD5 hash in a text file named `filename.ext.md5`;
* run `git add filename.ext.md5`;
* tell user to upload file to server with the appropriate name (see below).

The alias can be setup with the command `git config --global alias.add-test-data "!bash Code/Tools/Git/git-add-test-data"`. It is suggested that a new `SetupForDevelopment.sh` script is created, analogous to the [VTK script](http://public.kitware.com/gitweb?p=VTK.git;a=blob;f=Utilities/SetupForDevelopment.sh), that sets up the git aliases for a developer.

#### Remote Servers

[TODO] We need to decide where to put the data. It seems logical to have a central copy, say on Linode and then have local mirrors at each facility for faster access. Developers would *pull* from the local one but *push* to the central one.

**Question: Should we consider installing [Midas](http://www.midasplatform.org/) from Kitware? - It comes with a desktop client that looks a lot like an ftp client but the server portion handles file indexing and serving etc or do we just let apache serve them as static files and install an ftp server?**

### System Test History

It is possible to save the commit history for the `systemtests` repository when folding it back to the `mantid` repository but in practice we do not believe it is worth the effort. The state of the `systemtests` on the particular date of transition will be used.

### System Test Layout in Main Repository

The layout of the `mantid` repository is not currently optimal, however this will not be addressed here.

It is proposed that rather than a simple dump of the `systemtests` into `mantid`, the layout be cleaned up. The proposal for the layout of the system tests and data within the `mantid` repository is as follows underneath the `Code/Mantid` directory

    .
    +--Framework
    +--Images
    +--Testing
    |  +-- Data
    |      +-- DocTest
    |          +-- file1.nxs.md5
    |      +-- SystemTest
    |          +-- file2.nxs.md5
    |      +-- UnitTest
    |          +-- file3.nxs.md5
    |  +-- PerformanceTests
    |      +-- ...
    |  +-- SystemTests
    |      +-- scripts
    |          +-- performance
    |              +-- analysis.py
    |              +-- ...
    |          +-- stresstestframework
    |              +-- algorithm_decorator.py
    |              +-- emailreporter.py
    |              +-- ...
    |          +-- InstallerTesting.py
    |          +-- runSystemTests.py
    |          +-- ...
    |      +-- tests
    |          +-- reference
    |              +-- reffile1.nxs.md5
    |          +-- ARCSReductionTest.py
    |          +-- ...

The `StressTests` directory is not used and will be dropped.
