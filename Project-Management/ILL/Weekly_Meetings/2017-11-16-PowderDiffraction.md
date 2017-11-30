## Meeting notes - 2017/11/16 - Powder diffraction meeting

Participants: Gagik Vardanyan, Antti Soininen, Verena Reimund, Miguel A. Gonzalez, Franck Cecillon, Paolo Mutti, Thomas Hansen, Gabriel Cuello

### Gagik: Powder diffraction reduction for D20

See [slides](2017-11-16-PowderDiffraction.pdf) for more details.

Goals completed include:
 * Refactoring of the calibration algorithm, with improvements in code organization and speed.
 * Interpolation of overlapping 2-theta angles.
 * Implementation of option to normalise data using the number of counts in a detector ROI.
 * Fix exclusion regions for calibration.

Points discussed:
 * Best way of grouping measured diffraction patterns (typically as a function of temperature):
   1. The rebin algorithm can be used for this, but it is not well adapted.
   1. Decided to write a new algorithm (GroupPointData?) to combine patterns inside a range and return the average pattern and the average temperature (or adequate variable: pressure, magnetic field, etc.). On first approximation, all patterns can be equally weighted. However if data have been taken using different measuring times, a more refined weighting scheme would be needed.
 * Best way of selecting the scanning observable: Agreed to have a combo box with a limited list of usual variables and a final option 'Other' allowing to introduce any name existing in the sample logs, e.g. 'sample.temperature', 'Omega.Position', etc.
 * Detector scan reduction: Given the many common steps shared between the detector calibration and reduction, during the meeting it appeared that the prefered option would be to have a single algorithm with two different options: 'Produce Calibration' and 'Reduce'. However, later discussions taking into account D2B as well, have lead to decide that it is better to have two different algorithms.
 * How to identify bad cells in ambiguous cases. It has been found that a few cells count often 0, but not always. At present, a cell is treated as dead if it counts 0 in more than 80% of the runs. However this could be an issue in stroboscopic measurements (very short acquisitions), so this behaviour could have to be revised.
 * There are some differences in the efficiencies computed by Lamp and Mantid for some detector cells. However it was noted that the efficiency scan used by Gagik is not particularly good, so this does not seem to be an issue.
 * For testing or checking purposes, Thomas would like to be able to stop the reduction workflow at different points.
  
To do:
 * Grouping of diffraction patterns.
 * ROC corrections?
 * Testing with more data, types of scan and instruments (D1B) --> Needs NeXus files.
 * Validate GSAS output?

