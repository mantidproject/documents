# Updated estimate of SANS rewrite

## Table of Contents
1. [Development phases (and summary) of the initial estimate](#phase_original)
2. [Development Phases of rewrite](#phase_rewrite)
3. [Time spent on rewrite](#time)
4. [Comparison of original estimation with time spent on rewrite](#comparison)
5. [Reevaluation of estimate](#reeval)

This document aims to provide a updated estimation of what has been described
in the [initial estimation](Estimate_SANS_Rewrite_original.md).
 For the current workplan, please see [here](../SANS_rewrite_workplan.md)

<a name="phase_original"></a>
## Development phases (and summary) of the initial estimate

The old estimation had two scenarios:
  1. A parallel implementation
  2. A gradual implementation

Finally, a parallel implementation was chosen, since this would allow us to
remove bad elements of the reduction more easily as well as not restrain our
design decisions.

The development phases were:

<a name="point_1"></a>
* **State Object and work-flow handler**
 * 4 - 6 w
<a name="point_2"></a>
* **Reduction Workflow Algorithms and General Reduction**
 * SliceEvent: 1-2 w
 * CropDetBank: 1-2 w
 * MaskISIS: 3-6w
 * UnitsConvert: 1-3d
 * NormalizeToMonitor: 1.5-3w
 * TransmissionCalc: 3-5w
 * AbsoluteUnitsISIS: 0.5d
 * SampleGeomCorr: 1w
 * ConvertToQ: 1-1.5w
 * CanSubtraction: 1w
 * StripeEndNans: 1-2d
 * General-Reduction: 3-5w
* **GUI**
 * 2-4m
* **Python Interface**
 * 3.5 -5.5w
<a name="point_5"></a>
* **Batch mode**
 * 2-5d
* **Adding files**
 * 1-2d
* **Beam Centre Finder**
 * 3-5w

Note that this initial estimate is missing time for the design and the time
required for loading and moving the data.

<a name="phase_rewrite"></a>
## Development phases of rewrite

The listed development phases of the initial estimate differ from how the
current rewrite is being executed. This is mainly due to the conclusions which
were drawn from the design phase.

The development phases and their equivalent are drawn out below:

* **Phase 0: Design**
  * This was not taken into account in the initial estimates
* **Phase 1: Establish SANSState mechanism and loaders**
  * This corresponds to [**State Object and work-flow handler**](#point_1) in the initial estimate.
  * The loaders (and movers) were not taken into account in the initial estimate,
  but are developed in this phase.
* **Phase 2: Create the skeleton for reduction**
 * This corresponds to *General-Reduction* and *StripEndNans* in [**Reduction Workflow Algorithms and General Reduction**](#point_2)
 and [**Batch mode**](#point_5) in the initial estimate
* **Phase 3: Provide individual reduction steps**
  * This corresponds to all reduction steps in [**Reduction Workflow Algorithms and General Reduction**](#point_2)
* **Phase 4: Python Interface**
  * Same as in initial estimate
* **Phase 5: Integration into Beam Center Finder**
  * Same as in initial estimate
* **Phase 6: GUI development**
  * Same as in initial estimate

<a name="time"></a>
## Time spent on rewrite

The unit is days (=7.5h)

| Phase  | April   | May  | June  | July  | Total
| -------| -------| ----- |-------| ----- |-------|
| Design | 3.93    | 3.9  | 0.0   | 0.0   | 7.83      |
| Phase 1| 0.0     | 4.0  | 12.73 | 4.2   | 20.93     |
| Phase 2| 0.0     | 0.0  | 0.0   | 4.13  | 4.13      |
| Phase 3| 0.0     | 0.0  | 0.0   | 3.8   | 3.8       |


<a name="comparison"></a>
## Comparison of original estimation with time spent on rewrite

#### Phase 1

Time spent so far: 20.93d

The expected time from the initial estimate is 4-6w from [**State Object and work-flow handler**](#point_1). The intial estimates
did not account for the loading files and moving workspaces.

###### Achievements so far:
* Developed SANSState mechanism which allows passing structured python data
  into an algorithm.
* Developed `SANSLoad` algorithm which handles the different types of files and
allows for cached loading (i.e. from the ADS)
* Developed `SANSMove` algorithm which allows for the correct instrument-dependent
initital move, a set-to-zero move and a elementary displacement
* Developed state information for `SANSLoad` and `SANSMove`
* Developed UserFile parsing system which is considerably more robust.

###### Things left to do:
* Needs gradual updating when more sub-states of the individual reduction steps
are added.
* Need to implement loading of added data (required interface is in place)

#### Phase 2

Time spent so far: 4.13d

The expected time from the initial estimate is 3-5w for *General-Reduction* in [**Reduction Workflow Algorithms and General Reduction**](#point_2),
1-2d for *StripEndNans* in [**Reduction Workflow Algorithms and General Reduction**](#point_2) and 2-5d from [**Batch mode**](#point_5) . This is a total of 4-6w.


###### Achievements so far:
* Developed `SANSBatch`
* Developed `SANSSingleReduction`
* Developed *StripEndNans*

###### Things left to do:
* Add more tests when reduction steps in Phase 3 are added
* Fix some bugs I am aware of now

#### Phase 3

Time spent so far: 3.8d

The expected time  from the initial estimate for elements which have been
 completed (*SliceEvent* and *CropDetBank*) is 2-4 w.
The expected time  from the initial estimate for the currently worked
on item (*MaskISIS*) is 3-6w.
The expected time  from the initial estimate for the remaining elements is
completed (*SliceEvent* and *CropDetBank*) is 8-11 w.

###### Achievements so far:
* Developed `CropWorkspaceToComponent`
* Developed `SANSSliceEvent`
* Developed/ing `SANSMask`

###### Things left to do:
* Complete work on `SANSMask`
* Implement comparison tests that evaluate reduction chain up to masking
* Implement remaining reduction steps

#### Other phases

No work has been done yet on the other phases

<a name="reeval"></a>
## Reevaluation of estimate


| Phase  | Original Estimate     | Time taken        |  Ratio     |
| -------|----------------------|------------------|------------|
| Phase 1| 4 - 6w                |  ~ 4w             |   0.7 - 1  |
| Phase 2|                       |                   |    -       |
| Phase 3|                       |                   |    -       |
| Phase 4|                       |                   |    -       |
| Phase 5|                       |                   |    -       |
