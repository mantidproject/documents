Maintenance in the Release Period
=================================

The maintenance period starts as soon as the Beta test period for the current release starts.  However during that time there are some tasks that will always take precendence over any work on maintenance tasks.

1. Urgent Bug fixes or vital improvments for the current release
2. Testing PR's or manual unscripted testing for the current release
3. Encouraging and working with scientists on Beta testing


Maintenance tasks for 3.12
==========================

Highest priority
----------------

1. **Look over tickets (assigned and created by you) and close invalid ones (everybody) and [stale branches](https://github.com/mantidproject/mantid/branches/stale)**
1. Documentation
   1. Work left from dev meeting
   1. Move from wiki to developer `.rst`
   1. Change citations to new plugin
   1. Move all training to user `.rst`
1. Schedule stale PR detector (Nixon)
1. Address [unreliable tests](https://docs.google.com/spreadsheets/d/1qs81x3ZDDxvEu3H5Zg1KN8Qfu54dIVWKI2f3-zxFaFg/edit#gid=0) on build servers (Martyn to organise)
1. Update training courses for Python 3 compatability
93821. Parallell python3 release for ubuntu
14. move to gcc >= 5.3 (or gcc 6)
    1. [devtoolset-4](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-4/) on RHEL 7
3. Reducing static analysis issues that are on every pull request
   1. [cppcheck 1.80](http://builds.mantidproject.org/job/master_cppcheck/), upgrade version, move from jenkins into git
   2. [python3-flake8](http://builds.mantidproject.org/job/master_flake8_python3/) prioritizing complexity issues - Joe (issue [here](https://github.com/mantidproject/mantid/issues/20508))
   3. [pylint](http://builds.mantidproject.org/view/Static%20Analysis/job/master_pylint/) - need to review scope
   3. [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy/)
1. Extract performance tests build configuration into a script in the repository (Nixon)
1. Decouple scientific interface interdependencies. The recent restructure revealed some hidden dependencies (Gigg)
1. Move to El Capitan and drop support Yosemitte (Hahn)


Pool
----

Start from the top of the list

1. Check for slow unit tests
1. Reducing static analysis issues (discus stewards and soft limits)
    1. [coverity](https://scan.coverity.com/projects/335)
    3. [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy/)
    1. [pylint](http://builds.mantidproject.org/job/master_pylint/)
    2. [address-sanitizer](http://builds.mantidproject.org/view/Static%20Analysis/job/address_sanitizer/)
    2. [valgrind](http://builds.mantidproject.org/view/Valgrind/job/valgrind_core_packages/) (is currently only kernel and geometry)
1. enable warnings and fix issues
   1. [-Wdouble-promotion](https://gist.github.com/quantumsteve/38c7be4a5606edecb223) (GCC only)
   1. [-Wfloat-equal](https://gist.github.com/quantumsteve/05b55c0743030b8c439d) (GCC and clang)
   1. create a common `almost_equals` function in Kernel [see this](http://en.cppreference.com/w/cpp/types/numeric_limits/epsilon).
2. Remove [stale branches](https://github.com/mantidproject/mantid/branches/stale) after checking with developers which ones they still need
7. Change tests of `CurveFitting` "functions" to be actual unit tests [#16267](https://github.com/mantidproject/mantid/issues/16267) (Gemma)
1. Remove finders that exist in standard cmake 3.5
12. Fix GCC 7 compiler warnings (Peterson)
15. Remove uses of strcpy, sprintf, etc. [See ParaView-developers thread ](http://public.kitware.com/pipermail/paraview-developers/2017-April/005276.html)
1. Investigate overhead from logging [#20493](https://github.com/mantidproject/mantid/issues/20493)
1. Editing actual variable and class names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) and not covered by `clang-format`, max 1 days effort
1. Investigate breaking issues with updated dependencies: iPython 5.0 on mac
1084. Compilation times of components of the [pipeline build for master nightly](http://builds.mantidproject.org/view/Master%20Pipeline/) in static analysis tab (Ross)
1. Look at addressing issues shown up by [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy). Someone needs to look through the issues and first prioritize what we look at, potentially see what the `autofix` can do for us. (Steve)
   1.  Split [performance-unnecessary-value-param](https://github.com/mantidproject/mantid/tree/performance-unnecessary-value-param) branch into smaller pieces and assign to pool
   1. Check whether it's acceptable to pass a pointer (nullable) or a reference (not null) instead of a `shared_ptr`.
   1. While I prefer the modern syntax, these clang-tidy checks suggest A LOT of changes. If we make these changes, divide them up between multiple people over several cycles.
         1. [modernize-use-using](https://github.com/llvm-mirror/clang-tools-extra/blob/73313677032e42e218e72a4e388bbdc179c52da0/docs/clang-tidy/checks/modernize-use-using.rst) in llvm 3.9?
         2. [modernize-raw-string-literal](https://github.com/llvm-mirror/clang-tools-extra/blob/73313677032e42e218e72a4e388bbdc179c52da0/docs/clang-tidy/checks/modernize-raw-string-literal.rst) in llvm 3.9?
   2. Smaller checks that could be updated in a single PR.

For another release
-------------------

1. Remove workarounds for RHEL5/6 scattered around the code (mainly PythonInterface layer). (Martyn)
11. Stop using classes and member function removed in C++17.
    1. MSVC update 3 introduces [macros for fine-grained control](https://blogs.msdn.microsoft.com/vcblog/2016/08/12/stl-fixes-in-vs-2015-update-3/): `_HAS_AUTO_PTR_ETC`, `_HAS_OLD_IOSTREAMS_MEMBERS`, `_HAS_FUNCTION_ASSIGN`, `_HAS_TR1_NAMESPACE`, `_HAS_IDENTITY_STRUCT`
    2. See which ones we can turn off now.
    3. Identify functions and classes with deprecated code.
    4. example: we currently use `std::auto_ptr` with `boost::python`.
1. Investigate and distribute rewrite/refactor nexus algorithms - [#12591](http://github.com/mantidproject/mantid/issues/12591)  (Martyn)
2. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage) [#12630](https://github.com/mantidproject/mantid/issues/12630) (Pete)
3. Rework/clean up cmake as a whole
4. Making ANN an ExternalProject
1. [Boost 1.63](http://www.boost.org/users/history/version_1_63_0.html) has some nice improvements to `boost::python` - not available everywhere
   1. Added (basic) support for C++11 (std::shared_ptr, std::unique_ptr)
   2. Incorporated an extension API to wrap NumPy
   3. Would require building packages for Linux distributions with older version.
13. [Add Labels to unit tests](https://github.com/mantidproject/mantid/issues/17453)
14. [Improve ctest support with multi-configuration generators](https://github.com/mantidproject/mantid/issues/19303)
16. [Update gSOAP by using the system package or making it an external project](https://github.com/mantidproject/mantid/issues/19433)
10. Clang working more places (windows [#20492](https://github.com/mantidproject/mantid/issues/20492), neutronatom [#11542](https://github.com/mantidproject/mantid/issues/11542), [#9267](https://github.com/mantidproject/mantid/issues/9267), [#7565](https://github.com/mantidproject/mantid/issues/7565), [#5670](https://github.com/mantidproject/mantid/issues/5670), and a singleton stopping initializing python [#15293](https://github.com/mantidproject/mantid/issues/15293))
10. Remove uses of the deprecated [Q_FOREACH macro](https://www.kdab.com/goodbye-q_foreach/)
1. Restructuring `Framework` (and whole package structure) to make building and exporting classes easier
1. all systemtests at least work on one platform [skipped system tests](http://developer.mantidproject.org/systemtests/) [#12615](https://github.com/mantidproject/mantid/issues/12615) (Pete)
   1. Design document for next iteration of testing (splitting small and big system tests, select where they run) - Pete

Converted to actual tickets during a release
--------------------------------------------

1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)
1. Proper rpm and deb packages (without cpack)
