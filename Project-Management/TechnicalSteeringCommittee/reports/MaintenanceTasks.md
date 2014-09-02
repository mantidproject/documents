1. Remove unused tools
   3. mwclient
2. Harmonizing external contributions with the rest of mantid (e.g. PSI subpackage)
3. Making packages properly external
   1. ANN
4. Reducing static analysis issues (discus stewards and soft limits)
   1. [pylint](http://builds.mantidproject.org/view/Static%20Analysis/job/pylint_develop/)
   2. [coverity](https://scan.coverity.com/projects/335)
   3. [clang](http://builds.mantidproject.org/view/Develop%20Builds/job/develop_osx-10.9-clang/)
   4. CutAndPaste detector
   5. gcov (or equivalent)
4. Back-port changes from QTIPlot to MantidPlot
2. Move to CMake 3 [#9362](http://trac.mantidproject.org/mantid/ticket/9362) and rework cmake as a whole
