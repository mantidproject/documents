Introduction
------------

The Technical Steering Committee (TSC) have been asked by the Project Management Board (PMB) to have a look at what are the implications (mainly on a staff effort basis) of continuing to support and run RHEL6 as the main data analysis platform to run Mantid on at both the SNS and ISIS.


What are the issues with RHEL ?
-------------------------------

The main problems with RHEL we have all basically stem from the issue that RHEL is based on an aging toolset.  While this can be advantageous for certain use cases (e.g. infrastructure servers) it is not necessarily well suited to the use as a scientific workstation.  This problem seems to be worse for RHEL than some other 'Enterprise' releases due to the uncertainty in the release schedule for RHEL, e.g. Ubuntu LTS is released every 2 years.

Where do we Spend Staff Effort
------------------------------



Summary
-------

The approximate time taken by developers over the year to backport packages is 2 man months.  This does not include the additional time that we should take to monitor these backported packages for security updates and then rebuild to apply the fixes. It is estimated that this would be roughly 1 man week per (main) package per year.
