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
