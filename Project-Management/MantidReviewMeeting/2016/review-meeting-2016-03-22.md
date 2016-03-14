Agenda:  Calibration Files in Mantid
=========

* General Introduction to Calibration Files (Nick)

* Powder Diffraction (Pete, Vickie or Wendou)
  * [CalibrateRectangularDetectors](http://docs.mantidproject.org/nightly/algorithms/CalibrateRectangularDetectors-v1.html)
    * [GetDetectorOffsets](http://docs.mantidproject.org/nightly/algorithms/GetDetectorOffsets-v1.html)
    * [GetDetOffsetsMultiPeaks](http://docs.mantidproject.org/nightly/algorithms/GetDetOffsetsMultiPeaks-v1.html)
  * [AlignComponents](https://github.com/mantidproject/mantid/blob/master/docs/source/algorithms/AlignComponents-v1.rst)
  * [ascii file format](http://docs.mantidproject.org/nightly/algorithms/LoadCalFile-v1.html)
  * [h5 file format](http://docs.mantidproject.org/nightly/concepts/DiffractionCalibrationWorkspace.html)

* SCD Panel (Pete, Vickie or Wendou)
  * [SCDCalibratePanels](http://docs.mantidproject.org/nightly/algorithms/SCDCalibratePanels-v1.html)
    * Copied from ISAW (SCD Calibration), but ISAW's calibration is still better
    * Only works for RectangularDetectors
    * Input is PeaksWorkspace with peaks from multiple orientations
    * Output is DetCal file for LoadIsawDetCal
    * New TOPAZ IDF from script [TOPAZFromDetCal.py](https://github.com/mantidproject/mantidgeometry/blob/master/TOPAZ/TOPAZFromDetCal.py)
    * New MANDI IDF from script [MANDIFromDetCal.py](https://github.com/mantidproject/mantidgeometry/blob/master/MANDI/MANDIFromDetCal.py)
  
* Engineering (Federico)

* PSDTubes (Anders)
