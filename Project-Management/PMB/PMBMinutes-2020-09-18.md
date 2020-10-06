#  Minutes

##  Mantid PMB Meeting 19

**Minutes of: 2020-09-18 UTC12:00-14:00**

**In Attendance:**
```
* CSNS - (absent)

* ESS - Jon Taylor (PMB Chair)

* ILL - Miguel Gonzalez, Paolo Mutti, Gagik Vardanyan

* ISIS - Lamar Moore (co-PM), Toby Perring, Hannah Griffin

* ORNL - Mathieu Doucet, Andrei Savici

* Non-facility - Peter Peterson (co-PM + TSC chair), Stephen Cottrell (User Group Chair), Daniel Murphy (Secretary)
```
##  Agenda

-  Discuss the master governance proposal: https://github.com/mantidproject/collaboration/pull/1

##  1. Beginning Discussions

- Hannah mentioned after talking to the Director of ISIS that there should be a Mantid Governance / Confirmation board comprising the directors of each partner facility, which meets very infrequently (roughly every 3-5 years) to confirm commitment to the Mantid project.

- In forming the new governance model, answering the [immediate questions raised by Jon](https://github.com/mantidproject/collaboration/pull/1#issuecomment-694769218)
  is a good start. Thoughts towards a future ecosystem vision can be saved for later.
  **Those questions, which the TSC should be able to answer are:**
    _•    How partners collaborate and contribute
    •    How does the development workflow run - accepting changes and new contributions & moving from a single PM arrangement - how is the existing development progress maintained? How do we not break other sites critical code
    •    what group is responsible for release schedules
    •    What group is responsible for quality and functionality
    •    What group is responsible for requirements and scientific direction
    •    How are these groups interacting.
    •    How are significant architecture changes handled, planned, executed
    •    How are breaking changes handled_

- These questions were posed by Toby: _How do you feed in science requirements?? What do each facility want to see scientifically, before translating that into software?_

  Lamar mentioned that requirements gathering should be the responsibility of the developers as this is part of their skill set. This will continue to be performed locally at each facility and higher-level work can then be brought to the cross facility TSC. The user meeting is also a great platform for conversations about priorities being communicated between the facilities.

  The science input can drive the direction, but the actual details are the role of the development teams. There is a need to clearly describe how the different committees and groups have responsibility, which should be the focus of the next meeting.

- The 3-5 year roadmap is shaped by director level decisions, but should be owned by a steering committee that comprises a mix of scientific and computing members (as the current PMB does). Lamar, Paolo, Pas and others mentioned that it is important for there to be two-way feedback between instrument scientists and developers. 

  Pas pointed out that, while this two-way feedback works well on a local level, this is limited to short term aims, and does not capture long term goal and new technologies.

- Pete described Mantid as two different entities: 1) the cross-facility collaboration / project and 2) the product which moves forward with whatever local desires seem to be. We are okay at getting agreement upon requirements in the TSC. However, the local implementation will not always agree with the previously agreed decisions. There needs to be better communication between the facilities but also within facilities, in order to feedback back up to the TSC. The TSC was great for discussing the need for and progress of Mantid Workbench. It has also been great to inform other facilities of current major developments e.g. Geometry for Monte Carlo Absorption Correction at ISIS.

- Andrei mentioned that changes are not always driven by scientific goals, but sometimes technical/computing ones, for instance, replacing MantidPlot, as Qt4 lost support. We need to plan for how we perform and prioritise work that requires collective effort.

  Paolo mentioned a commitment of a certain number of Full Time Equivalents (FTE) from each facility. A cost-benefit analysis of priorities would complement this. Resources are currently provided by each facility as each requires. Pete said that he would be more comfortable having a firm commitment of the responsibility of each facility rather than FTE.

- Jon proposed that, with regards to governance, the PMB needs to make an educated guess and see if whatever new model is decided upon works.

##  2. What is wrong with the current governance??

- **It mentions the PMB, not the TSC and there is one overall PM. All agree that there should be a local PM for each facility with no overall PM.**

- We need the resources and headroom to plan for significant architecture changes. A review of how well this worked for Workbench would be useful. The move to creating Workbench didn’t run through governance, it just got done. 

  Workbench history: QT4 isn’t going to work going forward, generating a **report** with all possible options. Martyn wrote the first version of Workbench and consulted with the TSC at all points: e.g. architected for testing. And then afterwards all the other bits got filled out.
  Pas reiterated that **documenting decisions** is important to focus on overall science roles.

_Some disagreement over this next point, but generally agreed:_
- Developers are expected to find these future problems, somewhat unexpectedly. Having an overview of this in a management way isn’t possible. How do we detect future problems? We rely on the culture of the dev team to encourage horizon scanning for these future problems.

Many suggested, can we scrap this PMB, as the TSC should be running the project, without artificial hoops. Developers have the skills and drive to focus on the science ideas as well.

##  3. General Agreement

- _Generally, discussions continued around how to balance Computing vs Science priorities, especially for large cross-facility changes (e.g. Workbench)._

- Jon, Paolo and others mentioned the idea of a minimum requirement for being a member facility of the Mantid Project. Undecided what this would be, but for example: 1 TSC member and someone responsible to contact (effectively a local PM) from each facility.
- Toby, Stephen and Pas raised concerns over the lack of scientific input to the project roadmap. It was generally agreed that while the PMB should be scrapped it's members should become the new Steering Committee, which has a good balance of members from Scientific and Computing backgrounds, and is responsible for the 3-5 year Roadmap. The TSC is responsible for the work to be performed in the next 12 months.

- _While there was still some disagreement over whether the new Steering Committee should sit above or on the same level as the TSC_, it was initially agreed that the [diagram drawn out by Gagik](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/GovernanceModel.png) and [the related governance model](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/GovernanceModel.docx) was a good starting point for next time. The key feature that most promoted was the equal hieracrhy of the new Steering Commitee, the TSC (Technical Steering Committee) and the User Meeting. This basic model currently misses features such as requirements gathering and two-way feedback. 

##  Actions

- [ ] Each facility shoud prepare their internal roadmaps

 
##  Next Agenda:

- Discuss the responsibilites of each committee within the governance and, in doing so, answer [Jon's Questions](https://github.com/mantidproject/collaboration/pull/1#issuecomment-694769218).
- Run the new governance model past possible situations (e.g. Workbench) and determine how it would react. 
- Compare and merge Roadmaps
