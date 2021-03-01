Agenda
======


New Items
---------

- Keeping an eye on the stale issue detector it appears to be working well, however `Never Stale` isn't really doing what it should (David)
  - (This is verbose as I may be in an exam when the TSC meeting starts, but I'd like the discussion to happen this meeting, as the number of issues it affects will grow)
  - The label is being applied to bugs that exist and need fixing at "some point", but have lingered for years without any new activity or plans to fix soon.
  - The comment approach requires effort (intentionally) so people end up label setting-and-forgetting. Ultimately, we'll end up coming full circle to a large number of issues that are never stale and rot.
  - Fundamentally, the mistake is mine (David) picking "Never Stale", rather than actually asking the TSC what types of issues we want to keep long term. We should instead explicitly choose types of issues we want to keep and let the rest close with no interest. My questions are:
  - What labels do we add as exceptions as a type of issue that can linger for years, e.g. "Planning" or "Meta-issue"? Alternatively, should these long-term roadmaps (12-36+ months) be moved somewhere else and we all inactive issues can be marked marked as stale?
  - Should we write-up and enforce a issue life-time policy before we have a large number of issues in the "grey-zone" - possible suggestions:
  - What metric(s) do we apply to un-labelling a "Never Stale" issue. E.g. a bug can always be made stale, because if they're not important enough to fix in 6 months...
  - What period of time can a "Never Stale" issue be bumped for. E.g. if it's 3+ years and there's no progress or interest on a feature beyond pings to keep it alive do we close it?
  - Any others thoughts or feedback?

- Apple have dropped support for macOS High Sierra. What do we move our minimum supported version of macOS to? (Martyn)

- Ubuntu 16.04 EOL - April 30th (David)
  - Plan to migrate to LTS 20.04, move remaining non-docker services into containers to make upgrades / maintenance easier
  - Should use a new VM instead of upgrading existing; allows us to quickly back out to old VM and starts with a "clean-slate" to (hopefully) fix TCP speed issues
  - Wiki is a problem component: The theme used (with our own extra CSS on top) is EOL and does not work with newer versions
  - Options include: - Pick another theme and get someone to throw CSS on top again, - Migrate to our own or Github static pages, - Something Else?
- Implementation plan for pre-commit hooks. See [pull request](https://github.com/mantidproject/documents/pull/88) (Sam)
    

Last Meeting
------------

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
