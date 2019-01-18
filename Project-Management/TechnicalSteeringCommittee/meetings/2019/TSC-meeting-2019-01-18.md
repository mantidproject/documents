Fri 18th Jan 13:58:44 GMT 2019

## Attendees

- Owen Arnold
- Dan Nixon
- Martyn Gigg
- Lamar Moore
- Simon Heybrock
- Ross Whitfield
- Steven Hahn
- Andrei Savici
- Peter Peterson

## Original Agenda

This is the second TSC related meeting to discuss outputs from [PMB action](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2018-01-31.md#resourcing-of-the-core-team)

You will need to be familiar with the [proposal](https://github.com/mantidproject/dataset/pull/4) hence the advanced warning of this meeting. As we will be discussing this in depth, you should not attend if you do not understand what is being proposed.

**1. Evaluation of Design**
At this point we are NOT discussing plan or resourcing.
* Do you like the design. All obstacles ignored – would you like to see this realised in Mantid? 
* What specific feedback do you have regarding the updated design (NOT the plan or resourcing)

**2. Evaluation of Proposed Plan**
At this point we are NOT discussing resourcing.
* Do you have any specific feedback on the work-breakdown-structure and flow according to the updated plan? Does the proposed plan look to be prioritised correctly?
* Are there interdependencies or problems that have been missed?

**3. Informing Resourcing**
Resourcing is not the primary concern of the TSC so I would not like to see it discussed at length here. However:
•	Are you satisfied that the estimates attached to the plan are realistic.
•	At an individual level, would you be interested in monitoring and providing feedback on this ongoing development?

## Major Discussion Points

1. No issues with technical aspect of design. Highlighted that a large number of frameworks are now converging on this type-erased x-array approach (x tensor etc).
1. How is "better reflect the science" PMB requirement addressed?
   - Multiple runs, closer to experiment
   - Motivations for users (& PMB)
   - What science use cases will be benefited?
   - Was agreed to address this in the design document
1. Disucssion on whether it would be better to use/participate in/contribute in other projects?
   - Reduce Mantid developer time required
   - (xtensor, xframe)
   - Opportunity to collaborate with early stage projects
1. Martyn raised point about greenfield vs brownfield development
   - Existing functionality
   - Good for "new" project
   - All existing functionality to accommodate into dataset
1. Discussion naturally moved to [implementation path](https://github.com/mantidproject/dataset/blob/design-update/doc/design.md#implementation-path) following Martyn's comments.
   - Implementation stages (see latest design document)
     - Phase 1
       - Standalone package
       - Converters to/from workspace types
     - Phase 2
       - Science/technique supporting features
       - Implement technique workflows
       - +WB: implement Mantid Workbench support (flexible)
   - Dataset is not a direct replacement for traditional workspaces
     - Converters allow mixing workspaces and dataset in workflows
     - Dataset support not added to existing algorithms
1. Make scale of "rewrite" clear
   - Not just worksapces
     - Also algorithms, MD?, GUI
   - Will "legacy" workspaces (and algorithms) ever disappear?
   - Simon highlighted that this was deferred to a latter phase in the plan to allow the learning in earlier phases to inform the decision. Can implement stages 1 and 2 without making a decision on long term support
. Simon and Owen currently favour a non-breaking rollout, i.e. explicit porting needed.
1. Simon highlighted there would be no benefit to touching/refactoring existing algorithms/framework. Drew parallel to Dataset as MDWorkspace equivalent, different non-compabitible data structure with bespoke algorithms `PlusMD` etc.
1. Major discussion around how to show worth
   - Martyn suggested smaller scope with larger problem workflow
   - ESS plan to use DREAM as demo workflow
     - Difficult with current Mantid
   - Compare current and potential workflows to show significant benefit
   - Show something that does not work well in current Mantid
     - HB2A
     - NOMAD (total scattering)
1. Pete suggested separate approval of design (concept) from approval/decision of roll-out. This was agreed.
    - No issue approving technical design of concept after this is done
    - Split document will with concept + motivation (better science addressed) will go to 
1. Too early for demo at developer meeting?
    - Good to do user (developer) testing early
    - Really need workflow demo to prove dataset is worth implementing
    - Suggested that this should go ahead. This is for API steering forming part of the evaluation. This is not seen as a beta for something for the next release.

## Actions
1. Simon Heybrock: Split design document into "Concept" and "Rollout"
1. Owen Arnold: Andrei Savici: Add "support better science" to "Concept" and send "Concept" document for next TSC meeting (**January 2019**)
1. Simon Heybrock: Prepare for API steering session at developer meeting (**April 2019**). This fits with the [PMB request](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2018-01-31.md#resourcing-of-the-core-team) to have something ready to demostrate at the next Developer Meeting
1. Implement workflow in dataset. Nomad suggested as key information for PMB. Comparisons to existing Mantid need to be made. Initial people added to this task Andrei Savici, Owen Arnold, Simon Heybrock. Not clear yet exactly what is involved.


