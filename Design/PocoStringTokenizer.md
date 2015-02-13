## Motivation

Poco::StringTokenizer was [rewritten in version 1.5](https://github.com/pocoproject/poco/commit/67a27ac2fa64fca56931326b56d49224a1d56839)     
to treat all empty tokens equally. In earlier versions, the last empty element is a special case. 
Unfortunately, this new behavior breaks the following unit tests. 

* KernelTest_StringsTest
* GeometryTest_FitParameterTest
* DataHandlingTest_GroupDetectors2Test 
* DataHandlingTest_LoadRKHTest 
* CurveFittingTest_FitMWTest

Fixing these errors will break 
unit tests on systems running earlier versions of Poco. 

## Requirements

We need to find a solution that provides a consistent experience for our users regardless of which 
version of poco is available on the user's platform.    

## Implementation possibilities

### Limit the allowed versions of Poco. 

In principle, we could require Mantid be build against Poco versions between 1.4.2 
(our current minimum version) to 1.4.7. Currently the ornl-mavericks and ornl-yosemite 
retain Poco 1.4.7 depite a newer version being available via homebrew. Similarly we could 
raise the minimum version to 1.6 (1.5 is a development release), but the supported platforms
do not yet include this release.

### Different source code for each version.

We can use preprocessor statements to select the correct source code for different poco versions. 

### Switch to a different library.





## Actions
