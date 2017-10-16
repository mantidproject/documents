Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Add [abseil](https://abseil.io/) as a git submodule or an external project?
  * String functionality like `absl::StrCat()`, `absl::StrJoin()` and `absl::StrSplit()` would be useful. My hope is that their C++17ish types like `string_view`, `any`, `optional` and `variant` provide a better upgrade paths to the standard than boost.
  * Can we accept their 5 year compatibility and live at head philosophy?
  * https://opensource.googleblog.com/2017/09/introducing-abseil-new-common-libraries.html
  * https://github.com/abseil/abseil-cpp
  * https://youtu.be/tISy7EJQPzI
