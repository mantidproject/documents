Agenda
======

* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? 
* [User forum](/Design/UserForum.md) (Pete)
* [Signing mac executable](http://certhelp.ksoftware.net/support/articles/18835-how-do-i-sign-files-on-mac-osx-) 
* Downstream jobs for PR builds. Or can we otherwise speed things up. Request from Nick D.
* Apt & Yum repos on Linode (Martyn)
* `clang-format` providing [automatic reporting](http://builds.mantidproject.org/view/All/job/master_clang-format/) (Ross)
* Dropping support for OSX Mavericks in mantid 3.6 (Pete)
* [Visual Studio 2015](https://github.com/mantidproject/documents/blob/master/Design/VisualStudio-2015.md) (Martyn) along with minimum cmake version (Martyn/Pete)
* Outstanding issues for metrics reporting (Stuart)
* Linode Server - Expires End of Year (Stuart)

Minutes
=======
* Open pull request by Marina, Owen assigned
* Pros and cons of different user forum options listed in [User forum](/Design/UserForum.md) were discussed against requirement list. In summary the TSC recommend Discourse.
* Signing mac executable would require an Apple certificate. This can be looked into when there is a user need for this
* PR builds has now been speeded up moving doctest to Ubunto and more windows hardware, and PR builds is less of a problem. Nothing easy to move downstream 
* For `clang-format`. Ross investigate options for giving feedback back to developer where clang-format has changed code. Such feedback may include a link with information about which version of clang-format was used and how the developer can run clang-format prior to a PR 
