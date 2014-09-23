Timing Code
-----------
```python
import mantid
from mantid.simpleapi import Load
import sys
import time

precount = ("-npc" not in sys.argv)

start = time.time()
Load(Filename='PG3_2538_event.nxs', OutputWorkspace='PG3_2538_event',
     Precount=precount)
print "Elapsed time: %.4f seconds" % (time.time() - start)
```

Setup
-----

tcmalloc can be used in 2 different ways:
 1. Add to compile-time link list as ```-ltcmalloc``` and run executable as normal; 
 2. Do not compile in library but run executable using LD_PRELOAD: 

```LD_PRELOAD=libtcmalloc.so bin/MantidPlot```

or

```LD_PRELOAD=libtcmalloc.so python``` 


Timings
-------

"TCMALLOC=" in this context relates to the CMake flag.


| Description                 | TCMALLOC=ON && -ltcmalloc     | TCMALLOC=OFF && LD_PRELOAD=libtcmalloc.so  | TCMALLOC=OFF && No LD_PRELOAD |
| --------------------------- |:-----------------------------:|:------------------------------------------:|:-----------------------------:|
| Plain Python, with precount | Elapsed time: 7.3411 seconds  | Elapsed time: 5.9982 seconds               | Elapsed time: 7.4580 seconds
| Plain Python, NO precount   | Elapsed time: 14.8702 seconds | Elapsed time: 6.1999 seconds               | Elapsed time: 16.5008 seconds
| MantidPlot, with precount   | Elapsed time: 6.1279 seconds  | Elapsed time: 6.0493 seconds               | Elapsed time: 7.7117 seconds  |
| MantidPlot, NO precount     | Elapsed time: 6.3052 seconds  | Elapsed time: 6.2357 seconds               | Elapsed time: 17.5780 seconds |

Memory Reporting
----------------

### Code

```python
# mem_report.py
import mantid
from mantid.kernel import MemoryStats
from mantid.api import FrameworkManager
from mantid.simpleapi import Load
import os

mem = MemoryStats()
res1 = mem.residentMem()/1024.
print "Resident Memory Usage (MB)", res1
print

filename = "MER06398.raw" # in systemtests/Data
ws = Load(Filename=filename)
mem.update()
res2 = mem.residentMem()/1024.
print "Resident Memory Usage (KB)",res2
print "First load used (MB):",(res2-res1)
print

print "Clearing all memory (workspaces etc)"
FrameworkManager.clear()
mem.update()
res3 = mem.residentMem()/1024.
print "Resident Memory Usage (KB)",res3
print "Loss (MB)",(res3-res2)
print
print "Loading file again..."
ws = Load(Filename=os.path.join(filepath, filename))
mem.update()
res4 = mem.residentMem()/1024.
print "Resident Memory Usage (KB)",res4
print "Second load used (MB):",(res4-res3)
print

print "Clearing all memory (workspaces etc)"
FrameworkManager.clear()
mem.update()
res5 = mem.residentMem()/1024.
print "Resident Memory Usage (KB)",res5

print
print "Overall loss (MB):",(res5-res1)
```

### No Tcmalloc

```>>>``` *python mem_report.py*

```
FrameworkManager-[Notice] Welcome to Mantid version 3.2.20140826.1520 - Manipulation and Analysis Toolkit for Instrument Data
FrameworkManager-[Notice] Please cite Mantid in your publications using: http://dx.doi.org/10.5286/Software/Mantid
Resident Memory Usage (MB) 134.625

Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 6.52 seconds
Resident Memory Usage (KB) 3242.74609375
First load used (MB): 3108.12109375

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 3242.234375
Loss (MB) -0.51171875

Loading file again...
Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 5.96 seconds
Resident Memory Usage (KB) 3268.6796875
Second load used (MB): 26.4453125

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 3268.6796875

Overall loss (MB): 3134.0546875
```

### LD_PRELOAD TCMALLOC

```>>>``` *LD_PRELOAD=libtcmalloc.so python mem_report.py*

```
FrameworkManager-[Notice] Welcome to Mantid version 3.2.20140826.1520 - Manipulation and Analysis Toolkit for Instrument Data
FrameworkManager-[Notice] Please cite Mantid in your publications using: http://dx.doi.org/10.5286/Software/Mantid
Resident Memory Usage (MB) 136.21484375

Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 6.45 seconds
Resident Memory Usage (KB) 3638.20703125
First load used (MB): 3501.9921875

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 3635.01171875
Loss (MB) -3.1953125

Loading file again...
Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 5.85 seconds
Resident Memory Usage (KB) 3657.328125
Second load used (MB): 22.31640625

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 3657.328125

Overall loss (MB): 3521.11328125
```

### LD_PRELOAD TCMALLOC AND TCMALLOC_RELEASE_RATE

```>>>``` *LD_PRELOAD=libtcmalloc.so TCMALLOC_RELEASE_RATE=10000 python mem_report.py*

```
FrameworkManager-[Notice] Welcome to Mantid version 3.2.20140826.1520 - Manipulation and Analysis Toolkit for Instrument Data
FrameworkManager-[Notice] Please cite Mantid in your publications using: http://dx.doi.org/10.5286/Software/Mantid
Resident Memory Usage (MB) 136.25

Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 6.51 seconds
Resident Memory Usage (KB) 3592.09375
First load used (MB): 3455.84375

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 165.0859375
Loss (MB) -3427.0078125

Loading file again...
Load-[Notice] Load started
LogParser-[Warning] Cannot process ICPevent log. Period 1 assumed for all data.
Load-[Notice] Load successful, Duration 6.64 seconds
Resident Memory Usage (KB) 3595.140625
Second load used (MB): 3430.0546875

Clearing all memory (workspaces etc)
Resident Memory Usage (KB) 167.90234375

Overall loss (MB): 31.65234375
```
