Agenda
=========

* GCC will soon have the same default symbol visibility as MSVC (Anton): [#16559](https://github.com/mantidproject/mantid/pull/16559)
  * Intro [talk](http://gnab.github.io/remark/remarkise?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmantidproject%2Fdocuments%2Fmaster%2FPresentations%2FDevMeetings%2F2016-01%2FSymbols_Gigg%2FSymbols_Gigg.md) from Mantid developer meeting.

* Update to coding standards (Martyn) http://www.mantidproject.org/index.php?title=C%2B%2B_Coding_Standards&diff=26499&oldid=24375

* Python 2/3 compatibility (Martyn):
  * The C++ layer has been updated to be compatible with Python 2 & 3
  * All module-relatd Python files have been updated
  * (#16739)[https://github.com/mantidproject/mantid/issues/16739] umbrella issue for plugins (like Qt3). Please help!
  * Cheat sheet - http://python-future.org/compatible_idioms.html
  * Use `from __future__ import (absolute import, division, print_function)` as the first line in all new Python files. Note that these are scoped to that file.
  * Use [`six`](https://pythonhosted.org/six/) module for 2/3 compatability

* Mutli list selection for properties in Mantid (Nick Draper)
* feature usage reporting (Nick Draper)

Questions
=========
* Place your item here
