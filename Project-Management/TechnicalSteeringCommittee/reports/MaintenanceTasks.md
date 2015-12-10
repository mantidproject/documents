For 3.6 maintenance period
==========================

Pool
----
1. ~~Separate classes in `WorkspaceValidators.h` into separate files, including putting implementations in source files [#11035](https://github.com/mantidproject/mantid/issues/11035)~~
1. ~~Remove all cases of `#include <iostream>` from headers (or switch to `iosfwd`) and see if they required in source files [#13689](https://github.com/mantidproject/mantid/issues/13689)~~
1. Filling in argument list in python bindings (e.g. "self" etc) ([#12624](http://github.com/mantidproject/mantid/issues/12624) is umbrella issue. Task divided by submodule: ~~kernel ([#13690](http://github.com/mantidproject/mantid/issues/13690))~~, ~~geometry ([#13691](http://github.com/mantidproject/mantid/issues/13691))~~, ~~api ([#13692](http://github.com/mantidproject/mantid/issues/13692))~~, dataobjects ([#13693](http://github.com/mantidproject/mantid/issues/13693))
1. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/job/master_pylint/)
   2. [coverity](https://scan.coverity.com/projects/335) (~~[#13918](http://github.com/mantidproject/mantid/issues/13918)~~ and more issues listed in ~~[#12629](https://github.com/mantidproject/mantid/issues/12629)~~)
   3. [clang](http://builds.mantidproject.org/job/master_clean-clang/)
1. ~~Fix compilation errors with RHEL6 & devtoolset-2 [#13729](https://github.com/mantidproject/mantid/issues/13729)~~


Assigned
--------

#### Martyn
1. ~~Move to VS2015 Community Edition. See [notes] (https://github.com/mantidproject/documents/blob/master/Design/VisualStudio-2015.md) (Martyn)~~
1. Investigate and distribute rewrite/refactor nexus algorithms - [#12591](http://github.com/mantidproject/mantid/issues/12591)  (Martyn)

#### ~~Anders~~ Nick
1. ~~Reorganised files in CurveFitting folder [#13347](https://github.com/mantidproject/mantid/issues/13347)~~

#### Steve H
1. Move to ParaView 4.4 or 5.0 (Steven H)
1. Investigate breaking issues with updated dependencies (Steven H)
    1. Poco 1.6 [#11815](http://github.com/mantidproject/mantid/issues/11815) / [design doc](https://github.com/mantidproject/documents/blob/master/Design/PocoStringTokenizer.md)
    2. ~~oce 0.17 or OpenCascade 6.8 on mac~~ [#13844](https://github.com/mantidproject/mantid/issues/13844)

#### Pete (+ helpers)
1. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage) [#12630](https://github.com/mantidproject/mantid/issues/12630) (Pete/Michael W)
1. all systemtests at least work on one platform [skipped system tests](http://developer.mantidproject.org/systemtests/) [#12615](https://github.com/mantidproject/mantid/issues/12615) (Pete)
   1. Design document for next iteration of testing (splitting small and big system tests, select where they run) - Pete

#### Stuart
1. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion) - Limited to 2 man days [#12627](https://github.com/mantidproject/mantid/issues/12627) (Stuart)
1. ~~Move main code directory two levels up (Stuart)~~
   1. ~~Linux-ify the directory names~~

#### Anton
1. ~~Roll out MDUnits and MDFrame wider (Anton)~~

#### Ross
1. ~~Re-run `clang-format` (will likely be done much earlier)~~

#### Unassigned (not suitable for pool)
4. Simplify `Framework` only builds (MPI) 
1. Estimate time require to move from qwt5 -> qwt6 (results in TSC report)
1. Look in to removing Qt3 suport code [#11891](https://github.com/mantidproject/mantid/issues/11891) (results in TSC report)
1. CutAndPaste detector as a job in static analysis tab
1. Clang working on linux. Related to NeutronAtom ([#11542](https://github.com/mantidproject/mantid/issues/11542), [#9267](https://github.com/mantidproject/mantid/issues/9267), [#7565](https://github.com/mantidproject/mantid/issues/7565), [#5670](https://github.com/mantidproject/mantid/issues/5670)) and a singleton stopping initializing python
1. Explore [Mary Poppins](https://github.com/mary-poppins/mary-poppins) as a solution for testers (needs more detail)

Too low benefit/priority for this release
-----------------------------------------
1. Proper rpm and deb packages - is this required
1. Making packages properly external - benefit low, current version is effectively frozen this way which is actually good for us.
   1. ANN
   2. GSoap ?
1. Back-port changes from QTIPlot to MantidPlot - 2 man days to produce a shopping list of functionality, benefits and estimates
5. gcov (done on `Framework`)
1. Enforcing the [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (on Framework) [#12625](http://github.com/mantidproject/mantid/issues/12625)
   1. Editing actual variable and class names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) and not covered by `clang-format`, max 1 days effort
1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)


For a different release
-----------------------
1. Move to CMake 3 [#10205](http://github.com/mantidproject/mantid/issues/10205)
1. Move to Qt 5
1. Adding Python 3 compatability
1. Investigate breaking issues with updated dependencies
    3. iPython 4.0 [#13481](https://github.com/mantidproject/mantid/issues/13481)
1. Rework/clean up cmake as a whole
1. Restructuring `Framework` (and whole package structure) to make building and exporting classes easier

Release 3.7 maintenance
-----------------------
 1. Look at addressing issues shown up by [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy). Someone needs to look through the issues and first prioritize what we look at, potentially see what the `autofix` can do for us.
