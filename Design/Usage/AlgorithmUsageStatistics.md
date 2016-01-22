#Overview

We have several algorithms that are similar and would love to rationalise the code and make the choice of which algorithm to use easier for scientists.
However we always face the problem that we never know how much an algorithm is used.  It was agreed at the SSC2015 the we could track the usage of algorithms alongside simple startups of Mantid.

This design document should be considered as an extension of the previous implemented design [MeasureUsageStatistics](MeasureUsageStatistics.md).

#Requirements

##Must

1. Must record Mantid startup as is currently done.
2. Must record algorithm usage, in a flexible way that allows ad-hoc queries to be performed.
3. Must not significantly adversly affect Mantid interactive performance.
4. All tracking should be anonimised such that no user can be directly identified from the tracking information.  We will continue to use checksums of user names to prevent direct identification.
5. Failures in the reporting of usage must not affect wider Mantid activity.  Any failure may log information to the logging system, but that is all.  Usage data loss due to a failure is acceptable, and repeated attempts to send the data are not expected.

##Should

1. Should use the same opt out mechanism for usage reporting as the current startup reporting.
2. Should improve startup reporting to allow repeated usage calls for long running Mantid instances.
3. Should add in the capability to report how the framework was started (e.g. mantidplot or mantidpython). 
2. Other than above should not interfere with the current usage reporting.
3. All algorithm usage should be reported, both as parent or child, if possible how the algorithm is invoked (parent or child) should be recorded.  This is important in order to unserstand the absolute level of usage of an algorithm, but also if an algorithm is sloely used as a child algorithm we know that it is not externally known to end users.
6. Algorithms are one aspect of Mantid usage we want to track, but we may want to record other feature usages as well, such as Interface Usage (such as the Muon Interface startups), usage of specific features within an interface or Mantidplot (such as the Sliceviewer, or the beam centre finding within the ISIS SANS interface).
7. Algorithm and feature usages need to be linked to the version of Mantid, and optionally the OS version used.


 
##Won't - Will not be implemented, but considered for future development

1. Once commonly used queries are developed and understood for the algorithm and feature usage data, then we might add some reporting options to reports.mantidproject.org, until then reporting will be done via SQL queries on the database table directly.

** will not be implemented due to data size considerations ** 

4. 4. Some algorithms have various modes of operation and these are controlled by a "mode parameter", to allow usage of these modes to be tracked then the parameters of algorithms should be tracked if possible.
5. A small number of algorithms should have paramters that must be masked for security or truncated for performance.  Therefore MaskedProperties must be masked and long poprerties will need to be truncated.
6. The duration of execution of algorithms should be reported, this will allow us to track performance of Mantid in the real world.  If combined with Parameter recording this wold the development team to identify and address areas of poor performance that really matter.

## Possible Queries
The queries we perform an this data are likely to be discovered as we gather the data and mine it to answer questions in the future.  However for the benefit of this design here are some sample queries?

1. What algorithms have not been used in the last 2 releases?
2. What algorithms have not been directly executed in the last  release?
3. What algorithms are being used, but are not part of he Mantid standard installation?
4. Is the new algorithm , actually being used.


#Proposed Changes

We propose to Centralise the sending of all Usage reports into a central service, and extend the current functinality to 
allow usage reports of features within Mantid, where a feature might be:

1. Execution of an algorithm, parent or child
1. Startup of a Interface
1. Usage of a particular feature in an interface

Initially we would only intend to automatically track Algorithm usage, but other usage reports can be added by developer as they deem helpful.
The contents of a Feature usage would be:


* type - Algorithm, Interface, Feature
* name - Identifying name, for algorithms this would be Algorithm and version
* internal - true/false True if the interaction was not a direct response to user interaction (maps to alg.isChild()).
* Mantid_version - only the major and minor version (splitting on nightly versions will only complicate queries without particular benefit).
* count - the number of usages in this report

Take a look at the example json in the appendix for an example of a proposed message.


##New Code

###Kernel::UsageService

We would create a new service called UsageService which would be responsible for collating, and sending
all usage data.  This would centralise all the logic covering Usage Reporting including:

1. Detecting if repoting is enabled
1. Registering the startup of Mantid
1. Sending Startup usage reports, immediately, and every 24 hours thereafter
1. Registering feature usage, and storing in a feature usage buffer
1. Sending Feature usage reports on application exit, and when the feature usage buffer is above a size threshold.  This will need to be timed during development to ensure it does not add significantly to application shutdown.

The public methods of the UsageService will be exposed to python.

##### Implementation Notes:
This class will be owned and served out from the FrameworkManager.  The FrameworkManager will also be responsible for the setup  and will be shut down as part of the FrameworkManager Shutdown method. 

The Usage report will have methods to :

1. set and get an enabled status
2. set the Application string, defaulting to "MantidPython" and will be overwritten by Mantiplot in the MantidPlot startup code.
3. Record the startup of Mantid
4. Record Feature Usages
3. flush the feature usage buffer
4. set the interval for checking if time based jobs need to be done.

Other Notes :

1. Use Poco::Timer to handle the timed aspects of the class
  1. The 24 resend of startup data
  1. Checking every n minutes if the feature buffer above the threshold for sending.
1. Registering Feature usage must be fast, just create the record and return.
1. Do not lock the feature usage buffer for any longer than is absolutely necessary.
1. Use a queue, rather than a vector for the feature usage buffer.
1. Internet calls should use the InternetHelper.
1. Internet calls (apart from the final one on shutdown) will be down asynchronously on another thread the prevent thread.
1. Failures in the reporter should not throw exceptions outside of the reporter, just log and accept any loss of usage data.

###Server side API

Clearly the django website https://github.com/mantidproject/webapp will need to be extended to accept feature usage reports.
These would be stored in a seperate table to the startup reports, as there will be somewhere in the order of 10-100 times as many feature usage reports as there are startup reports.

Initially we do not plan to define reports for the feature usage data, they will be queried direct from the database using SQL.
Once a good understanding of the usefull aspects of the data clarifies we will look to integrating some reports into the API.

####Database size considerations

The current size of the gears instance we are using is roughly 300MB, of which the Sevices_Usage table (the startup usage table) is 30MB, when populated with roughly 1.5 years of data.  As this table is only storing summary data it's size will be inconsequential.

The current free plan we use allows for 1GB of storage, however the Bronze plan allows for 1GB of free storage, followed by $1 per month for each additional GB (up to 30GB max).  Once we get near to the end of the free plan we would move to the bronze plan and pay the small fee.

The value of old feature usage data over 1 year rapidly diminshes, however as this data will be very small there is no plan to remove old data.

####Tables
This will create a new table to store feature usage with the following structure:

FeatureUsage

* type VARCHAR(10) - Algorithm, Interface, Feature
* name VARCHAR(80)- Identifying name, for algorithms this would be Algorithm and version
* internal BOOL- true/false True if the interaction was not a direct response to user interaction (maps to alg.isChild()).
* Mantid_version VARCHAR(4) - only the major and minor version (splitting on nightly versions will only complicate queries without particular benefit).
* count INT - the number of usages, if the number passes the MAX the number will remain at MAX.

The type column could potentially be normalised to a seperate table, but given the size of the table and data it is an unnecessary complication.  The primary key of the table will be a compound key of (type,name,internal,mantid_version).

##To Existing Code

###API::FrameworkManager

Currently the code to send usage reports is in the FrameworkManager (FrameworkManagerImpl::SendStartupUsageInfo).  This would be replaced by calls to the Usage Service.
The FrameworkManager will also delete the UsageService as the first step of its shutdown method, when logging and all of the other ConfigService methods remain available.

##API::Algorithm

We would add a call to UsageService.registerFeatureUsage() within the Execute method of the Algorithm base class,
after exec has been called, close to where we record history.
This would simply record the information to be sent into a local queue object and return quickly.

##Algorithm::SendUsage

In order to harmonise the code and keep things simple and easy to follow, this algorithm will be removed and the functionality added to the UsageService.  As part of this the current hand crafted json creation will be repleaced using jsoncpp.

#Apendix
##Json for startup calls
``` json
{  
   "ParaView":0,
   "application":"mantidplot",
   "dateTime":"2015-11-30T16:20:39.060539000",
   "host":"df2545f221f5cecc6752219e1716384a",
   "mantidSha1":"a2c602fb1f8cb339abed583bc1e3e6af992ea9db",
   "mantidVersion":"3.5.20151127.836",
   "osArch":"AMD64",
   "osName":"Windows NT",
   "osReadable":"Microsoft Windows 7 Professional",
   "osVersion":"6.1 (Build 7601: Service Pack 1)",
   "uid":"114ede53ec4e133a0d637f889ef8764d"
} 
```
##Json for feature usage calls
Note: This has an almost identical header than that of the startup calls.
``` json
{  
   "features":[  
      {  
         "name":"LoadParameterFile.v1",
         "count":"47",
         "type":"Algorithm",
         "internal":true
      },
      {  
         "name":"Muon Analysis",
         "count":"2",
         "type":"Interface",
         "internal":false
      },
      { "_comment":".. more feature usage calls ..."  },
      ],
   "mantidVersion":"3.5"
} 
```

Approved [2015-12-09](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/meetings/2015/TSC-meeting-2015-12-09.md)
