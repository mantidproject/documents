Agenda
======

* [livereduce](https://github.com/mantidproject/livereduce) daemon
  * Wraps [live data listening](https://www.mantidproject.org/MBC_Live_Data_User_Interface) in a `systemd` process for publishing images to [sns monitor](https://monitor.sns.gov/report/nom/88677/)
  * Instrument scientists maintain a script to [process a chunk](https://github.com/mantidproject/autoreduce/blob/master/ReductionScripts/sns/powgen/reduce_PG3_live_proc.py) and a script to [process the acumulated data](https://github.com/mantidproject/autoreduce/blob/master/ReductionScripts/sns/powgen/reduce_PG3_live_post_proc.py)
  * When the run finishes normal autoreduction processes the data and pushes a final updated plot

* Jenkins updates
  * System tests are skipped if changes are **only** in `docs/`, `MantidQt/*` or `MantidPlot/*`
  * Packaging has been turned off by default on all PR builds. Use rebuild with `BUILD_PACKAGE=true` to force a package build

* Reminder
  * If your ticket is merged into `release-v3.9` check if the corresponding issue is closed when the branch is merged into master

Questions
=========

* Add your questions here
