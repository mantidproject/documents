Agenda
======

Pinned Topics
-------------

New Items
---------

- Decision on CII Best Practices
- PVS Studio (https://www.viva64.com/en/b/0679/)
- Switch to Let's Encrypt (RFC 8555) before 1st/11th September?
- FYI: Docker updated retention policy - 6 months for free accounts
- Maintenance/MantidPlot cleanup plans
  - Need to get codebase in state to build everything without MantidPlot. Biggest thing is docs (I think?). Would be nice to get them building faster too...
  - Current known issues summarized in https://github.com/mantidproject/mantid/issues/28650
  - Small team to focus on this? Not sure there is enough work to chuck everything at it?
- WIP document on [dependency handling](https://github.com/mantidproject/documents/blob/thirdparty-dependencies/Design/ThirdpartyDependencies.md).
  - As agreed previously we said once we dropped MantidPlot we would get to work on sorting out the dependency management issues. Above is something
    I put together to summarise the current state and look at solutions. Needs a bit of tidying then I'll open a pull request and we can discuss next time? 

Minutes
-------
Attendees: Gigg, Nixon, Savici, Hahn, Peterson, Guest, Fairbrother

* Nixon will add CII to the mantid project repository
* PVS studio will be evaluated as a maintenance task to see if it is useful
* Plan on changing to Let's Encrypt on 2020-08-27 (evening UK/lunchtime US). Servers will be down. The fallback is to restore from backup taken just before the switch
