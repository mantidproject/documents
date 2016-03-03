##Scope of Work##

The following the first-draft of the high-level [requirements](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md) approval on 22nd January 2016, an inital set of activies where identified to form the first milestone. 

###Activities Requested###

Protypes and reports requested

| Action        | Who           |
| ------------- |:-------------:| 
| What functions are called through Geometry. What are the questions we need to ask of the system     | O.Arnold |
| What questions are users/instrument scientists going to ask of the Geometry outside workspace/algorithm related calculations     | O.Arnold  |
| Scanning addition prototype. How bad will the performance be the event-based time positioning be?     | M.Gigg |
| Investigate standards for binary file formats for the IDF HDF5/VTK etc | P.Peterson & A.Savici |
| Investigate how other projects, namely [McStas](http://www.mcstas.org/download/components/) and [McVine](https://github.com/mcvine/resources/blob/master/instruments/ARCS/resources/ARCS.xml) describes complex components | O.Arnold |
| Prototype routing the l1 and l2 fetching via a vector. Try eagerly populating the vectors. What is the effect on performance for one or more of our system tests. A second step may be to determine the cost of invalidating/recalculating the l1 and l2's. | O.Arnold |

##Internal Geometry Use-cases##

This section aims to answer what high-level geometry related requests are made within Mantid. We are specifically looking at instrument related geometry usage.
 
| Request        | Example |
| ------------- | --------- |
| Component position fetch   |  
| ...   | 
TODO O.Arnold

##External Geometry Use-cases##

This section aims to answer what are instrument scientists currently accessing via geometry? What do they need to access in future?
TODO O.Arnold

##Scanning Instrument Prototype##

TODO M.Gigg

##Binary Formats##

TODO A.Savici/P.Peterson

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

[McVine](http://www.mcvine.org/) is part of the [DANSE](http://wiki.danse.us/danse/index.php?title=Main_Page) project. McVine uses [DANSE](http://wiki.danse.us/danse/index.php?title=Main_Page) [Instruments](http://dev.danse.us/trac/instrument) schema is elaborated upon in the [User Guide](http://dev.danse.us/trac/instrument/wiki/xml-userguide#Copy). Schema allows the use of DANSE [pyre](https://github.com/danse-inelastic/pyre/tree/master/python/pyre/units) units.


####Noteable Features####

* Handling of units. Lengths can be specified in different units for example [here](https://github.com/mcvine/resources/blob/master/instruments/ARCS/resources/ARCS.xml#L368)
* Handling of copied components explained [here](http://dev.danse.us/trac/instrument/wiki/xml-userguide#Copy)
* Visitor pattern used to avoid excessive specification of things related to geometry.For example separation of drawing from the base respresentaion. See [here](http://dev.danse.us/trac/instrument)
* McVine has the concept of a _Geometer_, used for example [here](https://github.com/mcvine/resources/blob/f461af477d119fe6ba9667d06d08569335ab25d1/instruments/ARCS/resources/ARCS.xml#L222) to specify a local coordinate system independent from that of parent components. This is just a way of specifying positions  relative to their parent components.
* Schema looks slightly better constructed to that used in the current IDF version of Mantid.

###Ideas not to take forward###

* The Mantid `ReferenceFrame` described [here](http://docs.mantidproject.org/nightly/concepts/InstrumentDefinitionFile.html#using-defaults) seems like a more flexible concept than the `LocalGeometer` `coordinate-system` used in McVine

###Ideas to take forward###

* Components in v2 geometry could solve the flight-path problem for say guides, but allowing each component to specify a `length`, which may be a derived value, but would default to zero. This might suit arbitrarily complex componnents such as non-linear guides
* The concept of Copy components from McVine seems nice
* The concept of units has been discussed, McVine handles this. How this could be done in Mantid should be investigated. Maybe Boost::Unit would be suitable.
* Separation of display information from the geometry information should definitely be looked at seriously. Example being a non-linear (parabolic etc) guide. Specifing its neutronic `length` may be sufficient for the data analysis, but we want something to look representative and good via the displays (Instrument View)
* We do not want to loose the  `LocalGeometer` (as known by McVine) or relative component aspects used in Mantid. This flexibility has been shown to work well, performance is an issue we'll have to get around.
* No system seems to have broached the affine transformation as a function of both _logs_ and _position of other components_ requried. We shall refer to this feature as __Geometry and Log Algebra__
* We should be able to _Chain_ components together. This should not depend upon the order of declaration. This would allow for example a non-linear guide above to be made of say a composite of mirrors. We should be able to mark `Components` with some sort of `source-component` metadata. Such a linked-list would describe a chain. I suggest we do this in addtion to allowing each component to express it's length.

##Detector L2 Cache##
See [issue] where caching has been applied (https://github.com/mantidproject/mantid/issues/15501) 
