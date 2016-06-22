Agenda
=========
* GCC now has the same default symbol visibility as MSVC - [#16559](https://github.com/mantidproject/mantid/pull/16559)
  * Intro [talk](http://gnab.github.io/remark/remarkise?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmantidproject%2Fdocuments%2Fmaster%2FPresentations%2FDevMeetings%2F2016-01%2FSymbols_Gigg%2FSymbols_Gigg.md) from Mantid developer meeting.
* Mutli list selection for properties in Mantid (Nick Draper)
* feature usage reporting (Nick Draper)
* Python 2/3 compatibility:
  * The C++ layer has been updated to be compatible with Python 2 & 3
  * Most Python files have been updated
  * Cheat sheet - http://python-future.org/compatible_idioms.html
  * Use `from __future__ import (absolute import, division, print_function)` as the first line in all new Python files. Note that these are scoped to that file.
  * Use [`six`](https://pythonhosted.org/six/) module for 2/3 compatability

Questions
=========
* Place your item here
