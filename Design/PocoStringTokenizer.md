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
version of poco is available on their operating system.    

## Implementation possibilities

### Limit the allowed versions of Poco. 

In principle, we could require Mantid be build against Poco versions between 1.4.2 
(our current minimum version) to 1.4.7. Currently the ornl-mavericks and ornl-yosemite 
retain Poco 1.4.7 depite a newer version being available via homebrew. Similarly we could 
raise the minimum version to 1.6 (1.5 is a development release), but the supported platforms
are well behind the latest release.

### Different source code for each version.

We can use preprocessor statements to select the correct source code for 
different poco versions. If we limit changes to the wrapper Mantid::Kernel::Strings::parseRange,
this might be the simplest solution. Unfortunately, Poco::StringTokenizer is called directly
in many places, so this may not be a pretty solution. 

### Switch to a different library.

Poco::StringTokenizer is very similar to boost::tokenizer. Unlike Poco, boost::tokenizer
hasn't undergone large changes in ~8 years. Recently, [Poco::RegularExpression was replaced 
with boost::regex](http://trac.mantidproject.org/mantid/ticket/10603), create precedence
for changing libraries. 

## Recommendation

If we can rewrite the affected algorithms to use a wrapper, then preprocessor statements 
are probably the quickest solution. Otherwise, I suggest migrating the affected algorithms
to boost::tokenizer. 
