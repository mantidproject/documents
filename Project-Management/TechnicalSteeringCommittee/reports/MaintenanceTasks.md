For 3.7 maintenance period
==========================

Pool
----

42. **Look over tickets (assigned and created by you) and close invalid ones (everybody)**
1. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/job/master_pylint/) ([#15173](https://github.com/mantidproject/mantid/issues/15173) and more issues listed in [#14705](https://github.com/mantidproject/mantid/issues/14705))
   2. [coverity](https://scan.coverity.com/projects/335) (For 3.7: [#15214](http://github.com/mantidproject/mantid/issues/15214); highly specific: [#14157](http://github.com/mantidproject/mantid/issues/14157) [#13950](https://github.com/mantidproject/mantid/issues/13950), [#13949](https://github.com/mantidproject/mantid/issues/13949))
   3. [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy/) (Lamar)
   4. [cppcheck 1.72](http://builds.mantidproject.org/view/Static%20Analysis/job/cppcheck-1.72/) [#15821](https://github.com/mantidproject/mantid/issues/15281)
1. Clang working on linux. 
   2. Related to NeutronAtom ([#11542](https://github.com/mantidproject/mantid/issues/11542), [#9267](https://github.com/mantidproject/mantid/issues/9267), [#7565](https://github.com/mantidproject/mantid/issues/7565), [#5670](https://github.com/mantidproject/mantid/issues/5670))  (requires gcc < 5 because not api compatible)
   3. A singleton stopping initializing python [#15293](https://github.com/mantidproject/mantid/issues/15293)
1. Move all Jenkins builds to use Ninja where possible (incl. Windows) [#15282](https://github.com/mantidproject/mantid/issues/15282)
1. Set a consistent policy for symbol visibility on all platforms. Currently on MSVC hides symbols by default.
   - Set [`CXX_VISIBILITY_PRESET`](https://cmake.org/cmake/help/v2.8.12/cmake.html#prop_tgt:LANG_VISIBILITY_PRESET) to `hidden` for gcc/clang and fix the builds.  [#15283](https://github.com/mantidproject/mantid/issues/15283)
1. Add the [`-Wsuggest-override`](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html) flag when building with GCC 5.1 or later and fix resulting warnings. Consider doing the same for `-Wsuggest-final-types` and `-Wsuggest-final-methods`. [#15284](https://github.com/mantidproject/mantid/issues/15284)
1. Migrate to C++11 standard library features.
  2. Check for places where we should be using `std::unordered_meow` instead of `std::meow` (`meow = {set,multiset,map,multimap}?`) [#15287](https://github.com/mantidproject/mantid/issues/15287), [#15370](https://github.com/mantidproject/mantid/issues/15370)
  3. Move Poco::Mutex, Poco::FastMutex, boost::mutex,... to std::mutex. [#15288](https://github.com/mantidproject/mantid/issues/15288)
  4. Remove all uses of `boost::assign::list_of` etc. This should now be able to be replaced by brace-initializer lists.  ~~[#15175](https://github.com/mantidproject/mantid/issues/15175)~~
  5. The [rule of 3](https://en.wikipedia.org/wiki/Rule_of_three_(C%2B%2B_programming)) is now the rule of 5. In any class with a copy constructor and copy assignment operator, we should add a move constructor and move assignment operator.[#15290](https://github.com/mantidproject/mantid/issues/15290)
6. Remove gmock 1.6
 

Assigned
--------

1. Investigate breaking issues with updated dependencies (Steve)
    1. Poco 1.6 [#11815](http://github.com/mantidproject/mantid/issues/11815) / [design doc](https://github.com/mantidproject/documents/blob/master/Design/PocoStringTokenizer.md) / [PR #15150](https://github.com/mantidproject/mantid/pull/15150)
1. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion) - Limited to 2 man days [#12627](https://github.com/mantidproject/mantid/issues/12627) (Stuart)
2. Remove [stale branches](https://github.com/mantidproject/mantid/branches/stale) after checking with developers which ones they still need. (Stuart)
1. oclint as a job in static analysis tab (Pete)- ready as [PR #15359](https://github.com/mantidproject/mantid/pull/15359)
1. Implement [Mary Poppins](https://github.com/mary-poppins/mary-poppins) as a solution for testers (Martyn)
1. Look in to removing Qt3 suport code [#11891](https://github.com/mantidproject/mantid/issues/11891)  (Roman)
2. Run compilation time report weekly(?) on static analysis tab (Simon)
  -  profile build time to find which files we should focus on
  -  initial idea: set `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, and time each command in the generated `compile_commands.json`.
2. Explore ways to reduce number of recursive includes in `Algorithm.h` with desire of speeding up builds (Fede) - ~~[#15246](https://github.com/mantidproject/mantid/issues/15246)~~, [#15319](https://github.com/mantidproject/mantid/issues/15319)
1084. Compilation times of components of the [pipeline build for master nightly](http://builds.mantidproject.org/view/Master%20Pipeline/) in static analysis tab (Ross)
1085. Streamline pull-request builds (Martyn)
1. Look at addressing issues shown up by [clang-tidy](http://builds.mantidproject.org/view/Static%20Analysis/job/clang_tidy). Someone needs to look through the issues and first prioritize what we look at, potentially see what the `autofix` can do for us. (Steve)
   1. [modernize-use-default](https://github.com/mantidproject/mantid/compare/modernize-use-default) I think we want to move some of these to the header file.
   2. [cppcoreguidelines-pro-type-static-cast-downcast](https://github.com/mantidproject/mantid/compare/cppcoreguidelines-pro-type-static-cast-downcast) In some of these cases, we need to also check that `dynamic_cast` doesn't return `nullptr`. 
   3. [modernize-loop-convert](https://github.com/mantidproject/mantid/pull/14989) - ready as PR #14989.
   4. [modernize-use-nullptr](https://github.com/mantidproject/mantid/pull/14990) - ready as PR #14990.
   5. [readability-simplify-boolean-expr](https://github.com/mantidproject/mantid/pull/15079)- ready as PR #15079.
1. replace `boost:shared_ptr<Widget>(new Widget())` with `with boost::make_shared<Widget>()`
   2. grep for `shared_ptr` and `new` in the same line. ready as [PR 15219](https://github.com/mantidproject/mantid/pull/15219) (Pete)
3. Upgrade fedora build server (Stuart)
4. Move `brian` to be ubuntu 16.04 (Ross) - [Done](http://builds.mantidproject.org/job/master_clean-ubuntu-16.04/)
23. Top level code re-org decided at 2016 developer meetings [design](https://github.com/mantidproject/documents/pull/11) (Martyn)
1. move functions currently using `boost::tokenizer` to `Mantid::Kernel::StringTokenizer` [#15285](https://github.com/mantidproject/mantid/issues/15285) (Anton)
1. We have a lot of in-and-out parameters ([example #1](https://github.com/mantidproject/mantid/blob/master/MantidQt/MantidWidgets/src/AlgorithmSelectorWidget.cpp#L151), [example #2](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/src/ConfigService.cpp#L75)) that accept then immediately clear and fill a container. The intent would be much clearer (and run at least as fast) if the container was constructed internally and returned by value. [#15286](https://github.com/mantidproject/mantid/issues/15286) (Ready as [PR #15354](https://github.com/mantidproject/mantid/pull/15354)) (Tom)
  2. clang-tidy's `google-runtime-references` check may help us find more.
7. Are there places where std::array (size known at compile time)  is more appropriate than std::vector (size known only at runtime)?[#15291](https://github.com/mantidproject/mantid/issues/15291) (Raquel)
1. Change raw owning pointers to `std::unique_ptr<>`. Having `PropertyManager::declareProperty` accept a `unique_ptr` may be a good place to start.[#15289](https://github.com/mantidproject/mantid/issues/15289) Done in [#15439](https://github.com/mantidproject/mantid/pull/15439) (Tom)

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
1. Move to Qt 5
1. Move to CMake 3 [#10205](http://github.com/mantidproject/mantid/issues/10205)
1. Making packages properly external - benefit low, current version is effectively frozen this way which is actually good for us.
   1. ANN
   2. GSoap ?
1. Enforcing the [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (on Framework) [#12625](http://github.com/mantidproject/mantid/issues/12625)
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
3. Eliminate remaining uses of the [Qt3Support library](http://builds.mantidproject.org/job/master_clean-Qt3-warnings/)
4. [Copy only part of a column](https://github.com/mantidproject/mantid/issues/15884).
5. Replace `boost::math::isnan` and `boost::math::isinf` with `std::isnan` and `std::isinf`
  1. should some of these checks be replaced with [`std::isnormal`](http://www.cplusplus.com/reference/cmath/isnormal/)?

Converted to actual tickets during a release
--------------------------------------------

1. Add `f2py` code to the builds - this is an ongoing process, only complex items remain (translating fortran to python and effectively support as python)
1. Proper rpm and deb packages (without cpack)
1. Adding Python 3 compatability (`.py` files in mantid converted)
1. Editing algorithm and variable names - investigate the discrepancy of our code with that in [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (Andrei)
