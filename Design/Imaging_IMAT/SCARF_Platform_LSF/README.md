SCARF Platform LSF client scripts
=================================

These are a handful of Python scripts to interact with the web service
provided by the SCARF cluster (http://www.scarf.rl.ac.uk/), which is
based on IBM Platform LSF
(http://www-03.ibm.com/systems/uk/platformcomputing/products/lsf/).

These scripts are effectively the definition of the SCARF remote job
control web service API. The scripts are included here as provided in
February 2015. They contain comments on particular issues (especially
certificates and authentication), and, importantly, the paths used for
different requests (submit, cancel, query jobs, query files, etc.).

Note that the scripts follow the API of the Platform LSF web service
(with one exception). This web service is defined in the IBM Platform
Application Center (PAC), which is an add-on module for Platform
LSF. PAC version 9.1 provides a RESTful web service which is used in
these scripts to interact with the SCARF job scheduler. As of this
writing, the version of Platform LSF PAC used on SCARF is 9.1.3.0.

These scripts have guided the implementation of the SCARFLSFJobManager
and LSFJobManager classes in Mantid. The script `paclogin.py`
represents an exception to the general Platform LSF RESTful API: the
login request is handled by a script that is specific to SCARF and
STFC, and uses federal IDs.
