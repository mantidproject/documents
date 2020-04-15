# Minutes

## Mantid PMB Meeting 15

**Minutes of: 2020-04-03 UTC12:00-14:00**

**In Attendance:**

```
* CSNS - Junrong Zhang
* ESS - Andrew Jackson, [Jon Taylor (normally PMB chair) mostly ABSENT for family emergency]
* ILL - Miguel Gonzalez, Paolo Mutti, Gagik Vardanyan
* ISIS - Lamar Moore, Toby Perring (acting Chair), Pascal Manuel, Hannah Griffin
* ORNL - Mathieu Doucet, Andrei Savici
* Non-facility - Nick Draper (PM), Peter Peterson (TSC chair), Stephen Cottrell (User Group Chair), Daniel Murphy (Secretary)
```

## 1. PMB Membership 

 - Welcome to Junrong Zhang from CSNS

## 2. PM Report:
**Nick Draper talked through the main points of the report.**

- Some COVID-19 related risk-planning has been performed, and the effects of the pandemic on Mantid work have been mostly small apart from the ILL (see discussion below).
- Difficulties and benefits of move to Python 3. ORNL is still working on their move to Python 3.
- Workbench Status: Many key features have been implemented. Currently the major functionality issue is the Slice/Peaks viewer, which is holding back Single Crystal diffraction from moving to workbench. 
- The breaking-point for Mantidplot will be from Ubuntu 20.04 (released at end of April 2020) which won’t support Qt4
- It was agreed that there should be a worldwide date for MantidPlot to be dropped, requiring planning and feedback from scientists and developers at all facilities. 

In light of MantidPlot deprecation should we follow: 
- Plan 1.) Do not support Ubuntu 20.04 yet 
- Plan 2.) Support Ubuntu 18.04 and 20.04, but only workbench on the latter.

The consensus was that Plan 1 would help focus the development effort on Workbench, and that Plan 2 was only worth pursuing if it did not require much effort, especially as facilities aren’t going to move to Ubuntu 20.04 any time soon.

Nick was charged with putting together a realistic assessment of the tasks and effort required to transition to Workbench only support. This will be the major topic of an extraordinary PMB meeting 6-8 weeks from the date of this meeting. See Summary of Actions at the end of this document for a detailed list of actions on this topic.

**COVID impact discussed at each facility:**
ISIS and ORNL: Working from home, communicating online, not much slow down.
ILL: Find it hard helping new starters to be inducted into Mantid remotely.
ESS:  Not much development into mantid code base at present.
CSNS: Staff largely back at their facility.
*Overall, not much affect.*

## 3. TSC Report – Peter Peterson

Currently no CSNS member on the TSC - one should be nominated by CSNS, and the TSC to work out how to accommodate on-line meetings across the various sites.
Currently no developer working on Conda.
It would be great to have a mac developer license.

ESS are willing to work on Mantid and Scipp in parallel, with a smaller Mantid effort. They want to commission beamlines in 2022, which may involve using Workbench.

## 4. Mantid European Review (Renamed: Mantid Advisory Board)

A remote review was decided against by the review Board. Consequently the meeting has been delayed until the end of the year (November / December). This gives plenty of time to prepare documentation for the Board. Paul Butler (Board Chair), Jon Taylor (PMB Chair), together with the Panel members and alongside the local organisers have worked out a plan for the review, the latest documents to be circulated to all members of the PMB by Lamar Moore, who is acting as the secretary for the Board meeting.

The general ideas behind the review were discussed. The focus is on how Mantid delivers scientific output for the facilities and users.
The software strategy, management, approach, and process are to be reviewed, not in a very technical manner, but technically informed.

The PMB discussed other matters to be brought to the next Board planning meeting (which consists of Paul Butler and a subset of the PMB)
- CSNS are glad to join the review, and will liaise with Lamar Moore about this.
- SNS representatives on the PMB expressed their desire to be an equal partner of the Board review as the European partners. 
- The name should be changed to reflect the global nature and advisory status from European Review to Mantid Advisory Board.
- Suggest that contributing institutions e.g. PSI, ANSTO and MLZ be involved in the review, by providing feedback in a session structured like that for instrument scientists and that for users. It will provide a forum by which they could be asked if they would like to contribute more to Mantid.

Getting user input has been hard. Getting small feedback through forms has been the way forward in ISIS. About 90 forms have been received off and online. For the user session of the Board review we would like two or three super-users to represent different techniques. From the ORNL side, the SHUG was proposed as being able to provide input.

## 5. User and Developer Meeting planning

- The decision was taken to hold the next user meeting between January and April 2021. The SNS are still happy to host.
- The User meeting will not be until Spring 2021, therefore the Developer meeting should be split from this, and could even be virtual.
- One option is to attach the Developer meeting to NOBUGS 2020 in mid-October, if it goes ahead.
- Hannah proposed holding a virtual meeting in October even if NOBUGS does not go ahead, in order to gain experience of such meetings. The aim could be in future to hold two meeting per year, one virtual and one in person, which would be good as there would be more interaction and they have different benefits.

## 6. Licenses

There was agreement that Mantid needs the gsl license for a long list of dependencies.

The current license has the potential to be restrictive to downstream users of the Mantid framework, but only in the case that Mantid is an essential part of an external project (although Scipp does NOT have to be gpl compliant, as it is an aggregate). People may not choose to use Mantid due to this gpl license. This has nothing to do with European FAIR use.

If we did change license scheme, then (i) we would need to have all the facilities agree, including any past contributors, and (ii) there could be significant effort to rework some code. We need specific examples and strong intent if we are to alter our license. However, the full list of license dependencies of Mantid needs to be documented in any case.

## 7. Mac Dev IDs

General interest in having a handful of developers that can sign the Mac package, spread across different facilities. Cost is $ 99 per year.

## 8. Any other business

The Acting Chair raised the fact that the Mantid governance document is overdue a review given the changes in the number of partner institutes, and changes that have been made in whole or in part to the governance. The terms of reference of the PMB itself also need review. Discussion of updates will be another major item of the extraordinary PMB meeting in May 2020.

## Summary of Actions: 

-    [ ] Nick Draper and Martyn Gigg will work with SNS to get estimates for Sliceviewer and getting Workbench feature complete.
-    [ ] Nick will coordinate an assessment of a MantidPlot deprecation date.
-    [ ] Nick will estimate the extra effort required to follow implementation Plan 1 rather than Plan 2.
-    [ ] Nick to set a date 6-8 weeks from this meeting date (3 April) to hold an extraordinary PMB meeting about implementation of MantidPlot deprecation and full move to Workbench.

-    [ ] Junrong to provide a CSNS member for TSC.
-    [ ] TSC is to decide how to make the international meetings with CSNS member possible.

-    [x] Lamar will email PMB with Mantid Advisory Board member list, current schedule and the outcomes from the last planning meeting.
-    [ ] Lamar will send CSNS information about the review.
-    [ ] Matt Doucet to invite SHUG committee to participate in the user session on behalf of users at the SNS.

-    [ ] Each facility to come prepared at the extraordinary PMB meeting with possible dates for User meeting between Jan-April 2021.

-    [ ] Nick to complete dependencies list (with licenses involved) and distribute this info to other PMB members.
-    [ ] Nick will push forward on organising Mac Dev IDs for signing Mac packages

-    [ ] Nick will update PMB / Mantid Project governance documents with annotations as to the current status and intents (not deleting things that are no longer relevant) AND inform PMB members that they can now look through these documents in time for the next meeting.
-    [ ] All to look over PMB / Mantid Project governance documents (give Nick a week or two to update)
-    [ ] Lamar and Hannah to look at governance of other similarly sized open source projects 


## Next Agenda

- Date and review of planning for MantidPlot deprecation
- Review PMB / Mantid Project governance documents (all should look through beforehand)
- Update on Advisory Board Status
- Fix dates for User meeting in the period January-April 2021, and Developer meetings
