Motivation
==========

In the case of autoreduction at ORNL, each run (e.g. nexus file) is processed independently.
Often during the processing some portions of the data processing re-occurs.
Specifically, many runs re-use the same characterization files (i.e. vanadium, empty instrument).
Since each autoreduction job acts independently, each one will reprocess these every time.
As an experiment continues the same characterization files get reprocessed dozens, if not hundreds of times.
This wastes computational resources as well as users' time waiting.
This design will address a way to cache the results of partially processed data for reuse in future calculations.

Requirements
============

1. The cached information will be available between mantid sessions (shut-down and start-up).
2. The cached information will be saved at the user level (e.g. in a location in the user's home area rather than a system-wide cache).
3. Cache files will bear enough information (through metadata or filename) to identify how they were produced. A hash of the processing information in the cache filename will probably be sufficient.
4. Cache files will be deleteable with the only side effect being performance degradation.

Using cache files will likely fall on script writers to take advantage of rather central to workflow algorithms.
This will allow for them to be used in a variety of ways rather than just to assist workflow algorithms.

Design
======

Loading Information From Cache
------------------------------

There are three basic steps for loading information form cache:

1. **Determining what would be produced.** This should be done by looking at the appropriate parameters used to produce the file. Since the list can be restrictively long, this can be passed through a hasing algorithm (e.g. `sha1`) to generate a unique specifier.
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
All of these properties are optional.
The whitelist and blacklist will be used to select which of the properties in the `PropertyManager` will be used to calculate the hash.
The string array is will be key/value pairs of properties that should be considered, but are not in the provided `PropertyManager`.
If a directory is not specified, cache files will go into a `cache` subdirectory of `ConfigService::getUserPropertiesDir()`.
On unix this will be `~/.mantid/cache`.

The algorithm will convert all properties to strings as `"%s=%s" % (property.name, property.valueAsStr)`, sort the list, then convert it to a `sha1`.
A filename with the form `<location>/<prefix>_<sha1>.nxs` will be return as the output property.
If no prefix is specified then file result will be `<location>/<sha1>.nxs`.

**CleanCache**

There will also be an algorithm to remove files from the cache directory so users won't need to find it themselves. 
This algorithm will take time (default age is two weeks) or a boolean to remove all files.
The algorithm will then delete files in the cache directory that end in `<sha1>.nxs`.
