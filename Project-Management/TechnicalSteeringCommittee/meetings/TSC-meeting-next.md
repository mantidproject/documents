Agenda
======

Pinned Topics
-------------

New Items
---------

- WIP document on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md).
  - As agreed previously we said once we dropped MantidPlot we would get to work on sorting out the dependency management issues. Above is something
    I put together to summarise the current state and look at solutions. Needs a bit of tidying then I'll open a pull request and we can discuss next time?
    
- Nexus API might be deprecated. Do we:
  - take ownership of it https://github.com/nexusformat/code  
  - get rid of it, and replace by plain HDF5 CPP https://portal.hdfgroup.org/pages/viewpage.action?pageId=50073884 
  - adopt the API from ESS https://github.com/ess-dmsc/h5cpp
    
- Discussion on hosting binaries:
  - Sourceforge continues to give us problems including timeouts on developer packages, and slow downloads for recent versions.
  - Bintray appears to be quite expensive for our needs (TBC with Martyn?)
  - Approx 2-3Tb unused outbound available, but our current bin size would quickly eat away at that.
  - CDNs do not guarentee caching for such large objects, so we should assume worst case direct-downloads.
  - Possible options: Shrink package down enough to host on Linode / Decentralise `download.mantidproject.org` across facilities with free outbound / Something else?

- Add MSVC Debug System Test jobs
  - Additional validators present in debug mode have caught various undefined behaviours and bugs (e.g. TBB thread local issues / invalid iterator usage)
  - Few developers run all system tests in debug mode, so tend to linger
  - This job is quite slow / intensive so could only run nightly to avoid slowing down our PRs


Minutes
-------
Attendees:
