# Mantid 4 libraries and names

* Users have difficulty finding algorithms/objects
* Reorganize imports
* Rename algorithms
    - a lot of the information is where you import the algorithm from
    - `CalMuonDeadTime` becomes `mantid.muon.CalculateDeadTime`
    - `Get...` returns a value (number, string, array, ...)
    - `Calculate...` returns a workspace
    - `Correct...` applies the calculation to the input workspace
    - use http://www.mantidproject.org/Mantid_Standards#Naming
    - no length restriction
    - no abbreviations
* Remove unused algorithms

---

# Mantid Libraries (current framework) 

* mantid.io
    - all loading and saving
* mantid.math 
    - matrix workspace math (also include `V3D`, `VMD`, ...)
    - `Plus`, `ExponentialCorrection`, `Rebin`, `Fit`
    - many algoritm names in this library will not contain a verb `Plus`, `Minus`
    - add aliases `Add`=`Plus`, `Subtract`=`Minus`
* mantid.math.axes
    - changing the axis of a matrix workspace (not the data), that is technique independent
    - `TransformX` (previously `ScaleX`, `ChangeBinOffset`, `ConvertAxisByFormula`), `GetMedianBinWidth` (former `MedianBinWidth`)
* mantid.math.events
    - deals with events (technique agnostic)
    - `FilterEvents`, `RebinByPulseTime`
* mantid.math.instrument
    - grouping, masking, etc
    - include `Instrument`, `Goniometer` objects
    - `GroupDetectors`, `MaskBankTubePixel` (currently `MaskBTP`), `SetGoniometer`, `MoveInstrumentComponent`
* mantid.math.multidimensional
    - technique agnostic multidimensional workspaces
    - `mantid.math.multidimensional.Rebin`(`BinMD`/`SliceMD`)
    - does not include `ConvertToMD`
* mantid.metadata
    - logs, title, but not history
    - `AddLog` (instead of `AddSampleLog`), `CorrectLogTimes`
* mantid.muon
    - muon related stuff
    - `CalculateAsymmetry` (instead of `AsymmetryCalc`)
* mantid.neutrons
    - things that are related to neutrons (time of flight), but not specific to a certain subfield (like diffraction)
    - `ConvertUnits`, `ConvertToMultiDimensionalWorkspace` (`ConvertToMD`), 
    - `NormaliseByProtonCharge` (`NormaliseByCurrent`), `Correct3HeTubeEfficiency`(`He3TubeEfficiency`)
* mantid.neutrons.crystal
    - single crystal stuff. Will include `UnitCell`, `OrientedLattice`, `SymmetryOperation`
    - `SetUB`, `FindPeaksReciprocalSpace` (`FindPeaksMD`), `IndexPeaks`
* mantid.neutrons.diffraction
    - powder/amorphous diffraction stuff
    - `StripVanadiumPeaks`, `AlignAndFocusPowder`
* mantid.neutrons.inelastic
    - algorithms related to both direct and indirect inelastic spectroscopy
    - `GetIncidentEnergy` (`GetEi`), `CorrectKiKf`, `CalculateDynamicStructureFactor` (`SofQW`)
* mantid.neutrons.reactor
    - single wavelength algorithms
    - right now most are facility specific
* mantid.neutrons.reflectometry
    - `FindReflectometryLines`
* mantid.neutrons.sans
    - `CalculateEfficiency`
* mantid.constants
    - no algorithms here
    - physical constants
    - neutronic constants
* mantid.remote
    - `SubmitRemoteJob`, `AbortRemoteJob`
* mantid.workspace
    - manipulate workspaces, history
    - should we move all workspace objects here?
    - `RenameWorkspace`, `GroupWorkspaces`, `CompareWorkspaces`, `AddCommentToHistory` (`Comment`)
* mantid.api
    - the current mantid.api (workspaces, validators, algorithm)
    
---

# Facility Specific Libraries

* mantid.ess
* mantid.hfir
* mantid.ill
* mantid.ral (or mantid.isis)
* mantid.sns
* can add instrument or technique specific sublibraries
    - `mantid.sns.corelli.CrossCorelate`
    - `mantid.sns.directinelatic.GetIncidentEnergy`

---

# Other Changes

* Move things from mantid.kernel (mostly to mantid.math or mantid.api)
* Move things from mantid.geometry (mostly into mantid.math.instrument)


