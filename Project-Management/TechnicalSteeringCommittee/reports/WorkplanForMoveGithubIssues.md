Workplan for moving to github issues.

**What needs to be taken into consideration**

* Open track tickets moved to github issue
  * Do all get moved?
  * How much information must be preserved?
* Trac remain live for getting information back from historical track tickets
* Updating existing Mantid documentation referring to trac
* Critical reports on trac produced from information from github issues (**the sooner we know these, the better**)

**Critcal reports we need to replicate**
Mostly taken from the trac queries [here](http://trac.mantidproject.org/mantid/report)

* Tickets created by me ([github](https://github.com/issues) | [trac](http://trac.mantidproject.org/mantid/report/1))
* Any tickets with no one assigned ([github](https://github.com/mantidproject/mantid/issues?q=is%3Aopen+is%3Aissue+no%3Aassignee) | [trac](http://trac.mantidproject.org/mantid/report/3))
* Tickets assigned to me ([github](https://github.com/issues/assigned) | [trac](http://trac.mantidproject.org/mantid/report/7))
* All tickets by owner ([github](https://github.com/mantidproject/mantid/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+sort%3Aassigned) | [trac](http://trac.mantidproject.org/mantid/report/10))
* My tickets for all iterations (github | [trac](http://trac.mantidproject.org/mantid/report/15))
* Tickets fixed per developer per milestone (github | [trac](http://trac.mantidproject.org/mantid/report/21))
* Patch candiate tickets ([github](https://github.com/mantidproject/mantid/issues?q=is%3Aopen+is%3Aissue+label%3A%22Patch+Candidate%22) | [trac](http://trac.mantidproject.org/mantid/report/20))
* Ticket burn rate. Per milestone, grouped by label (critical, blocker) etc (github | [trac](http://trac.mantidproject.org/mantid/report/24))
* How much each facility has contributed to Mantid over the last year. Number of issues fixed per facility (github | trac)
* SSC report query by ssc & keyword, columns are summary and milestone. Also need to know which facility the ssc item came from. See [here](http://trac.mantidproject.org/mantid/wiki/SSC%20Report%202015).
* **Custom query** - for example to create wiki-text for tickets per milestone grouped by technique area  ([github](https://github.com/mantidproject/mantid/issues) | [trac](http://trac.mantidproject.org/mantid/query))

***Desired Features***
* Milestone report ([github](https://github.com/mantidproject/mantid/milestones) | [trac](http://trac.mantidproject.org/mantid/roadmap))(Pete has this covered)
* Easily extact queries by Student, or Core

**Implementation steps**

* Nick want's all tickets migrated over. 
* All comments should be dragged across if possible
* Existing tickets need to be assigned to the correct person. Stuart might have a solution to this.
* Implement the aforementioned reports (then we can migrate)
