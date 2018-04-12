Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Patch release status update
* Should the release branch have a fixed name, e.g. `release-next` (Gigg)
* [An issue with distributions and dimensionless units](https://github.com/mantidproject/documents/blob/fix-divide-distribution/Design/DistributionsAndDimensionlessData.md) and [Multiplication and division rules for histograms](https://github.com/mantidproject/documents/pull/25)
* Switch to using "GitHub Pull Request Builder Plugin" again in Jenkins. How would we do downstream/pipeline/matrix builds? Make use of label dependent builds, skip build phrases, _etc_ (Whitfield/Gigg)

Minutes
-------

Attendees: Draper, Gigg, Hahn, Nixon, Peterson, Soininen, Whitfield

* [Patch release milestone](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+milestone%3A%22Release+3.12.1%22+) was created
* The release branch will have a fixed name: `release-next`
* Jenkins "GitHub Pull Request Builder Plugin"
  * Will deploy after patch release is done
  * Need to verify that it works with forks
  * Will determine how to roll-back changes if deploy doesn't work
