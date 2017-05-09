Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
- [Custom URL for Algorithms not part of the Mantid distribution](https://github.com/mantidproject/documents/pull/41/files)
- Request to include [yaml-cpp](https://github.com/jbeder/yaml-cpp) as a dependency:
  * packages are available for Red Hat, Ubuntu.
  * homebrew has a formula
  * just needs building on Windows.
- [External Python Interfaces](https://github.com/mantidproject/documents/pull/40)
- Are we comfortable mixing `boost::shared_ptr` and `std::shared_ptr`?
  - former has better support in `boost::python`
- [WorkspacePropertyWithIndex Design](https://github.com/mantidproject/documents/pull/42)
- Mantid developer meeting
  - [Developer survey](https://docs.google.com/forms/d/e/1FAIpQLSfm8KZ1BXvb_3zrOJKhjCjnaudooW4M5i6DRYC9giG0jl2v3Q/viewform?usp=sf_link)
  - SSI reports (science and tech one)
  - Focus this year continues on maintenance
  - Mantid is a scipy styled library - how do we make this a reality
  - Progress on mantid v4 work

Minutes
-------
Attendees: Draper, Heybrock, Moore, Borreguero, Peterson, Savici, Hahn

- Design for custom help url for algorithms was approved with minor changes
- `boost::shared_ptr` is required until all supported platforms are at boost 1.63 - Pete send email to dev list
