Agenda
======

* Review any outstanding external pull request
* Should [labels](https://github.com/mantidproject/mantid/labels) on github conform to a naming standard (i.e. spaces, pascalcase....)?
* Review of [skipped system tests](http://developer.mantidproject.org/systemtests/)
* Plan for moving to Github Issues (Stuart)
* [Maintenance tasks](/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md) for 3.5
* Use tcmalloc on Windows: v3.4 supports releasing memory back to the OS. Initial tests suggest much better performance for large workspaces, e.g. faster non-blocking delete (Martyn)
* Moving to a newer gcc on RHEL6. Decide on who should do the changes (Martyn)

Minutes
=======
Present: Pete, Ross, Stuart, Tobias, Owen and Anders

* No outstanding external pull requests found
* I was agreed that [labels](https://github.com/mantidproject/mantid/labels) must conform to the naming standard of using spaces between words and capital letter for each new words. Those few labels which did not already conform to this were updated accordingly
* Current [skipped system tests](http://developer.mantidproject.org/systemtests/). It was agreed to add a [Maintenance tasks](/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md) for 3.5 to get all system tests to run on at least one platform
* Plan for moving to Github Issues discussed. TSC members move to use Github Issues first before demonstrating/explaning the process to do this to all developers. Obtain information about which reports are critical on track (anders) 
* The Maintenance task of Re-run `clang-format`. Ross to report at next TSC meeting pros and cons of having `clang-format` automatic report on code not conforming to it. It was noted that different versions of `clang-format` may produce different formats 
* Stu reported on move to newer gcc on RHEL6 (4.9) and this will be added as software collection (stu)
* Item on tcmalloc moved to next meeting
