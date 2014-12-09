Agenda
------
* `clang-format` during the code freeze
* Potential for a clang matrix build (clang 3.4 vs 3.5, apple-clang)
* Revisit [nexus speed test results](https://github.com/OwenArnold/hdf5_vs_nexus/blob/master/read_results.md)
* Jenkins pull request builder plugin
* Agree on final strategy for pull requests
* Bluejeans for developer meeting
* Graphics within Mantid

Minutes
-------
Present: Stuart, Tobias, Peter, Ross, Martyn, Anders

* Do we want do also format branches? We should introduce a git hook to format before pushing.  The plan is to do it on Friday (PM-UK,AM-US) as this should be a low mark for the number of active testing tickets.  Ross had issues with `clang-format` (v3.5) in that it kept changing the files after multiple passes through the file. We will do this directly on master - Ross will do it.
* We will setup one to build master nightly - Peter
* It looks like the performance tests for LET indicate that files with larger number of items slow down much more using the NAPI.  LoadNexusLogs will be the first to be modified to test the improvements in using the HDF API.
* Concerns about the stability of the pull request plugin - especially with checking out.  
