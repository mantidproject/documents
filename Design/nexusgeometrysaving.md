## Overview

Version 4.0 of Mantid saw the introduction of the Nexus Geometry Format [updates](https://docs.mantidproject.org/v4.0.0/release/v4.0.0/framework.html#nexus-geometry-loading) into Mantid. This has gone well with, many of our tests showing speed improvements upon loading for a range of equivalant instruments (Rectangular Detectors excluded) and no loss of functionality or performance for the existing routes.

ESS intend to support the new geometry format for intermediate files because:

1. The format has been demonstrated to suit the representation of neutron instrument geometries well
1. It is relatively low-cost for the ESS to adopt as part of an intermediate format.
1. It gives a common format for geometry for Raw and Processed files
1. It is complete and accurate. The current approach bypasses serialization.
1. It is not application specific, geometries are useable in downstream applications more easily.

This is a follow up to the Working Group Meeting 20/06/2019. We are aware that ISIS do not intend to make use of the new format. The positions of the SNS and ILL were not represented at that time.

We are currently running a small project involving a student to provide a saving mechanism within the existing the lib [NexusGeometry](https://github.com/mantidproject/mantid/tree/master/Framework/NexusGeometry) to provide a high-level function to support the saving.

**This document is for discussion of the best way to make these features available within Mantid**

## 1. Implicit Replace instrument_xml in `SaveNexusProcessed`

This represents an implicit change in behaviour.

Current mechanism [implemented here](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/src/Instrument.cpp#L1010), would be replaced (see notes below) to use the new method in `NexusGeometry`. This would mean that ALL new processed nexus files contained the full geometry rather than the xml string. Aligned with that, we would also remove the instrument geometry specific parameters i.e. the things representing overloads to the correct position.

It would be recommended to retain the switch that allowed us to write old-style processed nexus files but the default would be to have the new-style files written out. The switch would be exposed as a parameter on the algorithm.

Reloading the files should work without any modifications, `LoadInstrument` already does the right thing.

**Pros**

1. Users do not need to be aware that this change is happening - they have enough to think about
1. Provides a useful modernisation update to Mantid across the facilities

**Cons**

1. Potential for breaking changes higher. Though we thoroughly test, and naturally would be very thourough prior to introduction of this feature - there is a danger of problems slipping through and affecting users.
1. Files written in newer Mantid versions wont work with v < 4 by default. 
1. I'm not aware of anyone inspecting the `instrument_xml` directly in the output file, but this would be harder (see Nexus Constructor Tool)
1. There would be a loss of instrument parameters as described. I'm not aware of anyone using these, but they would dissapear.
1. Harder to compare versions between files.

## 2. Explicit Replace instrument_xml in `SaveNexusProcessed`

Same as above, but with the default to be writing out old-style files and opt-in for new format.

**Pros**

1. Potential for breaking changes low.
1. Easy to compare files between versions of Mantid without thinking

**Cons**

1. Users need to be made aware of the switch
1. Users would not necessarily take advantage of this. More of a pain at facilities like ESS where the default would be to adopt.
1. Once parameter defaults have been set, very hard (almost impossible - see LoadInstrument rewrite spectrum map) to change them. 


## 3. Side-by-Side Algorithms

Refactor such that the common code of SaveNexusProcessed (most of it) is in a shared class/module. Keep `SaveNexusProcessed` exactly as it is and introduce a new algorithm which saves the new format.

**Pros**

* Users do not need to be aware of defaults at the property level for new usage
* No breaking for old scripts

**Cons**

* SaveNexus is a natural name for what we want to do in both cases
* Takes more time to refactor and create new algorithm

## Notes on the Instrument Service 

The instrument service allows Mantid to cache instruments and prevent reload. Both the `InstrumentDefinitionParser` and the `NexusGeometryParser` have hash mechanism to compare instruments based on content and therefore prevent uncessary reload.
