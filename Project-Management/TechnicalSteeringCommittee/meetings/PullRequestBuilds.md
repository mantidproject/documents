
Changes required
==================

* Pull request is the last possible step. Hardware demand is high per pull request, so pull requests are only done when the work is finished
* Keep automatic build with Pull Request. We need to show people how to skip CI when they make additional commits to open tickets
* External data needs to be finished, since we need everything to be available in the same repo as there will be no downstream steps
* [buildscripts](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Build/Jenkins) all need to be updated. These kick off the following (all part of the same job)

Pull Request Jenkins Job Process
================================

1.  Unit tests are run on all platforms
1.  All platforms have packages created
1.  System tests on RHEL6
1.  Doc test on Windows
