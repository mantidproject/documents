# Minutes

## Mantid PMB Meeting 13

**Minutes of: 2019-01-19T09:00-4:00**

## In Attendance

```
* ESS - Taylor
* ILL - Gonzalez, Mutti
* ORNL - Granroth, Peterson, Ramirez-Cuesta, Leal
* ISIS - Draper, Greenfield, Cottrell, Manuel, Moore
```

## Changes to the PMB

- Chair of PMB position available
- D. Greenfield is leaving the PMB.

## Pending issues / report on actions of the last PMB meeting

**Mantid Developers + User meeting @ILL, Grenoble**

* The Agenda will be updated with hotels.
* ORNL is hosting the next Mantid Developers + User meeting. The dates should be narrowed during the Grenoble meeting and then circulated through the PMB for approval.

**Mid-term scientists requirements**

- No changes to the spreadsheet since the last PMB meeting.

- N. Draper has chosen some key areas common across instruments / facilities.

  - Generic interfaces + workflow.
  - Although the reduction is different among instruments, some small components can be reused.
  - Useful for users to see (quasi) the same interface across instruments.

- Suggestion to develop a "gap analysis": see what other facilities don't have.

- Given the scarcity of resources, SSC should set the priorities and the PMB then decide what to implement.

**Project managers team (PMT)**

- N. Draper, P. Peterson and O. Arnold wrote the initial role of the PMT.
  - See *PM report to Project Management Board*, Section 5 "Mantid Project Managers Team".
- PMT will propose solutions. PMB decides based on those proposals.
- The suggestion in the report should be implemented and refined in the future. 
  - Chair: N. Draper.
  - Deputy chair: P. Peterson
  - See actions.

**Dataset design**

- Single data object for the whole Mantid.
- It will break Mantid as it is considerably different from the current workspace.
  - It will require changes in a fair amount of algorithms.
- Mantid as it is does not fit the requirements of ESS. The new dataset fits ESS and is a look in the future.
- The new dataset appears to increase the performance of Mantid. More tests are required and will be done.
- The problem appears to be resources to cope with the changes this will introduce.
- See actions.

## PM Report

* N. Draper reported on the Report previously shared with the PMB Members.
* Most users use the last release: version 3.13.0
* Last release introduced crash errors.
* The statistics need to be more "meaningful". Some information about the errors / crashes would be useful.
* Since the new Workbench is planned to be released without *Slice Viewer*, ORNL may place some resources to help with its inclusion. See actions.

## TSC Report

* P. Peterson reported on the Report previously shared with the PMB Members.
* Discussion on reduce the number of platforms supported. Too much resources are being spent. Rely more on the docker images. To date not many users are using docker (perhaps problems with the installation of the docker software).

## Facility News

* ILL: New permanent Mantid developer. Second phase of the project: 3 new developers will be hired .
* ORNL: SNS just came up. HFIR is in a long shutdown due to fuel element defects.
* ISIS: New temporary Mantid hires. New Mantid position will be advertised soon.
* ESS: The annual review suggested to prioritize the data collection.

## Summary of actions

* Call for volunteers is open for the PMB Chair.
* Make Hotel list available in the Mantid Developers + User meeting agenda.
* In the Grenoble's meeting discuss the uniformity across the facilities / instruments: interfaces, workflows, etc.
* Isis will circulate a document on the European review.
* PMT:
  * PMT should be implemented ASAP.
  * Change the documentation based on the PMB suggestions and circulate it.
* New dataset design.
  * ESS will continue the developments. Report to the PMB the result of this development.
* Better statistics on Mantid the errors / crashes.
* New Workbench:  ORNL may place some resources to help with *Slice Viewer* inclusion in the next release.

# Next Meeting

- Take advantage of the Developers + User meeting in Grenoble to meet face to face.