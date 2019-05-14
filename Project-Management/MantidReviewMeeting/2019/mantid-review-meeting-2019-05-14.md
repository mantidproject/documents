Agenda
======

* Jenkins now uses new mechanism capturing test failures. (Martyn)
  * It should catch all test failures, segfaults etc and avoid having to dig through the log
* Jenkins also has a [new warnings parser](https://builds.mantidproject.org/job/master_flake8/2802/flake8/) (Martyn)
  * The old one got deprecated and this one seems to produce nice output too.
* Now using [Material Design](https://material.io/tools/icons/?style=baseline) icons in workbench. (Martyn)
  - Dropped `qtawesome`
  - Wrapped icons directly our own very thin C++ shared library that converts glyphs to QIcon objects.
  - [mantid.qt.icons.get_icon](https://github.com/mantidproject/mantid/blob/master/qt/python/mantidqt/icons/__init__.py#L14) gives access in Python
  - `MantidQtIcons` gives access in C++

Questions
=========

* Add your questions here
