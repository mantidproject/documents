The need for patch releases should be greatly reduced if we had a mechanism to download updated versions of the 
instrument geometries. This document describes how that will happen.

This design makes some assumptions:
 1. The term "instrument geometry" is intended to mean both the geometry and any associated parameter files.
 2. Users will always want to have the full list of instruments as found in master.
 3. Only print a warning if the files on github cannot be fetched rather than failing to startup.
 3. The data fetched will be read only.
 4. Checksums (i.e. sha) are valid for verifying that files are unique rather than resorting to detailed difference checking.

Changes to Instrument Loading
-----------------------------
Since linux systems will require having multiple locations for instrument files (rather than just the install area), the real change is to have a collection of locations for instrument files to reside. The path will be, in order, cache area then install area. 

Storing Updated Instruments
---------------------------
The cache area for instrument files should be in a directory where the user has write access. On linux and mac systems this will be `${HOME}/.mantid/instrument`. On windows this is `%Local AppData%mantidproject\.mantid\instrument`.

Updating Instruments
--------------------
Since all of the instruments currently reside in a [single directory](https://github.com/mantidproject/mantid/tree/master/Code/Mantid/instrument) we can use a single github api call to get the list of the directory, then multiple subsequent calls to download the updated/changed instrument geometries. This process should happen in a separate thread from the main gui when mantid starts up. This should provide adequate updates and minimize the impact on usability both on startup and when users will need the new files.
 1. Go through the files in the cache. If a file is identical to one in the install area, delete the copy in the cache area.
 2. Verify that there is network connection by [getting a list of repositories](https://developer.github.com/v3/repos/#list-organization-repositories) owned by the mantidproject "organization." An alternative is to see if one can see the main github page.
 3. [Get a list](https://developer.github.com/v3/repos/contents/#get-contents) of the instrument geometries in master.
 4. Go through the list of files and do one of the following:
    1. If the file in master does not exist locally, add it to the list to download
    2. If the file in master has a sha that is different from the local version (installed or cache), add to the list to download
    3. If the file in master has the same sha as the local version in install area or cache area, do nothing
 5. Go through the list to download and get the files
