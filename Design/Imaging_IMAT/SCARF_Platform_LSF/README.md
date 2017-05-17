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
STFC, and uses federal IDs. Also, as an exception to the PAC defaults,
the paths that are by default defined in the PAC as 
`/platform/webservice/pacclient/jobs` for example, are modified like 
`/webservice/pacclient/jobs` (the initial `platform` path component is 
removed).

Additional references
---------------------

* The Platform LSF Web services (and the client scripts) are described
here:
https://www-01.ibm.com/support/knowledgecenter/SSGSCT_9.1.3/admin_guide/chap_web_services.dita?lang=en,
and further documentation can be found in the Platform LSF Wiki
(https://www.ibm.com/developerworks/community/wikis/home/wiki/New%20IBM%20Platform%20LSF%20Wiki?lang=en).

* A document that can be very helful in understanding the Platform LSF
  PAC web service is "IBM Platform Application Center V9.1: How to
  build client to submit and monitor job via Web Service"
  (https://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/e6e150b1-eb13-4a8c-86d2-6126a2f6d729/page/de8c4e9d-24a1-4593-a23e-5049741ef5d6/attachment/6822f93c-b9ea-4913-bf46-fea84446f164/media/Platform_PAC_WS_job_submission.pdf)
  which can be found in the Platform Application Center Wiki
  (https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20Platform%20LSF%20Wiki/page/IBM%20Platform%20Application%20Center).
