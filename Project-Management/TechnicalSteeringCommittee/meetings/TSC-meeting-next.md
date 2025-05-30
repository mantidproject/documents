Agenda
======


"New" Items
---------

- Update on Apple have dropped support for macOS High Sierra (Martyn)

- Update on Ubuntu 16.04 EOL - April 30th (David)
  - Changes to wiki
  - Plan to migrate to LTS 20.04, move remaining non-docker services into containers to make upgrades / maintenance easier
  - Should use a new VM instead of upgrading existing; allows us to quickly back out to old VM and starts with a "clean-slate" to (hopefully) fix TCP speed issues
  - Wiki is a problem component: The theme used (with our own extra CSS on top) is EOL and does not work with newer versions
  - Options include: - Pick another theme and get someone to throw CSS on top again, - Migrate to our own or Github static pages, - Something Else?

- Brief update on new mantid governance
- Brief update on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md)
- Review of [maintenance tasks](https://github.com/mantidproject/mantid/projects/15)
- Nexus API might be deprecated (need update on plans). Do we:
  - take ownership of it https://github.com/nexusformat/code
  - write our own API on top of HDF5
  - get rid of it, and replace by plain [HDF5 CPP](https://portal.hdfgroup.org/pages/viewpage.action?pageId=50073884)
  - adopt the [API from ESS](https://github.com/ess-dmsc/h5cpp)
- WIP document on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md).
  - As agreed previously we said once we dropped MantidPlot we would get to work on sorting out the dependency management issues. Above is something
    I put together to summarise the current state and look at solutions.
    Pull request: https://github.com/mantidproject/documents/pull/78
    Conda + some bundling solution is current suggestion.

- Shrinking installer size (Low priority):
  (Results from Windows)
  - QtWebEngine shrinks to 75MB compressed, this is one of the largest files in our bin
  - Could we use a local browser of shipping Chromium for our help pages?
  - SciPy / NumPy take another 50MB compressed, if the dep. management changes ship these separate we could easily shrink Mantid down to ~100MB.
  - Lighter packages help with users putting off trialing nightlies / beta versions, as they take a significant time to installer on HDDs

- [Discussion on vtk instrument demo](https://github.com/DanNixon/vtk_instrument_view_demo) (Dan)
