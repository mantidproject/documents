#REFACTORING LOADER ALGORITHMS#

##Motivation##

I've been working on decomentating how data from a file (usually a Nexus file) is read by a loader 
and is transferred to a workspace. I have found it difficult to do. 
If the code for the loaders was cleaner, I'd expect to easily see how each item of data
goes from file to workspace and so easily produce a table such as the one 
[here](http://docs.mantidproject.org/nightly/algorithms/LoadISISNexus-v2.html#data-loaded-from-nexus-file)

**Current Situation**

Loaders often have:
* Long Loader Class
* Member variables (behave like global variables)
* Long functions
* Functions with many arguments
* Functions that do too much
* Functions with misleading names

Other features that impair readability are:
* Intermediate storage of data outside of workspace
* Use of static functions in singleton helper

##Requirements##

**Must Haves**

* Functions have informative names
* Storage for data not immediately transferred to workspace needs to be justified

**Could Haves (Future considerations)**

Add a numbered list of things that the design *could* address but it would not be vital to cover

##Selected Use cases##

Add a selection of use cases

##Current Structure##

If the design addresses a current issue then briefly describe the current solution to the problem

##Proposed Solution##

Summarize the proposed solution

##Solution Details##

More detailed sections on proposed design

