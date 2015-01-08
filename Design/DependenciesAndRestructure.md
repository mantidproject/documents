# Dependencies and Restructring of the Mantid Project

## Motivation

The current structure of Mantid is heavily based on a plugin mechanism. The design implies that only core aspects of the framework (Kernel, API, Geometry, DataObjects). Other aspects of the framework are plugins, and should neither export symbols, or be interdependent on each other in any way. 

There are major problems that need to be addressed with the current Mantid project structure. Firstly, there are soft, run-time dependencies between different packages, which are in no way mirrored by the complile time dependencies. These soft dependencies are invisible to the build system and can cause run-time failures, and could even lead to deployments of mantid which are faulty based un tested execution paths. The second issue is that many of the compile time dependencies on each package are completely uncessary. This is likely to be negatively affecting build times, and will make the final binaries larger than is required.

### Run-time dependency issue

Using the dynamic factories, and run-time dll loading, we have created a framework which is very extensible. Stock Algorithms and Fit Functions are brought into Mantid in this manner. User provided Algorithms can also be built against the framework and then picked up by Mantid in the same way.

Unfortunately, the flexibility comes at a cost. We are increasingly finding that plugin packages suppling one Algorithm, actually look for and use another Algorithm during execution. Many algorithms in Crystal for example depend on those in Algorithms. WorkflowAlgorithms has no dependency on Algorithms pacakge, but several Algorithms such as MuonLoad and DgsConvertToEnergyTransfer within the WorkflowAlgorithms pacakge use Rebin from the Algorithms package. My findings can be derivided using the --graphviz option on CMake, and a simple grep of the source files. 

**I suggest we introduce a new package, called AlgorithmsCore. For and existing packages which contains and Algorithm which is used outside that plugin package should have that Algorithm moved into AlgorithmsCore. There should be a compile-time dependency on any package set up to AlgorithmsCore to make the relationship explit. Rebin, for example should move to AlgorithmsCore on this basis. Since mantid uses the catagories field rather than the hosting package for it's organisation of algorithms, the results should have not determental effects on what the userability and apparent user-facing organisation of all algorithms.**

### Compile-time dependency overuse

Running cmake with the --graphvis option demonstrates how many dependencies our leaf targets are unnecessarily linking against. For example, Algorithms is linked against PocoNetSSL, but actually has no dependency on it at all. The only reason this happens is by because somewhere further up the chain the dependency is required.

**As of cmake 2.8.11 we have new options when we run target_link_libraries, PUBLIC, PRIVATE and INTERFACE. We should use PRIVATE as much as possible, since PUBLIC is currently being assumed.**

**We should also make attempts to control library visibility for all plugins. No plugins should export symbols. Later versions of cmake have the flag CMAKE_CXX_VISIBILITY_PRESET  to control this.**

### Code reorganisation

Other than some suggested code movements around the plugins, it may be desireable to reorganise other aspects of the code/code-base.

* Introduce a top-level CMakeLists.txt file in the project root directory
* MantidPlot: Extract Instrument View, refactor ApplicationWindow
