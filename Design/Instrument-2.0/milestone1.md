##Scope of Work##

The following the first-draft of the high-level [requirements](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md) approval on 22nd January 2016, an inital set of activies where identified to form the first milestone. 

###Activities Requested###

Many of these are questions to unknowns:

1. What functions are called through Geometry. What are the questions we need to ask of the system. (Owen Arnold)
1. What questions are users/instrument scientists going to ask of the Geometry outside workspace/algorithm related calculations. Example: beam shape at component. (Owen Arnold)
1. Evaluate user geometry use cases (Tim Charlton / Owen Arnold)
1. Scanning addition prototype. How bad will the performance be the event-based time positioning be? (Martyn Gigg)
1. Investigate standards for binary file formats for the IDF HDF5/VTK etc (Pete/Andrei)
1. Investigate how other projects, namely [McStas](http://www.mcstas.org/download/components/) and [McVine](https://github.com/mcvine/resources/blob/master/instruments/ARCS/resources/ARCS.xml) describes complex components (Owen Arnold)

##How Other Projects Describe Components##

###McStas###

Uses the *.comp file format to describe components and *.inst files to assemble components into an instrument. Components are generally not nested. Components may be extended via __EXTEND__ , but typically only at the instrument level, otherwise the document suggest copying the component into a local directory and making changes there.

####Noteable Features####

* Components separation of `Parameters` from `Display`
* `Components` have input and output `Parameters`
* `Display` geometry specified via `MCDisplay`
* Instruments declare variables that are accessible to all components, and may, for example be used in positioning.
* Use of `RELATIVE` and `PREVIOUS` keywords when describing positions via `AT`
* Predicates available to control positions based on other parameters. For example using _WHEN(%PREDICATE%)_

###McVine###

####Nice Features####

###Ideas###

* Components in v2 geometry could solve the flight-path problem for say guides, but allowing each component to specify a `length`, which may be a derived value, but would default to zero. This might suit arbitrarily complex componnents such as non-linear guides
* 

