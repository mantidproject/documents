#REFACTORING LOADER ALGORITHMS#

This document arose from an informal code talk I gave at ISIS on 29 July 2016.

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

* Functions have informative names that follow a naming convention
* Storage for data not immediately transferred to workspace needs to be justified

***Naming Convention***

A naming convention would make it clearer exavtly what a function does. For example:
* **Load...** read something and put it into workspace
* **Read...** read something and store in self
* **Put...** put something stored in self into workspace
* **Get...** return something stored in self
 
***Intermediate Storage Justifications***

These are possible justifications for use of intermediate storage, which could be put into comments.
* Storage for multiple uses (e.g. number of spectra may be needed to set up arrays for workspace).
* Data may need to be gathered from several places in file, before it can be put into workspace.
* Efficiency issues with large data.

**Could Haves (Future considerations)**

In thinking of ways to reduce the number of arguments of functions, 
I came up with the idea of having one or more classes to contain different data that travel together.
Then it would be possible to:
* Reduce number of arguments in functions
* Put all output into return value
* Create when needed and delete or let go out of scope when not needed
 
Such an object may contain appropriate pointers to large data and 
may have a function to put its data into the workspace. 
It may also reduce the need of a singleton helper, which would obsure the flow of data.

##Selected Use cases##

One example is a function of ``IsisRawHelper::readTitle(FILE *file, std::string &title)``.
This does more that just read the title. it reads the header of the file and outputs the title.
According to my suggested naming convention, it could be named
``IsisRawHelper::readHeaderAndGetTitle(FILE *file, std::string &title)``.

This long name, suggests it would be a good candidate to break up in functions that each do less.

##Proposed Solution##

* Rename function appropriately, using naming convention
* Break up functions that were difficult to rename or were given long names
* Move data away from algorithm or helper member variables
* Transfer data directly from file to workspace if possible and efficient, else
* Put data in temporary objects of appropriate scope and
* Group data travelling together into a object of a new (or existing) class

##Solution Details##

No details of solution at present. This can be worked out after the renaming has been done. 
The ranaming may give some useful hints to the details of the solution.

