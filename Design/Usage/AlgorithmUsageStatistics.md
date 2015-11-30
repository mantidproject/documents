#Overview

We have several algorithms that are similar and would love to rationalise the code and make the choice of which algorithm to use easier for scientists.
However we always face the problem that we never know how much an algorithm is used.  It was agreed at the SSC2015 the we could track the usage of algorithms alongside simple startups of Mantid.

This design document should be considered as an extension of the previous implemented design [MeasureUsageStatistics](MeasureUsageStatistics.md).

##Proposed Changes

We propose to Centralise the sending of all Usage reports into a central service, and extend the current functinality to 
allow usage reports of features within Mantid, where a feature might be:

1. Execution of an algorithm, parent or child
1. Startup of a Interface
1. Usage of a particular feature in an interface

Initially we would only intend to automatically track Algorithm usage, but other usage reports can be added by developer as they deem helpful.
The contents of a Feature usage would be:

* type - Algorithm, Interface, Feature
* name - Identifying name, for algorithms this would be Algorithm and version
* time - The datetime of execution start
* duration - (optional) the execution duration
* details - (optional) Further details - for algorithms this will be a properties string, or possibly the python string of the Algorithm call.

These would be sent in addition to these fields in common with the startup Usage details:

* User ID hash
* host ID hash

###New Code

####API::UsageService

We would create a new service class called Usage Service which would be responsible for collating, and sending
all usage data.  This would centralise all the logic covering Usage Reporting including:

1. Detecting if repoting is enabled
1. Registering the startup of Mantid
1. Sending Startup usage reports, immediately, and every 24 hours thereafter
1. Registering feature usage, and storing in a feature usage buffer
1. Sending Feature usage reports on application exit, and when the feature usage buffer is above a size threshold.

###### Implementation Notes:

1. Use Poco::Timer to handle the timed aspects of the class
  1. The 24 resend of startup data
  1. Checking every n minutes if the feature buffer above the threshold for sending.
1. Registering Feature usage must be fast, just create the record and return.
1. Do not lock the feature usage buffer for any longer than is absolutely necessary.
1. Use a queue, rather than a vector for the feature usage buffer.
1. Create multiple overloads for registerFeatureUsage() to make is easy for other developers, one should be specialised for algorithms.
1. Internet calls should use the InternetHelper.

####Server side API

Clearly the django website https://github.com/mantidproject/webapp will need to be extended to accept feature usage reports.

Initially we do not plan to define reports for the feature usage data, they will be queried direct from the database using SQL.
Once a good understanding of the usefull aspects of the data clarifies we will look to integrating some reports into the API.

###To Existing Code

####API::FrameworkManager

Currently the code to send usage reports is in the FrameworkManager (FrameworkManagerImpl::SendStartupUsageInfo).  
As described above this change would create a UsageService which would be responsible for collating, and sending
all usage data.  As such I would propose to move the execution code from Framework Manager to the UsageService class, 
and replace it with a single call to UsageService::Instance().registerStartup().
This would also allow a single place to allow the additional logic to resend startup usage calls after 24 hours of constant running.
Currently Long running instances cause the usage statistics of Mantid to underreport.

###API::Algorithm

We would add a call to UsageService::Instance().registerFeatureUsage(*this) within the Execute method of the Algorithm base class,
after exec has been called, close to where we record history.
We would need to take care that this method cannot throw or allow exceptions to be thrown from it and executes very quickly.
It may be more efficient to send the AlgorithmHistory record rather than a pionter to the algorithm itself.

###Algorithm::SendUsage

In order to harmonise the code and keep things simple and easay to follow, this algorithm will be removed and the functionality added to the UsageService.
