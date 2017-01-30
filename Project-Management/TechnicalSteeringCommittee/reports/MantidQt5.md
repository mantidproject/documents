Mantid requires Qwt 5.2, which requires Qt4 with the Qt3Support
library. Qwt 6 has a different API and the decision was made to switch
1D and 2D plotting to matplotlib

Mantid Depends on QwtPlot3d, which hasn't been updated since
June, 2007. It requires Qt4 with the Qt3Support library. Similar
functionality is available in matplotlib and ParaView.

Qt 4.8 is unsupported after December 2015. Afterwards, there will be
NO UPDATES to the open source project.
http://blog.qt.io/blog/2015/05/26/qt-4-8-7-released/
http://blog.qt.io/blog/2014/11/27/qt-4-8-x-support-to-be-extended-for-another-year/

Unofficial patches are required to build with MSVC 2015. What about
MSVC 2017?
https://github.com/mantidproject/thirdparty-msvc2015/blob/master/build-scripts/build-qt4.bat#L50

Qt4 was removed from Homebrew in December, 2016.
https://github.com/Homebrew/homebrew-core/commit/05eaba4cd570b000aa85d91a01e2b4d503894f00

pyqt4 was moved to the boneyard.
https://github.com/Homebrew/homebrew-core/pull/6817

unofficial Qt4 tap. Unofficial patches required to build with El
Capitan and Sierra.  https://github.com/cartr/homebrew-qt4

ParaView 5.3 will, by default, build against Qt 5. One or two build
servers will keep Qt4.  Utkarsh is planning to keep Qt4 support for
v5.4 (planned for Sept 2017), then dropping Qt 4 support.  However, if
there's a strong community push back, they will revisit that plan.
