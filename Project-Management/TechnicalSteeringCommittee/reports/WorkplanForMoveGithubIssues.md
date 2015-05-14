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

* Tickets created by me
* Any tickets with no one assigned
* Tickets assigned to me
* All tickets by owner
* My tickets for all iterations
* Tickets fixed per developer per milestone
* Patch candiate tickets
* Ticket burn rate. Per milestone, grouped by label (critical, blocker) etc
* How much each facility has contributed to Mantid over the last year. Number of issues fixed per facility
* SSC report query by ssc & keyword, columns are summary and milestone. Also need to know which facility the ssc item came from. See [here](http://trac.mantidproject.org/mantid/wiki/SSC%20Report%202015)
* **Custom query** - for example to create wiki-text for tickets per milestone grouped by technique area

***Desired Features***
* Milestone report (Pete has this covered)
* Easily extact queries by Student, or Core

**Implementation steps**
* Implement the aforementioned reports
* Nick want's all tickets migrated over. 
* All comments should be dragged across if possible
* Existing tickets need to be assigned to the correct person. Stuart might have a solution to this.
