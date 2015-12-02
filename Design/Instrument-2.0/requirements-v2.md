Suggestions and Requirements for Future Features
================================================

##Motivation##

The current instrument geometry matched the requriements in the early programme lifecycle. We have subseqently retrofitted the geometry as more instruments and more facilities joined the project. This has worked well, but we have several major issues to solve for which a deeper and thourough rexeamination of the existing implementation is required. Firstly, experimental setup is becoming increasingly complex, and we need a virutal instrument that can model the real experimental setup. Secondly, the performance demands are now much greater than orignally designed for, particularly with the live-reduction challenge forethcomeing at the ESS. Thirdly, the current syntax for describing instruments is not as logical or straight forward as it ought to be, and encourages instrument related errors in the reduced data.

##High-level Functional Requrements##

###Mandatory###

* Existing funcitonality listed [here](https://github.com/mantidproject/documents/blob/Instrument-Geometry/Design/Instrument-2.0/features-v1.md) should be preserved.
* The design should simplify the process of directing and configuraton from the current experiment (Instrument control).
* The design should allow for complex beam paths, where components may order themselves to create the l1 & l2.
* Any new schema should allow for thorough validation to detect any logical errrors, for example, avoiding component collision
* Instrument parameter syntax should be richer, particularly when labelling and applying multiple functions to components.
* Any new schema should be more cohesive and self-describing than the current system
* The design should be optimized for reads, not for writes, since the former is much more frequent. See non-functional requriements.
* The design should allows for Moving instruments. For this it might be useful to separate things into two different concepts: (1) positions/rotations of spectra/event-list (2) detectors with no position/rotation information.
* The design should allow for **tagging** of components with an extendable list of attributes. This would include the existing detector, monitor, sample. This would avoid these tags having to be applied at the instrument level.
* Instruments should have better concept of allowed translations. A work around to this has been found in ISIS SANS.
* Algebra for positions based on log values should be supported. For example setting the source height based on the incident theta log value. Currently this cannot be done without using hard-coded displacements.

##Desired##
* The design should make it easy for laser scans to be imported. Components may be marked with 0-n referecnce markers.
* In file formats, definitions should be a first-class citizen, not just a textual representation.
* As far as possible geometry should be shared with instrument control, particularly in terms of instrument definitions.
* It should be possible to port v1 definitions to v2.

##Performance Non-functional Requriements and Technical Specifications##

### MPI

Especially for ESS, Mantid will most certainly need to be run on a cluster based on MPI.
Currently, one promising model is distributing work by splitting the instrument and assigning a subset of the detectors to each MPI rank.
We can either keep the complete instrument on each rank and only assign the relevant events/spectra, or actually keep only a part of the instrument.

* Keeping the full instrument might lead to memory problems, given that ESS has instruments with up to 10 million voxels.
* If we keep only parts of the instrument, the design of the instrument/geometry code should put no restrictions on how the subsets are defined (various subset definitions might be necessary for different instruments). For example, it must be necessary to split up something like a `RectangularDetector`.
* Splitting does not necessarily need to be compatible with visualization: Splitting is relevant for an MPI run of Mantid on a cluster, where we cannot have a GUI anyways.
* The option to redistribute an instrument might be an advantage. Basically this wold require an instrument design that allows for adding and removing/transferring components without breaking existing workspaces.

### Performance as a (Non-functional Requirement)

It is hard to put down a precise performance requirement.
We can try to do a worst-case analysis, based on various guessing:

* In the current SANS reduction run we observed up to 30% time spent in instrument/geometry related code.
* The detectors at ESS will have non-negligible depth that might require more complex geometry calculations.
* Voxel detectors will spread out the events that would normally be registered in a single pixel to several voxels, potentially yielding an additional factor.
* We hope to do some optimization work on various other parts of Mantid, so we should take into account that the non-geometry related parts will speed up.

Depending on the precise circumstances that may change very little, or could easily imply >80% time in instrument/geometry related code.
In the latter case we would ideally like to have at least a factor of 10 speedup.

* At a later point it might turn out useful if we managed to keep the underlying data layout flexible: In case we need to do some very expensive geometry calculations we might want to resort to vectorization (SIMD), which often works best with an SOA (structure-of-arrays) data layout instead of a AOS (array-of-structures) data layout. This flexibility is not a strong requirement at this point, just a nice-to-have.

### Threading

The current design implements a series of mechanisms to make modification of an instrument thread-safe.
I (Simon) cannot think of a use-case where this actually makes sense: Modifying an instrument while another thread is reading does always seem to lead to race conditions at the macro level, even if things on the micro level are thread safe (I may be overlooking something, please correct me if you can think of a realistic and useful counter example).
Thus:

* Instrument/geometry should be thread-safe for reading.
* Modifying an instrument does not need to be thread-safe.

Basically, I currently think that the requirements here should be the same as for the containers in std (C++11), such as std::vector.
