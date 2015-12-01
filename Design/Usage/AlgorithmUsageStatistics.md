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
* internal - true/false True if the interaction was not a direct response to user interaction (maps to alg.isChild()).

These would be sent in addition to several fields in common with the startup Usage details.  Take a look at the example json in the appendix for an example of a proposed message.


###New Code

####Kernel::UsageReporter

We would create a new class called UsageReporter which would be responsible for collating, and sending
all usage data.  This would centralise all the logic covering Usage Reporting including:

1. Detecting if repoting is enabled
1. Registering the startup of Mantid
1. Sending Startup usage reports, immediately, and every 24 hours thereafter
1. Registering feature usage, and storing in a feature usage buffer
1. Sending Feature usage reports on application exit, and when the feature usage buffer is above a size threshold.  This will need to be timed during development to ensure it does not add significantly to application shutdown.

###### Implementation Notes:
This class will be owned and served out from the ConfigService throu a new UsageReporter method.  The ConfigService will also be responsible for the setup and lifetime of the UsageReporter class.  This is beacuse the UsageReporter needs to send a data package as part of it's destructor and needs the ConfigSerivice to still be available when it does that.

The Usage report will have methods to :

1. set and get an enabled status
2. set the Application string, defaulting to "Mantidplot"
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
1. Internet calls (apart from the final one on application exit) will be down asynchronously on another thread the prevent thread.)
1. Failures in the reporter should not throw exceptions outside of the reporter, just log and accept any loss of usage data.

####Server side API

Clearly the django website https://github.com/mantidproject/webapp will need to be extended to accept feature usage reports.
These would be stored in a seperate table to the startup reports, as there will be somewhere in the order of 10-100 times as many feature usage reports as there are startup reports.

Initially we do not plan to define reports for the feature usage data, they will be queried direct from the database using SQL.
Once a good understanding of the usefull aspects of the data clarifies we will look to integrating some reports into the API.

#####Database size considerations

The current size of the gears instance we are using is roughly 300MB, of which the Sevices_Usage table (the startup usage table) is 30MB, when populated with roughly 1.5 years of data.  Given that we can expect 10-100 times as much data in the Features usage table then this will make the table 300MB to 3GB in size within 1.5 years.

The current free plan we use allows for 1GB of storage, however the Bronze plan allows for 1GB of free storage, followed by $1 per month for each additional GB (up to 30GB max).  Once we get near to the end of the free plan we would move to the bronze plan and pay the small fee.

The value of old feature usage data over 1 year rapidly diminshes, so we would plan to remove old data on a yearly basis.

###To Existing Code

####API::FrameworkManager

Currently the code to send usage reports is in the FrameworkManager (FrameworkManagerImpl::SendStartupUsageInfo).  This would be removed.


####Kernel::ConfigService

As described above this change would create a UsageReporter class which would be responsible for collating, and sending
all usage data.   This will be created, and owened by UsageReporter.registerStartup().
The config service will also delete the UsageReporter as the first step of its desctutor, when logging and all of the other ConfigService methods remain available.

###API::Algorithm

We would add a call to UsageReporter.registerFeatureUsage() within the Execute method of the Algorithm base class,
after exec has been called, close to where we record history.
This would simply record the information to be sent into a local queue object and return quickly.


###Algorithm::SendUsage

In order to harmonise the code and keep things simple and easy to follow, this algorithm will be removed and the functionality added to the UsageReporter.  As part of this the current hand crafted json creation will be repleaced using jsoncpp.

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
   "ParaView":0,
   "dateTime":"2015-11-30T16:22:35.270917000",
   "features":[  
      {  
         "details":"{\"name\":\"LoadParameterFile\",\"properties\":{\"Filename\":\"C:\\\\Mantid\\\\Code\\\\instrument\\\\GEM_Parameters.xml\"},\"version\":1}\n",
         "duration":0.25699999928474426,
         "name":"LoadParameterFile.v1",
         "start":"2015-11-30T16:21:44.460998000",
         "type":"Algorithm",
         "internal":true
      },
      { "_comment":".. more feature usage calls ..."  },
      ],
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
