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
  * https://youtu.be/xu7q8dGvuwk
  * http://cppcast.com/2017/10/titus-winters/
* Add Python exports for `TestHelpers`?

Minutes
-------
Attendees: Heybrock, Bush, Moore, Draper, Gigg, Whitfield, Savici, Peterson

* TSC agrees to exposing more of `TestHelpers` to python
* Gigg will create a wiki page for what libraries/packages we use and what developers should prefer for various tasks in C++ and python
* Abseil will be added as an `ExternalProject`. This will wait for [this pull request](https://github.com/abseil/abseil-cpp/pull/8) to get merged.
* Paying for next portion of linode is coming up. ILL will look into paying for the next two years. This needs to be sorted by January 1st.
