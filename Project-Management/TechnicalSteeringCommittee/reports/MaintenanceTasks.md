For 3.5 maintenance period
--------------------------
1. Remove unused tools
   3. mwclient
2. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage)
3. Making packages properly external
   1. ANN
   2. GSoap ?
4. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/view/Static%20Analysis/job/pylint_develop/)
   2. [coverity](https://scan.coverity.com/projects/335)
   3. [clang](http://builds.mantidproject.org/job/master_clean-clang/)
   4. CutAndPaste detector
   5. gcov (or equivalent)
   6. header analysis (e.g. [include what you use](http://www.mantidproject.org/IWYU) and CLion)
4. Back-port changes from QTIPlot to MantidPlot
3. Proper rpm and deb packages (see previous item)
2. Filling in argument list in python bindings (e.g. "self")
1. Enforcing the [C++ coding standards](http://www.mantidproject.org/C%2B%2B_Coding_Standards) (on Framework)
   2. Re-run `clang-format`
   42. Editing actual variable and class names
108. Generate `.py` from `.ui` files as part of the build
109. Add `f2py` code to the builds
110. Update `class_maker.py` to generate code following current standards

For a different release
-----------------------
2. Move to CMake 3 [#9362](http://trac.mantidproject.org/mantid/ticket/9362), rework cmake as a whole, re-examine the package structure
2. Move to Qt 5
3. Move to Python 3
