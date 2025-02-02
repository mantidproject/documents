## Startup Activities
* [C++ new starter exercise in Mantid](http://www.mantidproject.org/New_Starter_C%2B%2B_introduction) - approximately 5 days
* Skype code review with other developers for the C++ exercise
* Go through the [Mantid training course](http://www.mantidproject.org/Documentation) self-paced - approximately 2 - 3 days
 * [Mantid Basic Course](http://www.mantidproject.org/Mantid_Basic_Course)
 * [Introduction to Python](http://www.mantidproject.org/Introduction_To_Python) - very basic, only needed for anyone not familiar with Python
 * [Python in Mantid](http://www.mantidproject.org/Python_In_Mantid)
 * [Extending Python with Mantid](http://www.mantidproject.org/Extending_Mantid_With_Python)
* Read the [Architecture Design Document](https://github.com/mantidproject/documents/blob/master/Design/ArchitectureDesignDocument.doc)
* Look over some training materials from neutron training courses
 *  [ISIS Neutron Training Course](http://www.isis.stfc.ac.uk/learning/neutron-training-course/downloads/neutron-training-course-downloads9156.html)
   * See Neutron Training Course Manual
 * [14th Oxford School on Neutron Scattering](http://www.oxfordneutronschool.org/2015/Lectures/teaching%20materials_2015.htm)
   * Practical Neutron Scattering
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

See [Time of Flight Spectoscopy Requirements](Time-of-Flight-Spectroscopy-Requirements.md).

## Time of Flight Spectroscopy - Event Mode

The second block of 6 months is intended to focus on event mode data collection.

## Backscattering

See [Backsacttering Requirements](Backscattering-Requirements.md).

## Diffraction

See [Diffraction Requirements](Diffraction-Requirements.md).

## Strain Scattering

Talk to Federico Pouzols.

## SANS

See [SANS Requirements](SANS-Requirements.md).

## Time of Flight - Reflectometry

See [Reflectometry Requirements](Reflectometry-Requirements.md).

## Live data analysis

Mantid already has the listener to fill the workspace, better suited to events. At ISIS there is a simple TCP/IP port with a buffer. SNS have something more sophisticated which can pick up from, for example, the beginning of a run. Here events are streamed from files.
