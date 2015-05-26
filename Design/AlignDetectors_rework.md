Motivation
----------
With the NOMAD instrument there is a consistent issue with figuring out which instrument geometry a given calibration file
was created with. Since the offsets are relative, using the wrong geometry makes the calibration (potentially) useless. In
addition, the instrument team has determined that adding additional TOF dependant calibration parameters (`DIFA` and `TZERO`)
yield better focused data. This design will address both of these issues.

