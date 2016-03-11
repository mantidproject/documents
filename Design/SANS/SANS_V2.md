# SANS Work Flow Algorithm Port Estimation

## Motivation

The SANS reduction workflow makes use of the so-called `ReductionSingleton`, which essentially handles the configurational state of the reduction. It stores this state information either directly in itself, in an `ISISInstrument` object or so-called reductions steps. The individual reduction steps can also extract information from the `RedcutionSingleton`. This causes the reduction steps to be deeply coupled to the `ReductionSingleton`, which makes it hard to unit test them (and probably explains why such tests do not exist). In addition there is a strong coupling of the `ReductionSingleton` to the GUI logic, which essentially makes the ISIS SANS reduction a monolithic block.

A more modern approach is to use Mantid WorkflowAlgorithms. This mechanism avoids the deep coupling. Individual algorithms are supplied with the required workspaces and additional configurational information. They return an adequate output workspace. This setup naturally allows for simple unit testing.

## Current status

Besides being fairly monolithic and largely untested, there are several concerns which have been repeatedly raised by the instrument scientists:
* speed
* and excessive memory consumption

A brief investigation of these two issues is presented below.

For the rest of this document it is beneficial to point out the core elements of the data reduction (in this order):

*TOF Domain:*
1. *SliceEvent*<a name="SliceEvent"></a>: Converts an EventWorkspace into a Workspace2D
  * Main algorithm: Rebin
2. *CropDetBank*<a name="CropDetBank"></a>: Crops the workspace such that it only contains the spectra of the "current" detector
  * Main algorithm: CropWorkspace
3. *MaskISIS*<a name="MaskISIS"></a>: Excludes times and detectors
  * Main algorithm: MaskBins, MaskDetectors, MaskDetectorsInShape
4. *UnitsConvert*<a name="UnitsConvert"></a>: Converts the units to wavelengths (with additional rebinning)
  * Main algorithm: ConvertUnits

*Wavelength Domain:*
5. *NormalizeToMonitor*<a name="NormalizeToMonitor"></a>: Selects the incident monitor and subtracts the flat background.
6. *TransmissionCalc*<a name="TransmissionCalc"></a>: Uses transmission and direct workspaces to calculate the transmission.
  * Main algorithm: CalculateTransmission
7. *AbsoluteUnitsISIS*<a name="AbsoluteUnitsISIS"></a>: Scales part of the cross section calculation.
8. *SampleGeomCorr*<a name="SampleGeomCorr"></a>: Corrects for the volume of the sample
  * Main algorithm: ConvertUnits

*MomentumTransfer Domain:*
9. *ConvertToQ*<a name="ConvertToQ"></a>: Performs the cross section calculation. Takes the output of [*NormalizeToMonitor*](#NormalizeToMonitor) and [*TransmissionCalc*](#TransmissionCalc) and evaluates them in *CalculateNormISIS* (not a reduction step).
  * Main algorithm: Q1D and Qxy
10. *CanSubtraction*<a name="CanSubtraction"></a>: Performs steps 1 to 9 for the Can and subtracts the result from the intermediate Sample result.
11. *StripEndNans (for 1D)*<a name="StripEndNans"></a>: Strips off front and end of the final output workspace if NANs are present.


#### Profiling speed

Speed profiling was performed using the a SANS2D H2O data set (4 Runs). (The results are not too useful, since we should be looking at 100s of runs to get meaningful results. Nevertheless they indicate that we are not confronted with prominent bottlenecks.) The percentage of the mean total process time for each reduction step is shown below.

|Reduction Element                               |H2O:|Mean(%)| Std(%) |
|------------------------------------------------||--------|----------|
|Preprocessing                                   || 0.2    | 0.3      |
|[*SliceEvent*](#SliceEvent)                     || 5.2    | 2.1      |
|[*CropDetBank*](#CropDetBank)                   || 6.2    | 1,1      |
|[*MaskISIS*](#MaskISIS)                         || 7.4    | 0.7      |
|[*UnitsConvert*](#UnitsConvert)                 || 7.4    | 0.3      |
|[*NormalizeToMonitor*](#NormalizeToMonitor)     || 2.9    | 0.7      |
|[*TransmissionCalc*](#TransmissionCalc)         || 8.3    | 3.3      |
|[*AbsoluteUnitsISIS*](#AbsoluteUnitsISIS)       || 2.1    | 1.1      |
|[*SampleGeomCorr*](#SampleGeomCorr)             || 1.4    | 0.5      |
|[*ConvertToQ*](#ConvertToQ)                     || 4.7    | 4.1      |
|Preprocessing Can                               || 0.8    | 0.6      |
|[*SliceEvent Can*](#SliceEvent)                 || 2.8    | 2.6      |
|[*CropDetBank Can*](#CropDetBank)               || 6.8    | 3.4      |
|[*MaskISIS Can*](#MaskISIS)                     || 8.8    | 0.9      |
|[*UnitsConvert Can*](#UnitsConvert)             || 8.3    | 1.1      |
|[*NormalizeToMonitor Can*](#NormalizeToMonitor) || 2.1    | 0.4      |
|[*TransmissionCalc Can*](#TransmissionCalc)     || 9.4    | 1.4      |
|[*AbsoluteUnitsISIS Can*](#AbsoluteUnitsISIS)   || 2.8    | 0.6      |
|[*SampleGeomCorr Can*](#SampleGeomCorr)         || 1.4    | 0.6      |
|[*ConvertToQ Can*](#ConvertToQ)                 || 6.1    | 5.0      |
|Acutal Can Subtraction                          || 2.5    | 0.4      |
|[*StripEndNans*](#StripEndNans)                 || 1.1    | 0.6      |
|PostProcessing                                  || 1.3    | 0.4      |

This preliminary profiling shows that the current workflow is not directly hindered by any obvious bottlenecks, i.e. there are no outliers when it comes to runtime. It is not immediately obvious that a rewrite could improve this situation.

#### Investigation memory usage

Memory consumption when running the ISIS SANS reduction is fairly large since small event-mode files are converted to potentially very large histogram-mode files in the very [first reduction step](#SliceEvent).

The first few (non-converting) steps [*CropDetBank*](#CropDetBank), [*MaskISIS*](#MaskISIS) and [*UnitsConvert*](#UnitsConvert) don't seem to require the data in histogram form in principal. [*CropDetBank*](#CropDetBank) performs, in addition to extracting the current detector bank, a dark background correction. This dark background correction subtracts dark background values in the time domain from the sample workspaces. For this to work, the data is required in a histogram-mode format.

One possible workaround would be to allow only event-mode dark background workspaces and to add the dark background event-mode workspace as negative events.

The next reduction steps in line, [*NormalizeToMonitor*](#NormalizeToMonitor) and [*TransmissionCalc*](#TransmissionCalc), require the data to be in histogram mode. Hence we can potentially push back the conversion of the event-mode workspace to a histogram-mode workspace to about the fifth reduction step.

#### Reloading data

Another source of performance waste occurs when certain files are loaded multiple times during the reduction process, although the newly loaded file is identical to the old one. Note that this issue of redundant file loading is being addressed independently of a [here](https://github.com/mantidproject/mantid/issues/5106)).

Loading of "Data Files" and "Tube Calibration Files" are the main culprits. There are two strategies which could minimize redundant loading:
* Keep track of the modification status of loaded files, i.e. workspaces. If they have not been modified by the user or by the reduction algorithms, then there is no need to reload them. This requires a tracker object which is queried and updated whenever a load-request is performed. Loading will then occur at the recommendation of this tracker. The tracker itself will have to rely on the workspace history to determine the modification status of a workspace.
* Load files once and create working copies for individual reduction runs. Presumably it is much quicker to create a clone of a workspace than to reload it from a file. This will however incur a memory penalty which might be prohibitive (depending on the size of the workspace).

While the first strategy is definitely something we should implement, it would require a more careful investigation of current memory issues within the SANS workflow to determine if the second strategy is feasible at all.

###### Data Files

Data Files (SANS, Transmission, Direct) are loaded by the user before the reduction starts. During loading, the instrument associated with the workspace is displaced using the algorithms [*MoveInstrument*](http://docs.mantidproject.org/nightly/algorithms/MoveInstrumentComponent-v1.html) and [*RotateInstrument*](http://docs.mantidproject.org/nightly/algorithms/RotateInstrumentComponent-v1.html).

The data files are then reloaded once again when the user requests a reduction. Applying the first strategy mentioned above, could reduce the processing cycle for a reduction quite a bit.

###### Tube Calibration Files

The tube calibration files are loaded whenever the user file is being parsed. After a reduction finishes the user file is being parsed in order to provide a fresh setup of the `RedcutionSingleton`. This also means that the calibration files are being loaded. When the data files are being loaded they transfer instrument parameters to the calibration file. This happens only if the parameter is absent in the calibration file.

The first strategy mentioned above could provide some relief here. Since common calibration files are on the order of 50MB currently, it might still be worth considering the second strategy.

## SNS effort

A similar port has been performed at SNS by M.D. When asked about the time it took him to perform the port he provided the following insightful answer:

>...the re-write took me a good 6 months. But that included a re-write of the Reducer (ReductionSingleton), which still exists but is now only used to process the convenience commands that our users use.

>The main obstacle was to manage the reduction options, which was previously done in the Reducer. I chose to use a PropertyManager class, which is set up by SetupEQSANSReduction. That allows me to use the convenience commands to set up the reduction, then pass the PropertyManager to the SANSReduction algorithm. I’m not necessarily convinced that this is the best design, but it works well.

>The long and painful part of the work, once I decided on the design, was to port all the corrections to independent workflow algorithms. This might take you a little longer, since the ISIS code is a little more monolithic than ours. I had already gone through the exercise of separating all the corrections a couple of years prior to moving to the workflow algorithms. I ended up having to write system tests that exercise all the parameters of every correction to make sure that the results were the same. That’s why there are so many system tests for ORNL SANS.


## Parts which need to be redesigned for the port
Minimal change set:
  1. State object: It is likely that all parts of the SANS reduction need an altercation to some degree. The most significant step and the first one to worry about is to decouple the reduction steps from the `ReductionSingleton`. This will require us to develop a sensible state object and interface definitions. Ideally the state object should be easily manipulated from the `C++` and the `Python` side. At this step we will already be touching all reduction steps.

  2. Reduction Workflow Algorithms: The reduction steps will have to be ported to equivalent algorithms. This is a good opportunity to establish unit tests and performance test suites for the individual reduction steps. In principal this would also be the time to address performance issues.

  3. GUI: The GUI, even if we leave it unchanged on the surface, will need considerable effort to remove the coupling to the `ReductionSingleton`. Having a state object might allow us to setup everything on the GUI-side without having to query the `Python`-side. (although it is not clear how we could achieve input validation?)

  4. `Python` interface: The new workflow principle will have to be incorporated to the `Python` commands which are exploited by the SANS power users. Currently the `Python` interface requires the user to perform a sequence of commands which essentially stores state information in the `RecutionSingleton` and the reduction steps before executing. In order to guarantee backwards compatibility we might require a dummy-Singleton object which carries and populates a state object. (Python Commands v2 might also be an option)

  5. Batch mode: The batch mode file relies on the reduction itself. Once the points above have been addressed, it should be not too difficult to make the necessary changes in the batch file.

  6. Adding files: This is already decoupled and requires only minor changes.

  9. Beam Centre Finder: This element is heavily coupled to the `ReductionSingleton` and the `ISISInstrument`. It might make sense to create a workflow algorithm out of the Beam Centre Finder itself (see also [here](https://github.com/mantidproject/documents/tree/sans_beam_centre_finder_design_document/Design/SANS)).


Additional GUI change (optional):
As mentioned above, the internals of the GUI, will have to be touched during this rewrite, even if the GUI-skeleton stays untouched. Nevertheless it might be beneficial to port the GUI itself (or rather a 2.0 version) to `Python` which would avoid the complicated communication between the `Python` and `C++` logic.

### Expected work description:

#### V1: Gradual implementation

With a gradual implementation approach we try to introduce our new design bit by bit. It is continuously integrated into the current implementation of the SANS reduction. The advantage of this is that we will always have a working version of ISIS SANS available. The disadvantage that we could be restricted (at least in part) by old design decisions.

 1. State Object and decoupling:
    * Define adequate data structure for the state object. (1w).
    * Have the `ReductionSingleton` populate the state object instead of its own containers, the `ISISInstrument` and the reduction steps. This means we need to hollow out the reducer methods (and potentially some of the `ISISInstrument` methods). This is the most important part of the port and also the one which is mostly likely to have unexpected outcomes. Virtually all steps below, rely on the work which is being done here. (10-15w).

 2. [Reduction Workflow Algorithms](<a name="step2"></a>)
    * [SliceEvent](#SliceEvent): This algorithm currently depends on instrument information and slice limits which is available from the `RedcutionSingleton`. (1-2w)
    * [*CropDetBank*](#CropDetBank): The cropping part itself should be straightforward (1-2w) This reduction step also hosts the dark background subtraction, which  is already completely decoupled and tested.
    * [*MaskISIS*](#MaskISIS): This reduction step contains a lot of state settings and is in fact one of the most complex steps we currently have. It makes heavy use of the
    `RedcutionSingleton` and the `ISISInstrument`. In addition it is being used outside of the regular reduction chain, in the context of the mask tab in the ISIS SANS GUI. (3-6w).
    * [*UnitsConvert*](#UnitsConvert) This should be simple since the coupling should have been removed at the point we start to work on this item (1-3d).
    * [*NormalizeToMonitor*](#NormalizeToMonitor): Looking at this item, it seems to contain several instrument-dependent settings which might cause an issue during the port. (1.5-3w)
    * [*TransmissionCalc*](#TransmissionCalc): This is a complex algorithm with quite a few configurational options. It is considered one of the more difficult algorithms to port. (3-5w)
    * [*AbsoluteUnitsISIS*](#AbsoluteUnitsISIS): Simple (0.5 d)
    * [*SampleGeomCorr*](#SampleGeomCorr) : Provided the reduction step is already decoupled, it should be fairly simple (1w)
    * [*ConvertToQ*](#ConvertToQ): The main logic is already in `C++` and tested. The `Qresolution` part is already decoupled and tested as well. (1-1.5w)
    * CanSubtraction: There should be no surprises. (1w)
    * [*StripEndNans*](#StripEndNans): Should be easy (1-2d)
    * General Reduction: In addition to the actual reduction steps we need to have a workflow algorithm which drives the reduction, similar to the currently used [`WavRangeRecution`](https://github.com/mantidproject/mantid/blob/master/scripts/SANS/ISISCommandInterface.py#L372) : This function is rich in logic and drives which detector bank should be used for the reduction. (3-5w)

 3. GUI:
    * Once the `ReductionSingleton` is essentially hollow and only hosts a state object, we should get rid of it in the GUI. We need to find a good way to populate the state object from the GUI. (2-4w)

 4. Python interface:
    * Provide a new singleton host which does virtually nothing except for setting the state object. (3-5w)
    * Leave `WavRangeRecution` as a facade and use workflow algorithms in the background. (3d)
    * OR: create a script translator for legacy scripts and define a new way of writing SANS `Python` scripts

 5. Batch mode:
    * Make use of new reduction workflow (2-5d)

 6. Adding Files:
    * Only minor changes (1d), but we might want to wrap up in own algorithm and test better (2d)

 7. Beam Centre Finder:
   * The Beam Centre Finder will require a significant rewrite and potentially a packaging in a workflow algorithm (3-5w)


Adding up the estimates results in (37-58w) or roughly (9-12m).

Additional GUI change:

  * Porting the GUI from `C++` to `Python` is most likely a large task. The time spent on this would be largely dependent on the additional user requirements. A simple port itself could be (2-4m)

#### V2: Parallel implementation

A parallel development of SANS would in many ways be easier at the beginning since we would have less work regarding the decoupling. But later stages of the development would be slightly harder, since we would like to reuse old code which most likely contains coupling. This means that we cannot avoid the decoupling effort.

1. State Object and decoupling:
   * Define adequate data structure for the state object (1w)
   * Define a workflow algorithm which handles the entire reduction (2-3w)
   * Define interfaces for GUI and reduction steps (now workflow algorithms) (1-2w)
2. These steps are similar to steps [2](#step2) above. It is expected that the  implementation would take longer in this case, since we would like to reuse the reduction steps as much as possible. This would require us to perform the decoupling work in this step instead of in the previous step.

3. Identical to above.
4. Identical to above.
5. Identical to above.
6. Identical to above.
7. Identical to above.

The same work and estimates apply to an optional GUI development.

#### Conclusion

The two approaches are slightly different and require certain work to be done at different times of the development cycle. Nevertheless it appears that roughly the same work is required in the end, hence it is expected to take a similar time (9-12m).
