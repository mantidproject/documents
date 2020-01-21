Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* Python 3 status
  - macOS/Windows: A few failing tests.
  - RHEL: Packages built in sandox copr. Needs a test build and then packages install on builders
  - Ubuntu - good to go
* [Status of new workbench](https://github.com/mantidproject/mantid/projects/9)
* [Status of SliceViewer replacement](https://github.com/mantidproject/mantid/projects/19)
* Rewrite graphical parts of instrument view
* Should clean up [all these Jenkins jobs](https://builds.mantidproject.org/view/All/)?
* Do we *really* want CI on Draft PRs?
* Documentation screenshots
* Static link everything we can?
* Thread scheduling issues

Minutes
-------
Attendees: Gigg, Nixon, Draper, Fairbrother, Vardanyan, Peterson, Savici, Whitfield, Hahn
* Welcome to David and Gemma.
* Picking up meetings for 2020. Agreed to drop frequency to once a month.
* Facilities are mostly aware of Python 3 changes.
* Python 3:
  - RHEL: Pete testing RHEL rpms. Building newer matplotlib to 2.2.4 to be able to drop 1.5 workarounds.
          Tested installing mantid42 with mantidunstable-python3. All good.
  - macOS/Windows: Small collections of tests to fix.
  - Will wait a few days for ORNL to collect external packages requiring updating to Python 3 and fix final tests.
  - Boost minimum updated to 1.65. New boost.python numpy module available for future.
* v4.3 will become 5.0 to indicate drop of Python 2 support
  - Will **NOT** drop MantidPlot.
