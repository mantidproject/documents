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


##Area's developers highlighted as overly complex##

* Excessive use of Singletons
* Workspace hierarchy 
* Function hierarchy 
* Adding new property types
* Finding functionality already implemented (naming/location problems?) 
* Too many available algorithms, few of them core, some duplicated
* Instrument being very very complex
* Geometry, understanding how it works particularly surface/object intersections
* Parameter Map Leakage
* Algorithms depending on the Analysis Data Service
* Workspace groups and the Analysis Data Service
* MantidPlot, ApplicationWindow a complete mess
* Bloated classes and methods for example Application Window, but there are many others.
* MantidPlot, 3D plotting 
* Fitting of anything other than 1D too hard to use
* AlgorithmProxies (do we need them?)
* Bloated interfaces, for example MatrixWorkspace
* Units, presumably the distinction between Quantities and Units?


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
 *     induction material is fine
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
