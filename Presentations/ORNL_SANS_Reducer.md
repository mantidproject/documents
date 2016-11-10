# ORNL_SANS_Reducer

## TL;TR;

Documentation: http://docs.mantidproject.org/nightly/concepts/ORNL_SANS_Reduction.html

## 

Code is in the folder:
`mantid/scripts/reduction_workflow`

## Reduction script

imports:
```python
from reduction_workflow.instruments.sans.hfir_command_interface import *
```

Code example:
```python
GPSANS()
# (....)
Reduce()
```

## Code

https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/instruments/sans/hfir_command_interface.py

Sets poperties on `ReductionSingleton()`, e.g.:
```python
ReductionSingleton().reduction_properties["BeamCenterFile"] = datafile
```



`ReductionSingleton()` is here:
https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/command_interface.py

The `ReductionSingleton()` contains an instance of `Reducer`

`Reducer` is here: https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/reducer.py

