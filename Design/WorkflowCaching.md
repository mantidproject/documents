Motivation
==========

In the case of autoreduction at ORNL, each run (e.g. nexus file) is processed independently.
Often during the processing some portions of the data processing re-occurs.
Specifically, many runs re-use the same characterization files (i.e. vanadium, empty instrument).
Since each autoreduction job acts independently, each one will reprocess these every time.
As an experiment continues the same characterization files get reprocessed dozens, if not hundreds of times.
This wastes computational resources as well as users' time.
This design will address this by defining a mechanism for caching the results of partially processed data for reuse in future calculations.

Requirements
============

1. The cached information will be available between mantid sessions (shut-down and start-up).
2. The cached information will be saved at the user level (e.g. in a location in the user's home area rather than a system-wide cache).
3. Cache files will bear enough information (through filename) to identify how they were produced. A hash of the processing information in the cache filename will probably be sufficient.
4. Cache files will be deleteable with the only side effect being performance degradation.

Using the cache files will likely fall on script writers to take advantage of rather central to workflow algorithms.
This will allow for them to be used in a variety of ways rather than just to assist workflow algorithms. This does mean that care must be taken for a race condition with cache files on distributed systems. A possible solution is to use [flock](https://github.com/misli/python-flock). There is also an issue with properties that change even though their string representation isn't (`FileProperty` and `WorkspaceProperty`). This is not addressed by this design.

Design
======

Loading Information From Cache
------------------------------

There are three basic steps for loading information form cache:

1. **Determining what would be produced.** This should be done by looking at the appropriate parameters used to produce the file. Since the list can be restrictively long, this can be passed through a hasing algorithm to generate a unique specifier.
2. **Finding if that exists.** While the hash generated from the processing parameters is unique, it lacks clarity to people that look in the cache directory. To aid this, the cache files should be named (when possible) `<instr>_<runid>_<sha1>.nxs`. This will users to, at a glance, have a cursory understanding what the files are.
3. **Loading the cache file.** Rather than create a new file format. The cache file will just be loaded using `LoadNexusProcessed`.
 
Processing and Saving to Cache
------------------------------

The workspace that will be cached should be saved using `SaveNexusProcessed` using filename described above.
The script maintainer should only save the workspace if it was not already found in the cache.
In python
```python
if not os.path.exists(vanCacheFilename):
    SaveNexusProcessed(InputWorkspace=vanWkspName, Filename=vanCacheFilename)
```

The Missing Link(s)
-------------------

**CreateCacheFilename**

The fundamental component that is missing is an "easy" way to create the hash from a set of processing parameters. This will be done as an Algorithm and borrow ideas from [python tempfile](https://docs.python.org/3/library/tempfile.html).
The algorithm will accept a prefix, [PropertyManager](http://docs.mantidproject.org/nightly/api/python/mantid/kernel/PropertyManager.html), whitelist of properties to use, blacklist of properties to exclude, and a string array (or `List`), and a directory for cache files to exist in.
All of these properties are individually optional, but failing to specify any should result in an error.
The whitelist and blacklist will be used to select which of the properties in the `PropertyManager` will be used to calculate the hash.
Both will be interpreted as globbing.
The string array is will be key/value pairs of properties that should be considered, but are not in the provided `PropertyManager`.
If a directory is not specified, cache files will go into a `cache` subdirectory of `ConfigService::getUserPropertiesDir()`.
On unix this will be `~/.mantid/cache`.

The algorithm will convert all properties to strings as `"%s=%s" % (property.name, property.valueAsStr)`, sort the list, then convert it to a `sha1`.
A filename with the form `<location>/<prefix>_<sha1>.nxs` will be returned as the output property.
If no prefix is specified then file result will be `<location>/<sha1>.nxs`.

**CleanFileCache**

There will also be an algorithm to remove files from the cache directory so users won't need to find the cache location themselves. 
This algorithm will take last modified time (default age is two weeks) or a boolean to remove all files.
The algorithm will then delete files in the cache directory that end in `<sha1>.nxs`.

Example
-------

This example is taken from NOMAD's autoreduction which is one of the main motivators for generating this infrastructure.

```python
import os
import sys
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
import mantid

eventFileAbs=sys.argv[1]
outputDir=sys.argv[2]
maxChunkSize=8.
if len(sys.argv)>3:
    maxChunkSize=float(sys.argv[3])

eventFile = os.path.split(eventFileAbs)[-1]
nexusDir = eventFileAbs.replace(eventFile, '')
runNumber = eventFile.split('_')[1]
configService = mantid.config
dataSearchPath = configService.getDataSearchDirs()
dataSearchPath.append(nexusDir)
configService.setDataSearchDirs(";".join(dataSearchPath))

# these should be options that are filled in by the calling script
resamplex=-6000
vanradius=0.58

# determine information for vanadium caching
wksp=LoadEventNexus(Filename=eventFileAbs, MetaDataOnly=True)
characterizations=PDLoadCharacterizations(Filename="%(char_file)s",
                                          ExpIniFilename="%(expini_file)s",
                                          OutputWorkspace="characterizations")[0]
PDDetermineCharacterizations(InputWorkspace=wksp,
                             Characterizations=characterizations)
DeleteWorkspace(str(wksp))
charPM = mantid.PropertyManagerDataService.retrieve('__pd_reduction_properties')
van_run=charPM['vanadium'].value[0]

vanWkspName="NOM_"+str(van_run)
vanProcessingKeys=['vanadium', 'empty', 'd_min', 'd_max', 'tof_min', 'tof_max']
vanProcessingProperties.append("ResampleX="+str(resamplex))
vanProcessingProperties.append("VanadiumRadius="+str(vanradius))
vanCacheFilename=CreateCacheFilename('__pd_reduction_properties', vanProcessingKeys,
                                 vanProcessingProperties, Prefix=vanWkspName,
                                 CacheDir=outputDir)

if os.path.exists(vanCacheFilename):
    print "Loading vanadium cache file '%%s'" %% vanCacheFilename
    Load(Filename=vanCacheFilename, OutputWorkspace=vanWkspName)

# process the run
SNSPowderReduction(Instrument="NOM", RunNumber=runNumber, Extension="_event.nxs",
                   MaxChunkSize=maxChunkSize, PreserveEvents=True,PushDataPositive='AddMinimum',
                   CalibrationFile="%(cal_file)s",
                   RemovePromptPulseWidth=50,
                   ResampleX=resamplex, BinInDspace=True, FilterBadPulses=25.,
                   SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=outputDir,
                   StripVanadiumPeaks=True,
                   VanadiumRadius=vanradius,
                   NormalizeByCurrent=True, FinalDataUnits="MomentumTransfer")

# save out the vanadium cache file
if not os.path.exists(vanCacheFilename):
    SaveNexusProcessed(InputWorkspace=vanWkspName, Filename=vanCacheFilename)

# save a picture of the normalized ritveld data
wksp_name="NOM_"+runNumber
SavePlot1D(InputWorkspace=wksp_name,
           OutputFilename=os.path.join(outputDir,wksp_name+'.png'),
           YLabel='Intensity')

```
