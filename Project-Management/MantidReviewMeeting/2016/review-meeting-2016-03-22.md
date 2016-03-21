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
  * Calibration of every detector/pixel: [EnggCalibrateFull](http://docs.mantidproject.org/nightly/algorithms/EnggCalibrateFull-v1.html)
  * Calibration of banks: [EnggCalibrate](http://docs.mantidproject.org/nightly/algorithms/EnggCalibrate-v1.html)
  *  The legacy ascii/csv format that you shouln'd use: [ENGINX_full_pixel_calibration_vana194547_ceria193749.csv](https://github.com/mantidproject/mantid/blob/master/scripts/Engineering/calib/ENGINX_full_pixel_calibration_vana194547_ceria193749.csv)
  *  The [HDF format]((http://docs.mantidproject.org/nightly/concepts/DiffractionCalibrationWorkspace.html)) that will be used.

* PSDTubes (Anders)
