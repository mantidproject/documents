Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------
* [Py-Qt-MVC](https://github.com/morefigs/Py-Qt-MVC) (Owen)
* Change of performance review ownership (Owen)
* What version of osx should be supported?
* Should we move http://docs.mantidproject.org and http://downloads.mantidproject.org from linode to github?
* [Require Python 2.7 on RHEL 6?](http://www.curiousefficiency.org/posts/2015/04/stop-supporting-python26.html)
* Discussion questions:
  1.  Do we move our 1D/2D plotting to use matplotlib directly?
  2.  Do we drop our fitting for scipy’s?
  3.  Do we move TableWorkspace to be a pandas DataFrame [[1](http://stackoverflow.com/questions/21647054/creating-a-pandas-dataframe-with-a-numpy-array-containing-multiple-types)]?
  4.  Do we change Workspace2D (or lower) to use XArray?
  5.  Do we migrate our current underlying geometry to [CombLayer](https://github.com/SAnsell/CombLayer), openCascade[[2](https://blog.kitware.com/designing-nuclear-reactor-core-geometry-and-meshes/), [3](http://dev.opencascade.org/index.php?q=node/1090), [4](http://www.opencascade.com/doc/occt-7.0.0/overview/html/occt_user_guides__vis.html)] VTK?

Minutes
-------

Attendees: Whitfield, Hahn, Savici, Peterson, Arnold, Gigg, Heybrock

* Py-Qt-MVC looks like a useful tool to add in the future
* Reviewing performance tests has moved to Lamar
* OSX supported is Yosemite (10.10) and El Capitan (10.11). Yosemite is what most build servers will run.
* Publish the download html pages to `gh-pages` branch in its repository (Pete)
* TSC agrees that we should look more into software collections for python 2.7 on rhel6 during the mantid 3.8 development cycle
* 
