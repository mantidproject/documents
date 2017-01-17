Maintenance in the Release Period
=================================

The maintenance period starts as soon as the Beta test period for the current release starts.  However during that time there are some tasks that will always take precendence over any work on maintenance tasks.

1. Urgent Bug fixes or vital improvments for the current release
2. Testing PR's or manual unscripted testing for the current release
3. Encouraging and working with scientists on Beta testing


Maintenance tasks for 3.10
==========================

Highest priority
----------------

1. Migrate Mantid internals to use `HistogramData` features. Remove usage of the "Deprecated" legacy interface.
  * Start by reading the concepts page for [HistogramData](http://docs.mantidproject.org/nightly/concepts/HistogramData.html)
  * Read these [refactoring notes](https://github.com/mantidproject/documents/blob/master/Help/HistogramData/HistogramData-refactoring.md)
  * Look at unsafe methods marked *Deprecated* in the `MatrixWorkspace` header [here](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/MatrixWorkspace.h).
  * If you require help or have questions ask Simon Heybrock, Lamar Moore or Owen Arnold.
  * Pick some algorithm from the [umbrella issue](https://github.com/mantidproject/mantid/issues/17641) and get started.
1. Finish GSL2 compatibility work (Roman) **needs follow-on?** Tests that fail: [#16680](https://github.com/mantidproject/mantid/issues/16680).
1. Adding Python 3 compatability (`.py` files in mantid converted) (Gigg and Whitfield lead) Issue [#16739](https://github.com/mantidproject/mantid/issues/16739)
  3. Start adding `from __future__ import absolute_import, division, print_function` to these files and fix any errors ([general docs](http://python-future.org/compatible_idioms.html)).
  4. use [2to3 code translation](https://docs.python.org/2/library/2to3.html)?
  4. Require the above statement in all new work.


Pool
----

42. **Look over tickets (assigned and created by you) and close invalid ones (everybody)**
1. Reducing static analysis issues (discus stewards and soft limits)
   2. [coverity](https://scan.coverity.com/projects/335)
   4. [cppcheck 1.73](http://builds.mantidproject.org/job/master_cppcheck/)  and [#17155](https://github.com/mantidproject/mantid/issues/17155)
   3. [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy/)
   2. [address-sanitizer](http://builds.mantidproject.org/view/Static%20Analysis/job/address_sanitizer/)
   294742. [flake8](http://builds.mantidproject.org/job/master_flake8/)
   1. [pylint](http://builds.mantidproject.org/job/master_pylint/)
1. Since all of our compilers support `= delete`, we should use that directly and remove [ClassMacros.h](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/inc/MantidKernel/ClassMacros.h)
1. Replace Boost.TypeTraits with <type_traits>
11. Stop using classes and member function removed in C++17.
   1. MSVC update 3 introduces [macros for fine-grained control](https://blogs.msdn.microsoft.com/vcblog/2016/08/12/stl-fixes-in-vs-2015-update-3/).
       2. _HAS_AUTO_PTR_ETC
       3. _HAS_OLD_IOSTREAMS_MEMBERS
       4. _HAS_FUNCTION_ASSIGN
       5. _HAS_TR1_NAMESPACE
       6. _HAS_IDENTITY_STRUCT
   2. See which ones we can turn off now.
   3. Identify functions and classes with deprecated code.
     4. example: we currently use std::auto_ptr with boost::python.
13. [Add Labels to unit tests](https://github.com/mantidproject/mantid/issues/17453)
1. enable warnings and fix issues
  1. `/W3` on Visual C++ - https://msdn.microsoft.com/en-us/library/thxezb7y.aspx recommends this for production
  1. [-Wdouble-promotion](https://gist.github.com/quantumsteve/38c7be4a5606edecb223) (GCC only)
  1. [-Wfloat-equal](https://gist.github.com/quantumsteve/05b55c0743030b8c439d) (GCC and clang)
    1. create a common `almost_equals` function in Kernel [see this](http://en.cppreference.com/w/cpp/types/numeric_limits/epsilon).


Assigned
--------

1. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion) - Limited to 2 man days [#12627](https://github.com/mantidproject/mantid/issues/12627) (Stuart)
2. Remove [stale branches](https://github.com/mantidproject/mantid/branches/stale) after checking with developers which ones they still need. (Stuart)
7. Change tests of `CurveFitting` "functions" to be actual unit tests [#16267](https://github.com/mantidproject/mantid/issues/16267) (Raquel)
6. Move gmock 1.7 to be ExternalProject [#16266](https://github.com/mantidproject/mantid/issues/16266) (Peterson)
1. Move to boost 1.60 on Windows. It allows classes marked final to be exposed to Python. We chave currently applied [this patch](https://github.com/boostorg/type_traits/commit/04a8a9ecc2b02b7334a4b3f0459a5f62b855cc68) to the 1.58 headers. 1.60.0 has been compiled [here](https://github.com/mantidproject/thirdparty-msvc2015/tree/boost-160) but there are warnings to fix with it.
13. Replace `new Progress` with `Kernel::make_unique<Progress>` in the ~~35~~ 40 files that do it [#17590](https://github.com/mantidproject/mantid/issues/17590) (Dimitar)
12. Fix GCC 6 compiler warnings [#17593](https://github.com/mantidproject/mantid/issues/17593) (Dimitar)
  1. [master_clean-fedora24](http://builds.mantidproject.org/job/master_clean-fedora24/)
42. Modernize more code to use functions now found in `<string>`. `atoi` should move to `std::stoi` and `atof` should move to `std::stof` ([reference](http://www.cplusplus.com/reference/string/stof/)). [#17600](https://github.com/mantidproject/mantid/issues/17600) (Lottie)

Unassigned (not suitable for pool)
----------------------------------


Unsorted
--------

8. Investigate overhead from logging. Specifically
   9. Would we benefit from checking the logging level before constructing a string?
   10. When we have a single string literal, ensure it is passed directly to the appropriate Logger method.
   10. Investigate why it is faster to construct a string with std::stringstream and pass that string to the logger instead of directly using the logger's insertion operator. Can this be easily fixed upstream?
   11. Can we minimize flushing the stream inside the [thread-safe log stream](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/src/ThreadSafeLogStream.cpp)?
1. all systemtests at least work on one platform [skipped system tests](http://developer.mantidproject.org/systemtests/) [#12615](https://github.com/mantidproject/mantid/issues/12615) (Pete)
   1. Design document for next iteration of testing (splitting small and big system tests, select where they run) - Pete
1093777. radon as a job in static analysis tab
1. Editing actual variable and class names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) and not covered by `clang-format`, max 1 days effort
1. Investigate breaking issues with updated dependencies: iPython 5.0 on mac
1. Restructuring `Framework` (and whole package structure) to make building and exporting classes easier
2. Investigate and resolve differences in fitting tests on different compilers & platforms.
1084. Compilation times of components of the [pipeline build for master nightly](http://builds.mantidproject.org/view/Master%20Pipeline/) in static analysis tab (Ross)
1. Look at addressing issues shown up by [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy). Someone needs to look through the issues and first prioritize what we look at, potentially see what the `autofix` can do for us. (Steve)
   1.  Split [performance-unnecessary-value-param](https://github.com/mantidproject/mantid/tree/performance-unnecessary-value-param) branch into smaller pieces and assign to pool
      1. Check whether it's acceptable to pass a pointer (nullable) or a reference (not null) instead of a `shared_ptr`.
23. Top level code re-org decided at 2016 developer meetings [design](https://github.com/mantidproject/documents/pull/11) (Martyn)
9. clang-tidy
     1. While I prefer the modern syntax, these clang-tidy checks suggest A LOT of changes. If we make these changes, divide them up between multiple people over several cycles.
         1. [modernize-use-using](https://github.com/llvm-mirror/clang-tools-extra/blob/73313677032e42e218e72a4e388bbdc179c52da0/docs/clang-tidy/checks/modernize-use-using.rst) in llvm 3.9?
         2. [modernize-raw-string-literal](https://github.com/llvm-mirror/clang-tools-extra/blob/73313677032e42e218e72a4e388bbdc179c52da0/docs/clang-tidy/checks/modernize-raw-string-literal.rst) in llvm 3.9?
      2. Smaller checks that could be updated in a single PR.
10. Clang/C2 working on Windows
   1. Add the CMake 3.6 flag `-T v140_clang_3_7` to configure
14. move to [devtoolset-4](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-4/) on RHEL 6 & 7

For another release
-------------------
1. Investigate and distribute rewrite/refactor nexus algorithms - [#12591](http://github.com/mantidproject/mantid/issues/12591)  (Martyn)
2. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage) [#12630](https://github.com/mantidproject/mantid/issues/12630) (Pete/Michael W)
3. Rework/clean up cmake as a whole
4. Making ANN an ExternalProject
1. [Boost 1.63](http://www.boost.org/users/history/version_1_63_0.html) has some nice improvements to `boost::python`
   1. Added (basic) support for C++11 (std::shared_ptr, std::unique_ptr)
   2. Incorporated an extension API to wrap NumPy
   3. Would require building packages for Linux distributions with older version.

Converted to actual tickets during a release
--------------------------------------------

1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)
1. Proper rpm and deb packages (without cpack)
1. Clang working on linux.
   2. Related to NeutronAtom ([#11542](https://github.com/mantidproject/mantid/issues/11542), [#9267](https://github.com/mantidproject/mantid/issues/9267), [#7565](https://github.com/mantidproject/mantid/issues/7565), [#5670](https://github.com/mantidproject/mantid/issues/5670))  (requires gcc < 5 because not api compatible)
   3. A singleton stopping initializing python [#15293](https://github.com/mantidproject/mantid/issues/15293)
