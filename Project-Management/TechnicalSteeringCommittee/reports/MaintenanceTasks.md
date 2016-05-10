For 3.8 maintenance period
==========================

Highest priority
----------------

1. Remove Qt3support requirement from Mantid. 
   1. Finish removing Qt3support classes [#11891](https://github.com/mantidproject/mantid/issues/11891)  (Roman)
   2. Update functions that were removed in Qt4 (http://builds.mantidproject.org/job/master_clean-Qt3-warnings/)
      3. Set `WITH_QT3_SUPPORT_WARNINGS=ON` by default?  
   3. Remove Qt3support package from [mantid buildscript](https://github.com/mantidproject/mantid/blob/082354338d1fca01065c1b6af235d5ad769bdc69/CMakeLists.txt#L73).
1. Adding Python 3 compatability (`.py` files in mantid converted)
  1. Ensure Mantid builds when [linked against Python 3](https://docs.python.org/3.5/howto/cporting.html#changes-to-object-apis) and boost::python built against Python 3.
  2. Categorize the order which Python files will be made compatible with BOTH Python 2 & Python 3.
  3. Start adding `from __future__ import absolute_import, division, print_function` to these files and fix any errors.
      4. Require the above statement in all new work. 

Pool
----

42. **Look over tickets (assigned and created by you) and close invalid ones (everybody)**
1. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/job/master_pylint/) 
   2. [coverity](https://scan.coverity.com/projects/335) 
   3. [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy/)
   4. [cppcheck 1.73](http://builds.mantidproject.org/job/master_cppcheck/) 
1. Clang working on linux. 
   2. Related to NeutronAtom ([#11542](https://github.com/mantidproject/mantid/issues/11542), [#9267](https://github.com/mantidproject/mantid/issues/9267), [#7565](https://github.com/mantidproject/mantid/issues/7565), [#5670](https://github.com/mantidproject/mantid/issues/5670))  (requires gcc < 5 because not api compatible)
   3. A singleton stopping initializing python [#15293](https://github.com/mantidproject/mantid/issues/15293)
1. Move Windows Jenkins builds to use Ninja where possible.
1. Set a consistent policy for symbol visibility on all platforms. Currently on MSVC hides symbols by default.
   - Set [`CXX_VISIBILITY_PRESET`](https://cmake.org/cmake/help/v2.8.12/cmake.html#prop_tgt:LANG_VISIBILITY_PRESET) to `hidden` for gcc/clang and fix the builds.  [#15283](https://github.com/mantidproject/mantid/issues/15283)
1. Migrate to C++11 standard library features.
  5. The [rule of 3](https://en.wikipedia.org/wiki/Rule_of_three_(C%2B%2B_programming)) is now the rule of 5. In any class with a copy constructor and copy assignment operator, we should add a move constructor and move assignment operator.[#15290](https://github.com/mantidproject/mantid/issues/15290)
6. Remove gmock 1.6 [#16113](https://github.com/mantidproject/mantid/pull/16113)
7. Change tests of `CurveFitting` "functions" to be actual unit tests
8. Fix class_maker.py when used with Geometry folder. [#16104](https://github.com/mantidproject/mantid/issues/16104)
 

Assigned
--------

1. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion) - Limited to 2 man days [#12627](https://github.com/mantidproject/mantid/issues/12627) (Stuart)
2. Remove [stale branches](https://github.com/mantidproject/mantid/branches/stale) after checking with developers which ones they still need. (Stuart)
2. Run compilation time report weekly(?) on static analysis tab (Simon)
  -  profile build time to find which files we should focus on
  -  initial idea: set `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, and time each command in the generated `compile_commands.json`.
2. Explore ways to reduce number of recursive includes in `Algorithm.h` with desire of speeding up builds (Fede) - ~~[#15246](https://github.com/mantidproject/mantid/issues/15246)~~, [#15319](https://github.com/mantidproject/mantid/issues/15319)
1084. Compilation times of components of the [pipeline build for master nightly](http://builds.mantidproject.org/view/Master%20Pipeline/) in static analysis tab (Ross)
1085. Streamline pull-request builds (Martyn)
1. Look at addressing issues shown up by [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy). Someone needs to look through the issues and first prioritize what we look at, potentially see what the `autofix` can do for us. (Steve)
   1.  Split [performance-unnecessary-value-param](https://github.com/mantidproject/mantid/tree/performance-unnecessary-value-param) branch into smaller pieces and assign to pool
      1. Check whether it's acceptable to pass a pointer (nullable) or a reference (not null) instead of a `shared_ptr`.    
23. Top level code re-org decided at 2016 developer meetings [design](https://github.com/mantidproject/documents/pull/11) (Martyn)
1. move functions currently using `boost::tokenizer` to `Mantid::Kernel::StringTokenizer` [#15285](https://github.com/mantidproject/mantid/issues/15285) (Anton)
  2. clang-tidy's `google-runtime-references` check may help us find more.
7. Are there places where std::array (size known at compile time)  is more appropriate than std::vector (size known only at runtime)?[#15291](https://github.com/mantidproject/mantid/issues/15291) (Raquel)

#### Unassigned (not suitable for pool)

For another release
-------------------

1. Move to boost 1.60 on Windows. It allows classes marked final to be exposed to Python. We chave currently applied [this patch](https://github.com/boostorg/type_traits/commit/04a8a9ecc2b02b7334a4b3f0459a5f62b855cc68) to the 1.58 headers. 1.60.0 has been compiled [here](https://github.com/mantidproject/thirdparty-msvc2015/tree/boost-160) but there are warnings to fix with it.
1. Investigate and distribute rewrite/refactor nexus algorithms - [#12591](http://github.com/mantidproject/mantid/issues/12591)  (Martyn)
1. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage) [#12630](https://github.com/mantidproject/mantid/issues/12630) (Pete/Michael W)
1. all systemtests at least work on one platform [skipped system tests](http://developer.mantidproject.org/systemtests/) [#12615](https://github.com/mantidproject/mantid/issues/12615) (Pete)
   1. Design document for next iteration of testing (splitting small and big system tests, select where they run) - Pete
1. Estimate time require to move from qwt5 -> qwt6 (results in TSC report)
1093777. radon as a job in static analysis tab
1. Move to CMake 3 [#10205](http://github.com/mantidproject/mantid/issues/10205)
1. Making packages properly external - benefit low, current version is effectively frozen this way which is actually good for us.
   1. ANN
   2. GSoap ?
1. Editing actual variable and class names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) and not covered by `clang-format`, max 1 days effort
2. Enforcing python standards
1. Investigate breaking issues with updated dependencies
    3. iPython 4.0 [#13481](https://github.com/mantidproject/mantid/issues/13481)
1. Rework/clean up cmake as a whole
1. Restructuring `Framework` (and whole package structure) to make building and exporting classes easier
1. enable warnings and fix issues
  1. [-Wdouble-promotion](https://gist.github.com/quantumsteve/38c7be4a5606edecb223) (GCC only)
  1. [-Wfloat-equal](https://gist.github.com/quantumsteve/05b55c0743030b8c439d) (GCC and clang)
    1. create a common `almost_equals` function in Kernel [see this](http://en.cppreference.com/w/cpp/types/numeric_limits/epsilon). 
1. Since all of our compilers support `= delete`, we should use that directly and remove [ClassMacros.h](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/inc/MantidKernel/ClassMacros.h)
2. Investigate and resolve differences in fitting tests on different compilers & platforms.
4. [Copy only part of a column](https://github.com/mantidproject/mantid/issues/15884).
5. Replace `boost::math::isnan` and `boost::math::isinf` with `std::isnan` and `std::isinf`
  1. should some of these checks be replaced with [`std::isnormal`](http://www.cplusplus.com/reference/cmath/isnormal/)?

Converted to actual tickets during a release
--------------------------------------------

1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)
1. Proper rpm and deb packages (without cpack)
1. Editing algorithm and variable names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (Andrei)
