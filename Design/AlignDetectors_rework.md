Motivation
----------
With the NOMAD instrument there is a consistent issue with figuring out which instrument geometry a given calibration file
was created with. Since the offsets are relative, using the wrong geometry makes the calibration (potentially) useless. In
addition, the instrument team has determined that adding additional TOF dependant calibration parameters (`DIFA` and `TZERO`)
yield better focused data. This design will address both of these issues.

Select Additional Requirements
------------------------------
1. The information needs to be stored in a file that can be read/written quickly and with accuracy. There is a performance issue with SNAP which has 18x256x256 pixels.
2. The parameters need to be somewhat flexible since the specific calibration parameters used change over time.
3. Which instrument (e.g. name and date) the parameters are valid for is useful for diagnosing/debugging purposes.

Proposed Solution
-----------------
