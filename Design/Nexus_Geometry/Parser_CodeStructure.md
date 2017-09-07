# Code Structure for parsing OFF Nexus Geometry

The code structure for parsing OFF Nexus Geometry, creating an instrument and adding to the workspace is made up of 3 parts:

## 1. The load algorithm

This is kept separately as `LoadNexusGeometry` in _Framework/DataHandling/_.  In future, it will likely be incorporated into the current `LoadNexus` algorithm.
`LoadNexusGeometry` will be responsible for calling and handling errors created by `ParseNexusGeometry`.  It will also load the instrument created by `ParseNexusGeometry` to a workspace.  In future this workspace will also be loaded with the data contained in the Nexus File.

## 2. The OFF Instrument Definition Parser

`ParseNexusGeometry` will be a class responsible for parsing the OFF instrument definition contained within the Nexus File.  It will be given a reference to an instance of an `InstrumentAbstraction` class.  
`ParseNexusGeometry` will read the instrument definitions from the Nexus file, and use the `InstrumentAbstraction` methods to add detectors, components etc. to an instrument.  Upon completion the `InstrumentAbstraction` object will be returned to `LoadNexusGeometry`.

The parser will be based on a previously written class, which can be found [here](https://github.com/ScreamingUdder/cpp_nexus_utilities).

## 3. The Instrument Abstraction Class

### The need to abstract the instrument interface

The current Instrument interface is being replaced by Instrument 2.0.  It is possible to use the Instrument 2 interface to read from any Instrument 1 objects, but not yet possible to create an instrument through it.  Therefore any code which has to create an instrument will have to do so through the old interface, but will be updated in future to use Instrument 2.

In order to limit the number of changes that will have to be made, the `InstrumentAbstraction` class will be created to provide a common interface to both Instrument 1 and Instrument 2.

### Implementation

`ParseNexusGeometry` and `InstrumentAbstraction` will be placed in a new directory in _Framework/NexusGeometry_.  The interface will be implemented through compile-time polymorphism, using [CRTP](https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern).

This will require an aditional class to be written, which will implement the abstraction functions for Instrument 1.  This will be placed in _Framework/Geometry_.  When the switch to Instrument 2.0 is made, the abstraction class will be placed in _Framework/Beamline_.

## Code

The code is being implemented in the [screamingUdder/mantid](https://github.com/ScreamingUdder/mantid) repository, and all changes will be merged into the feature branch [NexusGeometry](https://github.com/ScreamingUdder/mantid/tree/nexus_geometry).
