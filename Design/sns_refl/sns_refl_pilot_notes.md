#QuickNXS Notes

## Running QuickNXS on Ubuntu

### Start-up

These dependencies were not met on my system, so had to be installed:
```sh
 apt-get install python-h5py python-psutil
```

I also had to teach it where to find Mantid.

```diff
diff --git a/quicknxs/main_gui.py b/quicknxs/main_gui.py
index bd7d4f5..55e2342 100644
--- a/quicknxs/main_gui.py
+++ b/quicknxs/main_gui.py
@@ -4,10 +4,11 @@
 Module including main GUI class with all signal handling and plot creation.
 '''
 
 import os
 import sys
+sys.path.append(os.environ['MANTIDPATH'])
 import math
 from math import radians, fabs
 from glob import glob
 from numpy import where, pi, newaxis, log10, array, empty, shape
 from matplotlib.lines import Line2D
```

Since I don't have a proper installation of Mantid on my machine at `/opt/mantid`
I had to set `$MANTIDPATH` manually.

 MANTIDPATH=/home/harry/MantidProject/main/build/bin ./scripts/quicknxs


### Loading data

In Mantid, I have `SNS` as my default facility, and `REF_L` as my default instrument.

I placed the following files in directories searched by Mantid:

* REF_L_116999_event.nxs
* REF_L_116998_event.nxs
* REF_L_116935_event.nxs
* REF_L_116936_event.nxs


## Implementation Notes

### Decorators

Several custom decorators are used internally. They're all defined in `decorators.py`

* **log_call**
    * If log level isn't DEBUG, does nothing. Otherwise, logs the function call, and basic metadata (line no, etc.)
* **log_input**
    * Similar to log_call, but logs the input values/parameters
* **log_output**
    * Similar to log_call, but logs the return value too
* **log_both**
    * A combination of log_input and log_output
* **time_call**
    * Times how long the function took (does not write to log, timing data is stored elsewhere)
* **waiting_effects**
    * Wraps calls in a function that sets/unsets a waiting cursor

### Processing

While some processing used to be performed by `calc_refl` and `plot_refl`, `plot_refl` currently
returns immediately, leaving no other calls to `calc_refl`, orphaning it.

Currently, hitting the "REDUCE" button calls the `runReduction` method of `main_gui`, which
instantiates the `REFLReduction` class from the Reduction module. This class then uses its own
`ReductionObject` class, from the same module, to wrap the calculation steps, which are performed
using Mantid's python simpleapi. The data itself is located using Mantid, but loaded using the
`NXSData` class, from the `qreduce` module.

The `gui_utils` module contains a class called `Reducer`, however this is only used by the
quickReduce action, which does not seem to be accessible from the reflectometry interface.

The scaling factor file handled in `ReductionObject::apply_scaling_factor`, which is called by
`REFLReduction::__init__`.
In the scaling factor file, various properties such as the slit positions, the medium, and slit
width are used to look up the correct values and error values for `a` and `b`. All of the values
other than `a`, `b`, `a_error`, `b_error`, are used to match. The `s1w` and `s2w` values may
be optionally ignored when searching for a match, as specified by the user.
The scaling factor is applied with the function: `f(x) = a + b * x`.

The data and normalisation data objects, and their configuration objects are stored in an
internal array of the form:
`[ [dataObject, normObject, configObject], ... ]`

Scaling factor processing is handled by the `CalculateSF` class, imported from the `calculate_SF`
module.

Once processing has completed, there doesn't seem to be much functionality for outputting data.
In the code there's some functionality for outputting ASCII files in `utilities.py`, but I've
yet to find a way to use it from the GUI. There is an "Export the plot to ASCII" button on the
scaling factor preview plot, but its output is too terse to be of much use.


#### Profile

Indentation denotes the time consumed is a subset of the parent, not in addition to it.
```
47.35s spent in qreduce.py NSXData::_read_REFL_file
44.55s spent in qreduce.py LRDataSet::from_event
  43.45 spent in qreduce.py LRDataset::getIxyt
35.18s spent in reduce.py ReductionObject::__init__
25.11s spent in reduce.py ReductionObject::rebin
  25.11 spent in qreduce.py LRDataset::getIxyt
13.07s spent in main_gui.py loading_configuration_file
```

### XML Config Format

The parsing itself is performed inside `main_gui.py`, in `loadFullConfigAndPopulateGui()`.
Large amounts of the parsing logic is duplicated in `loadConfigAndPopulateGui()`, which could
be cleaned up.

The XML config file contains several nodes called `RefLData`, and for each of them it:

* Creates a new row in the main table.
* The value of `<data_sets>` is inserted in to column 0 (run number).
* The value of `<norm_dataset>` is inserted in to column 6 (normalisation run number).
* The value of `<incident_angle>` is inserted in to column 1 (incident angle), and is optional.
* The value of `<from_lambda_range>` is inserted in to column 2 (lambda min), and is optional.
* The value of `<to_lambda_range>` is inserted in to column 3 (lambda max), and is optional.
* The value of `<from_q_range>` is inserted in to column 4 (q min), and is optional.
* The value of `<to_q_range>` is inserted in to column 5 (q max), and is optional.

* If this is the very first row:
    * The value of `<scaling_factor_file>` is loaded to scaling factor file lineedit.
    * The value of `<scaling_factor_flag>` is loaded to scaling factor checkbox.
    * The value of `<slits_width_flag>` is loaded to scaling factor slits width flag checkbox.
    * The value of `<incident_medium_list>` is csv and placed into select incident medium list.
    * The value of `<incident_medium_index_selected>` is used to select incident medium.
    * The value of `<fourth_column_flag>` is used to set output4thColumnFlag checkbox.
    * The value of `<fourth_column_dq0>` is used to set dq0 lineedit value.
    * The value of `<fourth_column_dq_over_q>` is used to set dQoverQ lineedit value.

* The value of `<data_full_file_name>` is loaded using the `NXSData` class.
* The value of `<norm_full_file_name>` is loaded using the `NXSData` class.


### Other

Some abbreviations are used across the code base.
As far as I can deduce, these are their definitions:

* **ai**: angle of incidence
* **tth**: two theta
* **dai**: resolution, i.e. delta angle of incidence
* **yi**: lambda / i
* **yt**: lambda / tof
* **it**: i / tof
* **ix**: i / x

### Module Summaries

* **main_gui**
    * the main gui logic

* **qreduce**
    * handles reading NXS files to instantiate MRDataset and other objects

* **reduction**
    * handles processing data using mantid algorithms

* **open_run_number**
    * handles manual loading of runs
    * OpenRunNumber class locates and loads the run, using FileFinder from Mantid

* **single_plot_click**
    * handles double*click logic for main_gui

* **utilities**
    * provides utility calculation functions

* **calculate_sf**
    * provides the CalculateSF class, which determines the best scaling factor to use when stitching two datasets

### Possible improvements

* There's plenty of orphans in main_gui and other places that could be deleted.
* There's also a lot of commented out code that could be deleted.
