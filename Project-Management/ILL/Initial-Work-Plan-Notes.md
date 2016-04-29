## Startup Activities
* [C++ new starter exercise in Mantid](http://www.mantidproject.org/New_Starter_C%2B%2B_introduction) - approximately 5 days
* Skype code review with other developers for the C++ exercise
* Go through the [Mantid training course](http://www.mantidproject.org/Documentation) self-paced - approximately 2 - 3 days
 * [Mantid Basic Course](http://www.mantidproject.org/Mantid_Basic_Course)
 * [Introduction to Python](http://www.mantidproject.org/Introduction_To_Python) - very basic, only needed for anyone not familiar with Python
 * [Python in Mantid](http://www.mantidproject.org/Python_In_Mantid)
 * [Extending Python with Mantid](http://www.mantidproject.org/Extending_Mantid_With_Python)
* Read the [Architecture Design Document](https://github.com/mantidproject/documents/blob/master/Design/ArchitectureDesignDocument.doc)
* Meetings with scientists in technique areas each person will be working on

## Project Related Activities

During the day to day development some time will be required for reviewing pull requests from the wider Mantid project. In turn, our own pull requests will be reviewed by the wider team.

Official Mantid releases happen every 4 months. At these times a couple of days of manual testing will be required by developers for manual testing. Post release developers at the ILL will need to take up a couple of weeks to work on maintenance tasks for the project too.

## General Approach for Any Technique Area

These are the approximate steps required for any technique area.

* Understand the workflow in LAMP. Talk to computing group and instrument scientists to understand how the workflows work, including any shortcomings.
* Understand the workflow in Mantid. System tests is a good place to start for these, then existing members of the Mantid team will need to be identified for more details or examples of different workflows.
* Understand what is going on under the hood in Mantid. It will be important to understand the process of any workflows in Mantid. This will help identify any changes required for the ILL.
* Demos of the runs in Mantid should be shown back to the instrument scientists. In this way they can help identify any potential shortcomings or issues with Mantid.
* Find the new features that ILL will require in Mantid. This will require clarification with instrument scientists as well as other members of the Mantid team, to try and avoid implementing any features that already exist.
* Implement features required in Mantid. This should be done in close collaboration with instrument scientists to ensure the new techniques are implemented correctly. The focus here would be implementing the algorithms, not adding the GUI.
* The Mantid results will need to be verfied. These will most likely normally be done against LAMP. Any large discrepancies should be understood, and the correct behaviour determined.
* Add a GUI interface if desired, and work on any other usability issues.

Each technique area will vary in the breakdown of time for different tasks, depending on work already done and new requirements in Mantid. These tasks will also work in iterative cycles to a certain extent, for example during validaiton new requirements may be found. 

A breakdown of work on these areas might look something like the following:
* 25% - Evaluate LAMP and Mantid
* 15% - Define new requirements
* 20% - Implementation of new algorithms
* 20% - Results validation
* 20% - GUI interface

## Scanning Instruments

Separate document to be created on this. See [this document](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for more information on requirements.

## Time of Flight Spectroscopy

ISIS and SNS take two different approaches. ISIS relies mostly on Python scripts while the SNS use workflow algorithms. The SNS approach is more likely to be the one to follow.

Tasks:
* Evaluate what exists in LAMP and Mantid
 * Look at both SNS and ISIS workflows to determine which is the most useful approach
 * See if any extra work is required on the loaders - e.g. with configence levels, check format of NeXuS files
* Create requirements document for missing features
 * This will require working closely with instrument scientists at ILL
* Implement missing features
 * This will require working closely with instrument scientists at ILL
* Evaluate Mantid results against LAMP and resolve any major discrepancies

Relevant contacts are Alex Buts at ISIS and Stuart Campbell at SNS.

General Algorithms Used

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| rdsum |read and sum sample runs | (1) Load/LoadILL and  (2) MergeRuns | (1) Loads a ILL nexus file. (2) Combines the data contained in an arbitrary number of input workspaces. | Loaders exist for IN4, IN5 and IN6 already. Gives identical results to Lamp, but requires start and end points for each channel. |
| normalise | Normalises data to monitor or counting time. This should always be the first routine called after reading in the data. | NormaliseToMonitor | Normalizes a 2D workspace by a specified spectrum, spectrum, described by a monitor ID or spectrun provided in a separate worskspace. | No normalisation by time currently exists. |
| remove_spectra | Removes suspect spectra from a workspace. | MaskDetectors | In Mantid the spectra for the masked detectors are zeroed. In Lamp the unwanted spectra are removed completely. In Mantid the three monitor detectors are included in the workspace. Offsets aside, these results are otherwise identical. |
| vnorm | Normalises data to vanadium. | NormaliseVanadium | Normalises all spectra to a specified wavelength. | Small discrepancy in normalaisations found by Wilcke. |
| cylindercor | Absorption correction for annular cylinder | [CylinderAbsorption](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption)* | Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | No comparison has been made of these yet. |
| slab_tof | Takes a 2-D time-of-flight workspace and corrects for sample attenuation of the scattered neutrons assuming slab sample geometry.  | [FlatPlateAbsorption](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption)* | Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | No comparison has been made of these yet. |
| corr_tof | Corrects data in TOF for energy-dependence of detector efficiency, frame overlap and time-independent background. | DetectorEfficiencyCorUser | This algorithm calculates the detector efficiency according the formula set in the instrument definition file/parameters. | These are not identical between Lamp and Mantid, despite DetectorEfficiencyCorUser attempting to replicate the Lamp behaviour. |
| t2e | Transforms time-of-flight data to energy transfer h &#969;. | ConvertUnits(Target='DetlaE') | Performs a unit change on the X values of a workspace. |  The Lamp algorithm performs three steps - convert to dE, correct for Ki/Kf, correct for dT/dE. Mantid treats these separately, but does not have a separate dT/dE correction. The dT/dE correction seems to be done in the SofQW step in Mantid. Without the corrections in Lamp t2e and ConvertUnits are identical. |
| t2e - Ki/Kf | In Lamp Ki/Kf is part of t2e algorithm. | CorrectKiKf | Performs k_i/k_f multiplication, in order to transform differential scattering cross section into dynamic structure factor. | A small difference was found between Lamp and Mantid, which is proporitonal to the counts. |
| sqw_rebin | Rebins data to regular-grid S(Q,&#969;) covering the entire measured Q-E region | SofQW | Computes S(Q,&#969;) using a either centre point or parallel-piped rebinning. | Some minor differences exist here. See report by Wilcke for more information on the comparison. |

* Note that CylinderAbsorption and FlatPlateAbsorption both inherit from the more general method [AbsoprtionCorrection](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection). 

Instrument Specific Algorithms

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| in4strip ||||

## Time of Flight Spectroscopy - Event Mode

The second block of 6 months is intended to focus on event mode data collection.

## Backscattering

A lot of work has already been implemented in Mantid for IN16b by Elliot Oram with help from Spencer Howells. Hence the time required on this should be relatively short, and much of it will focus on filling in any gaps.

## Powder Diffraction

This will likely be different from anything used currently in Mantid. A variety of people have some knowledge of this, Nick Draper, Martyn Gigg, Pete Peterson, Shahroz Ahmed and Federico Pouzols.

## Liquid Diffraction

May require implementation of absorption/multiple scattering corrections - Paalman-Pings currently in Mantid.

## Strain Scattering

Talk to Federico Pouzols.

## SANS

Could be that work done for HFIR at the SNS is most relevant - another reactor. Mathieu Doucet at the SNS knows most about this approach.

## Time of Flight - Reflectometry

SNS are starting to move towards the ISIS way of doing this. Useful contacts for this are Owen Arnold, Raquel Alvarez and Matt King.

## Live data analysis

Mantid already has the listener to fill the workspace, better suited to events. At ISIS there is a simple TCP/IP port with a buffer. SNS have something more sophisticated which can pick up from, for example, the beginning of a run. Here events are streamed from files.
