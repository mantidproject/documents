##Summary##
The TSC circulated a survey to Mantid Developers in November 2015. The following are the common themes extracted from the free-text questions. The following includes the responses from 20 developers of varying experience across 3 facilities.

##Things that could be done to make day-to-day development easier##

* Information available on the wiki, but not easy to find (To be discussed at SSC)
* Not enough effort put into testing, causes problems down-stream (To be discussed at Worshop)
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
