Agenda
======

Pinned Topics
-------------

New Items
---------

- Set a date for renaming `master`->`main`?

- Brief update on new mantid governance
- Brief update on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md)
- Review of [maintenance tasks](https://github.com/mantidproject/mantid/projects/15)
- Nexus API might be deprecated. Do we:
  - take ownership of it https://github.com/nexusformat/code
  - write our own API on top of HDF5
  - get rid of it, and replace by plain [HDF5 CPP](https://portal.hdfgroup.org/pages/viewpage.action?pageId=50073884)
  - adopt the [API from ESS](https://github.com/ess-dmsc/h5cpp)
- WIP document on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md).
  - As agreed previously we said once we dropped MantidPlot we would get to work on sorting out the dependency management issues. Above is something
    I put together to summarise the current state and look at solutions.
    Pull request: https://github.com/mantidproject/documents/pull/78
    Conda + some bundling solution is current suggestion.

- Discussion on hosting binaries:
  - Sourceforge continues to give us problems including timeouts on developer packages, and slow downloads for recent versions.
  - Bintray appears to be quite expensive for our needs (TBC with Martyn?)
  - Approx 2-3Tb unused outbound available on Linode server.
  - Looking at SourceForge data December was our largest no. downloads at ~1100. At 400MB (Windows) this would use 4TB alone
  - CDNs do not guarantee caching for such large objects, so we should assume worst case direct-downloads.
  - Possible options: Shrink package down enough to host on Linode / Point to Github Assets instead for releases / Decentralise `download.mantidproject.org` across facilities with free outbound / Something else?

- Shrinking installer size (Low priority):
  (Results from Windows)
  - QtWebEngine shrinks to 75MB compressed, this is one of the largest files in our bin
  - Could we use a local browser of shipping Chromium for our help pages?
  - SciPy / NumPy take another 50MB compressed, if the dep. management changes ship these separate we could easily shrink Mantid down to ~100MB.
  - Lighter packages help with users putting off trialing nightlies / beta versions, as they take a significant time to installer on HDDs

Minutes
-------
Attendees: Fairbrother, Gigg, Hahn, Nixon, Peterson, Savici

- Brief discussion of release. Things that would stop release (all are in progress)
  - DownloadInstrument bug
  - OSX installer suffix
  - Muon gui
- Rename `master` to `main` on the first Monday after the release is announced. Currently, 2021-02-15
- When we move to a new version of `clang-format`, change the maximum line length to 119. We should also look into reducing the line length for python to 119 as well. This should wait until [`pre-commit`](https://github.com/mantidproject/mantid/issues/30265) has been configured for developers.
