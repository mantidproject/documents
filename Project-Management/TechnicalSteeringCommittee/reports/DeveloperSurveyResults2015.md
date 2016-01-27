##Summary##
The TSC circulated a survey to Mantid Developers in November 2015. The following are the common themes extracted from the free-text questions. The following includes the responses from 20 developers of varying experience across 3 facilities.

##Things that could be done to make day-to-day development easier##

* Information available on the wiki, but not easy to find (To be discussed at SSC)
* Not enough effort put into testing, causes problems down-stream (To be discussed at Workshop)
* Algorithms with exec functions that are far too large (many people highlighed this)
* Faster local builds (many people requested this)
* Faster unit test suites
* Larger list of historic PR packages. Really slows testing down when you have to build and package everything. Should keep packages until the PR is closed.
* More build servers.
* Properly isolating modules and tests so they can be run without  the rest of the code base. This is the soft-link issue.
* Developers forget to clang-format and then load the build servers when they fix it. Slows everything down.
* More spontaneous communication between facilities
* Macros for git commands
* Core framework now over-built. Hard to do seemingly simple things in Kernel/API.
* A chart explaining where things are in Mantid.
* More 'Concepts' in the code base co-located and properly separated. Not all geometry is in Geometry.
* Documentation from the physics point of view 

###Discussion###

1) Information available on the wiki, but not easy to find (To be discussed at SSC)
* Go through and clean the wiki every release/maintenance task. 
* Devs need permission to delete pages
* Feels like things related to development should be on the github wiki.
* Guide for GUI development is not a guide for GUI development.

2) Not enough effort put into testing, causes problems down-stream (To be discussed at Workshop)
* Review process should be done via gatekeepers.
* Triage step should be reintroduced. But needs to work faster. Probably easy to implement via labels.

3) Algorithms with exec functions that are far too large (many people highlighed this)

* Culture change required.

4) Faster local builds (many people requested this)

* Should be handled by TSC and code reorg.

5) Faster unit test suites

* Start enforcing limits on the long-running tests should be checked at PR
* Maintenance tasks should be done to go through long-running tests
* We need some way of logging spurious failing system/unit tests/doctests on master

6) Larger list of historic PR packages. Really slows testing down when you have to build and package everything. Should keep packages until the PR is closed.

* We need to pay for more space, or find ways to host these somewhere else. Would definitely be worth doing.
* Alternative is to have a manual job to create one-off packages based on a PR and platform

7) More build servers.

* Every facility should have at least one build server for the supported platform. 
* Run the system tests as a downstream job 
* Shrink system tests
* Split system tests (split the system tests across the same jobs)
* VMs shared across all facilities. What is the cost of this. Create images for all the VMs.


8) Properly isolating modules and tests so they can be run without the rest of the code base. This is the soft-link issue.

* Somehow handled by the code reorganisation

9) Developers forget to clang-format and then load the build servers when they fix it. Slows everything down.

* We should have a git pre-commit hook for clang-format. Would solve the amount of churn. We should also check the version.

10) More spontaneous communication between facilities

* Create more channels on Slack. 

11) Macros for git commands

* Working on forks may be made easier. Particularly pulling from another developers branch on their fork.
* This group is not entirely convinced of the value.

12) Core framework now over-built. Hard to do seemingly simple things in Kernel/API.

* Code re-organization issue
* Possibly go away with the triage step. Should see the Triage step as a direction for how to implement the fix.

13) A chart explaining where things are in Mantid.

* We might want to do this before the reorg
* This should definitely be done as part of the code reorganisation 


14) More 'Concepts' in the code base co-located and properly separated. Not all geometry is in Geometry.

* Code reorganisation.

15) Documentation from the physics point of view

* Developers are asked to refactor stuff that they don't understand. This doesn't always happen. 
* Encourage scientists to follow issues on Github
* Group meetings to inform people that interesting stuff is being worked on.
* Should notify instrument scientists (a) when stuff has been scheduled (b) a running estimate on when it's going to be ready.
* We need to have a live schedule communicated to the instrument scientists. This could be done per group.

##Area's developers highlighted as overly complex##

* Excessive use of Singletons
 * Stop using them  
* Workspace hierarchy 
 * Inheritance is highly overused
 * Do we have the correct base class ? (Probably not)
 * MatrixWorkspace is too bloated
 * Take MDWorkspace out of MatrixWorkspace
 * ExperimentInfo out of hierarchy
 * Look into how Qt (QVariant) deal with generic container types ?
 * Workspace type if tightly coupled to the data type it contains
  * Should some kind of data object be the place for variation (e.g. Histogram1D)
 * All workspaces should be able to contain multiple experiment info
* Function hierarchy 
* Adding new property types
 * See Owen's notes from Tuesday afternoon 
* Finding functionality already implemented (naming/location problems?) 
* Too many available algorithms, few of them core, some duplicated
* Instrument being very very complex
 * Dealt with as part of Geometry Rewrite 
* Geometry, understanding how it works particularly surface/object intersections
 * Dealt with as part of Geometry Rewrite 
* Parameter Map Leakage
 * Dealt with as part of Geometry Rewrite 
* Algorithms depending on the Analysis Data Service
* Workspace groups and the Analysis Data Service
* MantidPlot, ApplicationWindow a complete mess
 * What is the future of MantidPlot ?
 * Algorithms that depend on MantidPlot should be either re-written or moved out of Framework
* Bloated classes and methods for example Application Window, but there are many others.
* MantidPlot, 3D plotting 
 * VATES ?
 * Once we go to Qt5 - look at new Qt APIs
 * Matplotlib 
 * Needs to be scritable
* Fitting of anything other than 1D too hard to use
* AlgorithmProxies (do we need them?)
 * No we don't  
* Bloated interfaces, for example MatrixWorkspace
 * See above
* Units, presumably the distinction between Quantities and Units?
 * Already have actions to look into this 

##Other things we ought to worry about##

* Developer documentation is low-quality
* MantidPlot described as a horror, but a "mature/polished/bug-fixed horror"
* Some custom interfaces are too hard to maintain. How can we correct this?
* Algorithm options not well explained child/managed/unmanaged 
* We could use some examples of model Mantid code to help new developers (and old-hands too)
* Hard to find history after the code reorganisation 
* "It's overly complicated and demotivating to develop in Mantid. There are a tone of Python Packages that would cut the development by a factor of at least 10."
* I generally know enough of the instrument science, but not always to do my job
* Nexus file and logs "are a real nightmare"
* More examples where users can learn how to do things, like the Mantid training courses

###Discussion###

* Developer documentation is low-quality
 *     Induction material is fine
 *     Architectural design doc ok at a high level
 *     We are missing scientific technique overviews
 *     Missing some detailed design docs
  *     Development processes is fine
  *     Exposing objects to python could do with more docs / easier to find
  *     What packages to use for what & examples, e.g. xml, json
* MantidPlot described as a horror, but a "mature/polished/bug-fixed horror"
  *     The prime example of a missing design doc
  *     Is possible to extend, but the original design is too rigid
  *     Some of the worst examples of classes that are too long
  *     Not worth complete redesign for a 2nd choice tool of the future
  *     Future interfaces / gui aspects should be designed as widgets for use elsewhere as well
* Some custom interfaces are too hard to maintain. How can we correct this?
  *     Front end complexity, consider refactoring, consider a simpler interface (in addition)
  *     Back end complexity - refactor
  *     Web interfaces of the future, we need common design - Pilot
* Algorithm options not well explained child/managed/unmanaged
  *     Need to add to the dev documentation
* We could use some examples of model Mantid code to help new developers (and old-hands too)
  *     See suggestion in dev documentation
* Hard to find history after the code reorganisation
  *     Reorganise code less often
  *     Side point: Clang format tools resubmit after PR, can we have this automatically applied
* "It's overly complicated and demotivating to develop in Mantid. There are a tone of Python Packages that would cut the development by a factor of at least 10."
  *     Group view: It is complicated, is is not demotivating, in fact is is motivating.
  *     Hard for part time developers to keep up with changes
  *     Some areas are overly complicated without good reason e.g. mantidplot (more towards qtiplot + enhancements)
  *     Web: Django, D3
  *     General: Addition of a package is possible, but has to justify itself
* I generally know enough of the instrument science, but not always to do my job
  *     Instrument scientist generally happy to help
  *     Andre is a great local resource
  *     Ask who to check with within dev team, who the assigned inst scientists are.
* Nexus file and logs "are a real nightmare"
  *     Mantid shields many devs from this
  *     No real experince of this in group
  *     Not everything we will have to work is perfect
  *     Some cans of worms should remain unopened
* More examples where users can learn how to do things, like the Mantid training courses
  *     We have some "really old" examples, these are at best high level examples of the concepts
  *     Self paced courses available, and good
  *     However this more likely to be technique specific, in which case instrument specific instruction need to be created by instrument team.
