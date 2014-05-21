Agenda
======

1. [Monitors in Live Data](https://github.com/mantidproject/documents/blob/master/Design/MonitorsInLiveData.md)
2. Build servers
   1. Requirments for OS to be in matrix build
      1. Only officially supported OS as declared by PMB
      2. At minimum two servers at each site (ISIS and ORNL)
      3. Work out initial bugs in partially supported area
   2. Partially supported platforms
   3. Tab names
   4. Other static checks: CPD, [pylint](http://www.pylint.org/), [pyflakes](https://pypi.python.org/pypi/pyflakes),
      [pep8](https://pypi.python.org/pypi/pep8)
   5. [SonarQube](http://www.sonarqube.org/) with [Sonar cxx](https://github.com/wenns/sonar-cxx)
6. Tasks that Russell does that the TSC should take over
   * Look after nightly builds
   * Look after performance tests (master, develop, and RHEL6 rolling system test)
2. Developer documentation
6. [Getting DOIs for releases from github](https://guides.github.com/activities/citable-code/)
7. Embedded IDF in NeXus files
