The need for patch releases should be greatly reduced if we had a mechanism to download updated versions of the 
instrument geometries. This document describes how that will happen.

This design makes some assumptions:
 1. The term "instrument geometry" is intended to mean both the geometry and any associated parameter files.
 2. Users will always want to have the full list of instruments as found in master.
 3. The data fetched will be read only.
 4. Checksums are valid for verifying that files are unique rather than resorting to detailed difference checking.

Changes to Instrument Loading
-----------------------------

Storing Updated Instruments
---------------------------

Updating Instruments
--------------------
Since all of the instruments currently reside in a [single directory](https://github.com/mantidproject/mantid/tree/master/Code/Mantid/instrument) we can use a single github api call to [get the list of the directory](https://developer.github.com/v3/git/trees/) then multiple subsequent calls to [download the updated/changed instrument geometries](https://developer.github.com/v3/git/blobs/).

Purging Instrument Cache
------------------------
