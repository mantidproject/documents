Introduction
------------

The Technical Steering Committee (TSC) have been asked by the Project Management Board (PMB) to have a look at what are the implications (mainly on a staff effort basis) of continuing to support and run RHEL6 as the main data analysis platform to run Mantid on at both the SNS and ISIS.


What are the general issues with RHEL ?
---------------------------------------

The main problems with RHEL we have all basically stem from the issue that RHEL is based on an aging toolset.  While this can be advantageous for certain use cases (e.g. infrastructure servers) it is not necessarily well suited to the use as a scientific workstation.  This problem seems to be worse for RHEL than some other 'Enterprise' releases due to the uncertainty in the release schedule for RHEL, e.g. Ubuntu LTS is released every 2 years.

Specific issues 
---------------

 * Backporting dependencies
 * Monitoring backported packages for security updates
 * Language features that are unavailable (e.g. lack of C++11 features in GCC 4.4, Python 2.6)
 * Work arounds for RHEL6 specific bugs 
 * Bugs in RHEL6 that we have no solution for that limit functionality (e.g. Paraview on RHEL6)
 * The roadmap and support plans of our 3rd party dependencies for RHEL6
 * Next version of iPython is Python 2.7 only (RHEL6 only has Python 2.6)
 * Paraview is looking at moving to Qt5

Summary
-------

The approximate time taken by developers over the year to backport packages is 2 man months.  This does not include the additional time that we should take to monitor these backported packages for security updates and then rebuild to apply the fixes. It is estimated that this would be roughly 1 man week per (main) package per year.

Apart from developers, the other group of people who spend time supporting RHEL6 are the sysadmin staff.  Estimating the time they spend on RHEL as opposed to another linux distro is unclear, but at the SNS the sysadmin staff report that they have at least 2-3 updates per year from RHEL that cause significant issues in the smooth operation of the system.

