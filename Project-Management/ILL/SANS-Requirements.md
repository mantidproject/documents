## SANS Requirements

Could be that work done for HFIR at the SNS is most relevant - another reactor. Mathieu Doucet at the SNS knows most about this approach. For general information on SANS reduction in Mantid see [this document](http://docs.mantidproject.org/nightly/algorithms/SANSReduction-v1.html).

The SANS reduction works somewhat differently to [Time of Flight Spectroscopy](Time-of-Flight-Spectroscopy-Requirements.md), as every step is called within the workflow algorithm. For example, for D33 the two algorithms required for the initial reduction are [SetupILLD33Reduction](http://docs.mantidproject.org/nightly/algorithms/SetupILLD33Reduction-v1.html) and [SANSReduction](http://docs.mantidproject.org/nightly/algorithms/SANSReduction-v1.html).

Normally the algorithms listed below would not be called individually. However, for the purposes of comparing Lamp and Mantid they should be useful to be scripted separately. In the report by Wilcke some differences were noted between Lamp and Mantid, so the reduction steps will need to be broken down to determine where the differences occur.

An example of a D33 reduction script can be seen [here](https://www.ill.eu/fileadmin/users_files/documents/instruments_and_support/support_facilities/computing_for_science/data_analysis/process_data_final.py).

### General Algorithms Used

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| <sub> ? Read NeXus file |  <sub> |  <sub> [LoadILLSNAS](http://docs.mantidproject.org/nightly/algorithms/LoadILLSANS-v1.html) | <sub> Loads a ILL nexus files for SANS instruments.|  <sub> Currently only for D33 |
| <sub> sans_center | <sub> (check Lamp) Determine SANS centre and beam width (for Q resolution) from Direct beam |  <sub>  [SANSBeamFinder](http://docs.mantidproject.org/nightly/algorithms/SANSBeamFinder-v1.html)/[FindCenterOfMassPosition] | <sub> Beam finder workflow algorithm for SANS instruments./FindCenterOfMassPosition | <sub> In [SetupILLD33Reduction](http://docs.mantidproject.org/nightly/algorithms/SetupILLD33Reduction-v1.html) use `BeamCenterMethod="DirectBeam"`. SANSBeamFinder is a workflow algorithm to abstract the details of calling FindCenterOfMassPosition |
| <sub> sans_transm | <sub> (check Lamp) Calculate transmission values for sample and empty cell from transmission data (TD, TEC, TS) | <sub> [SANSDirectBeamTransmission](http://docs.mantidproject.org/nightly/algorithms/SANSDirectBeamTransmission-v1.html)/[ApplyTransmissionCorrection](http://docs.mantidproject.org/nightly/algorithms/ApplyTransmissionCorrection-v1.html) | <sub> Compute transmission using the direct beam method/Apply a transmission correction to 2D SANS data. | <sub> Similarly SANSBeamFinder, SANSDirectBeamTransmission is a workflow algorithm to make sure use of ApplyTransmissionCorrection. In [SetupILLD33Reduction](http://docs.mantidproject.org/nightly/algorithms/SetupILLD33Reduction-v1.html) use `TransmissionMethod="DirectBeam"`. |
| <sub> sans_tau | <sub> (check Lamp) Correct detector dead time (given formula for instrument) | <sub> Not present | <sub> | <sub> |
| <sub> sans_cor | <sub> (check Lamp) Subtract cell (EC) using transmission value as a function of scattering angle and monitor values & Correct for solid angle, sample thickness, parallax (instrument dependent) | <sub> (1) [SANSSolidAngleCorrection](http://docs.mantidproject.org/nightly/algorithms/SANSSolidAngleCorrection-v1.html),  (2) [NormaliseByThickness](http://docs.mantidproject.org/nightly/algorithms/NormaliseByThickness-v1.html) <sub> | <sub>  |
| <sub> sans_cor | <sub> (check Lamp) Absolute scaling | <sub> [SANSAbsoluteScale](http://docs.mantidproject.org/nightly/algorithms/SANSAbsoluteScale-v1.html) | <sub> Calculate and apply absolute scale correction for SANS data | <sub> Options for Mantid are Value and ReferenceData |
| <sub> sans_radial | <sub> Integrate data, 2D(QX,QY) – radial integration => I(Q) | <sub> [http://docs.mantidproject.org/nightly/algorithms/SANSAzimuthalAverage1D-v1.html](SANSAzimuthalAverage1D) | <sub> Compute I(q) for reduced SANS data | <sub> |
| <sub> sans_merge | <sub> Merge data, 1D(Q) – merge data covering different Q ranges | <sub> Not present | <sub> | <sub> |

### Interfaces

There are two interfaces available for SANS reduction, one is for ISIS and one for ORNL (HFIR/SNS). Lamp has a different approach, an editable spreadsheet showing all of the input data together. This may be desired in Mantid, so a decision will need to be made on using this against using the existing SANS reduction interfaces.

### SANS Requirements

1. Verify loaders are still compatible with current data
1. Compare beam centre finding algorithms
1. Compare transmission corrections
1. Investigate requirements for detector dead time calculations
1. Compare sans_cor in Lamp with SANSSolidAngleCorrection and NormaliseByThickness in Mantid
1. Compare radial integration between Mantid and Lamp
1. Find or create a Mantid equivalent to sans_merge
1. Finalise workflows for
 * D33
 * D11
 * D22
1. Interface
 * Determine requirements for interface, create mockups
 * Implement interface, making as much use of existing ISIS and ORNL interfaces as possible

