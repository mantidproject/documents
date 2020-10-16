#  Minutes

##  Mantid PMB Meeting 20

**Minutes of: 2020-10-16 UTC+1 12:00-14:00**

**In Attendance:**
```
* CSNS - (absent)

* ESS - Jon Taylor (usually PMB Chair)

* ILL - Miguel Gonzalez, Paolo Mutti, Gagik Vardanyan

* ISIS - Lamar Moore (co-PM), Toby Perring (acting chair for this meeting), Pascal Manuel

* ORNL - Mathieu Doucet, Andrei Savici

* Non-facility - Peter Peterson (co-PM + TSC chair), Stephen Cottrell (User Group Chair), Daniel Murphy (Secretary)
```
##  Agenda
- Discuss the responsibilities of each committee within the governance and, in doing so, answer 
  [Jon's Questions](https://github.com/mantidproject/collaboration/pull/1#issuecomment-694769218).
- Run the new governance model past situations (e.g. Workbench) and determine how it would react.

##  1. Initial Governance Model plans and how this relates to local governance

Started discussing the governance model diagram drawn up by Gagik, to which Jon added the local scientific steering 
committees. On the diagram is was clarified that the local PM feeds back to the TSC.
Toby mentioned that the directors should be included on this.

Lamar presented a slide demonstrating the plans for how local ISIS governance works with 
the international governance model. This involved a more balanced approach to feature requests with more 
involvement from science groups and maintaining the future features within the ISIS Mantid Programme Board.
Due to the balance between Technical and Science motivations, local representatives should be informing 
a Science Roadmap, and a Technical Roadmap, which are to be owned by the Steering and Technical Steering Committees
respectively. The steering committee will involve people from both science and technical background. 

Toby mentioned that the tension/balance between the technical and scientific demands give accountability for discussing
the practical resources required for each feature request. Jon agreed that this is quite a robust model.

Pete and Jon discussed how gaining feedback from the user meeting gain feedback can rely on its set-up and can sometimes
be simply a way of spreading information.

##  2. [Jon's Questions](https://github.com/mantidproject/collaboration/pull/1#issuecomment-694769218)

### *Q1 How do partners collaborate and contribute?*

Lamar: It's much better to work in projects to measure what you're contributing to. This allows for resource management
, with a defined end-point and scope.
Toby: If 2 facilities want to do something rather similar but not identical (e.g. SANS reduction in ISIS and SNS)
, how would this be managed?
 
Lamar said that Roadmaps are useful for identifying commonalities.
Paolo liked the project approach but wants a way to not duplicate work in different facilities.
Lamar said that with an understanding of the broader picture of each facilities' future projects, it will be possible to
to zoom out and understand whether common projects can work.
Toby pointed out that simply the timing of different projects can be a barrier to collaboration work
between different facilities. This depends on how flexible internal facility roadmaps can be.

Pete, Andrei and Mathieu mentioned that we need buy in from the instrument scientists. In a recent project, they had
scientists working closely with the development team, including at daily stand-ups. This scientists were able to be 
involved with writing user stories and tests. This required a lot of nudging of scientists. 
Involvement of managers has been helpful, in terms of getting this scientist engagement and deadline setting.

There were some short discussions around how much the engagement of management / directors is useful for the 
collaboration. While ISIS have suggested an infrequent directors meeting, Pete warned that directors may
want the benefits, but none of the commitment / work. 

Following this, there were many (initially Mathieu) that expressed the idea that the specific value of Mantid to each 
facility must be sold to their directors (possibly in a one page [glossy / flashy] briefing that could come before 
the directors' meeting).


### *Q2 How does the development workflow run ?...*

The structure mentioned in the Governance model diagram handle this, with local committees also, in a project focussed
manner.

### *Q7 Significant architecture changes handled, planned, executed*

Paolo recommended FTEs for resourcing these significant architecture changes.
Lamar said as a collaboration, they could define a common project and allocate resources on this basis.

Pete discussed how dealing with technical debt is only possible if you can give someone (managers / stakeholders)
a good reason why it should be worked on. This is only the case when that debt visibly impedes
the current goals. This reasoning helps to explain why it is worthwhile removing effort from other
tasks. Trying to sell fixing technical debt when it is not visible or really related to their work, is very hard.

Gaining FTE commitment from management would only be possible if these benefits could be explained for each individual
facility. Also, this needs to be linked to something that directors understand. A project-style focus could aide this.

Paolo agreed with all this, but thinks that if there is a common core project, then that will require cross-facility 
buy-in and it should not be dealt with by one facility, this makes things fair, and helps to spread the knowledge.
Workbench effort was roughly 60-70% from ISIS.

Pete mentioned that even though every facility didn't participate equally in making Workbench, it was still important 
for each one to communicate the need for workbench within their facility.

### *Q3+4 What group is responsible for release schedules? What group is responsible for quality and functionality?*
TSC

### *Q5 What group is responsible for requirements and scientific direction?*
Overall governance model handles these competing motivations.

##  Actions

- [ ] On Lamar, to consolidate the discussions of the last few meetings and fleshing out the responsibilities of 
      each committee into a coherent document for review. Circulate in ~2 weeks time and it can be discussed before
      the next meeting in ~3 weeks (6th November 2020). 

 
##  Next Agenda:

- [ ] Discuss Lamar's fleshed out responsibilities for each committee 
- [ ] Anything else related to Jon's questions?
- [ ] Prepare for review in December.