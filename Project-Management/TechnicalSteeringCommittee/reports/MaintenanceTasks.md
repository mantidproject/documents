For 3.6 maintenance period
--------------------------
1. Move to VS2015 Community Edition. See [notes] (https://github.com/mantidproject/documents/blob/master/Design/VisualStudio-2015.md)
1. Reorganised files in CurveFitting folder [#13347](https://github.com/mantidproject/mantid/issues/13347)

For 3.5 maintenance period
--------------------------
1. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage) ([trac #11792](http://trac.mantidproject.org/mantid/ticket/11792))
1. all systemtests at least work on one platform [skipped system tests](http://developer.mantidproject.org/systemtests/) ([trac #11777](http://trac.mantidproject.org/mantid/ticket/11777))
1. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/job/pylint_master)
   2. [coverity](https://scan.coverity.com/projects/335)
   3. [clang](http://builds.mantidproject.org/job/master_clean-clang/)
   6. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion) - Limited to 2 man days ([trac #11789](http://trac.mantidproject.org/mantid/ticket/11789))
   7. Refactoring of specific code areas (load nexus algorithms) - investigate and distribute ([trac #11753](http://trac.mantidproject.org/mantid/ticket/11753))
   4. ~~CutAndPaste detector~~
   5. ~~gcov (or equivalent)~~
1. Filling in argument list in python bindings (e.g. "self") ([trac #11786](http://trac.mantidproject.org/mantid/ticket/11786))
1. Enforcing the [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (on Framework) ([trac #11787](http://trac.mantidproject.org/mantid/ticket/11787))
   1. Re-run `clang-format`
   1. Editing actual variable and class names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) and not covered by `clang-format`, max 1 days effort
1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)

Too low benefit/priority for this release
-----------------------------------------
1. Proper rpm and deb packages (see previous item) - is this required
1. Making packages properly external - benefit low, current version is effectively frozen this way which is actually good for us.
   1. ANN
   2. GSoap ?
1. Back-port changes from QTIPlot to MantidPlot - 2 man days to produce a shopping list of functionality, benefits and estimates

   
For a different release
-----------------------
1. Move to CMake 3 [#9362](http://trac.mantidproject.org/mantid/ticket/9362), rework cmake as a whole, re-examine the package structure
1. Move to Qt 5
1. Move to Python 3
1. Investigate breaking issues with updated dependencies
    1. [Poco 1.6](http://trac.mantidproject.org/mantid/ticket/10976)
    2. oce 0.17 or OpenCascade 6.8
    3. iPython 3.0
