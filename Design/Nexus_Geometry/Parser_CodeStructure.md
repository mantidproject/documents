# Code Structure for parsing OFF Nexus Geometry

The code structure for parsing OFF Nexus Geometry, creating an instrument and adding to the workspace is made up of 3 parts:

## 1. The load algorithm

This is kept separately as `LoadNexusGeometry` in _Framework/DataHandling/_.  In future, it will likely be incorporated into the current `LoadNexus` algorithm.
`LoadNexusGeometry` will be responsible for calling and handling errors created by `ParseNexusGeometry`.  It will also load the instrument created by `ParseNexusGeometry` to a workspace.  In future this workspace will also be loaded with the data contained in the Nexus File.

## 2. The OFF Instrument Definition Parser

`ParseNexusGeometry` will be a class responsible for parsing the OFF instrument definition contained within the Nexus File.  It will be given a reference to an instance of an `InstrumentAbstraction` class.  
`ParseNexusGeometry` will read the instrument definitions from the Nexus file, and use the `InstrumentAbstraction` methods to add detectors, components etc. to an instrument.  Upon completion the `InstrumentAbstraction` object will be returned to `LoadNexusGeometry`.

## 3 The Instrument Abstraction Class
