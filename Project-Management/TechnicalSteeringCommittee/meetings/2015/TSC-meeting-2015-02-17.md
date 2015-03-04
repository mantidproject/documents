Agenda
======

1. Peformance tests. Average commit statistics (Owen Arnold)
1. Assign tasks to move non-vates portions of Mantid to be able to compile with Qt 5
1. [Andrei's Python Algorithms Proposal](/Design/pythonAlgorithmsForMDEvents.rst)
1. [Steve's string tokenizer proposal](/Design/PocoStringTokenizer.md)
1. Federico's observation on Load Nexus algorithms. Should we monitor the frequency of edits of each file as sign of potential code degradation (Anders)
1. Design signoff spreadsheet? (Anders)
1. git-clang-format – comments to its use in c++ coding standards wiki
1. IDL version 2 (Anders)
1. Add cppcheck to "pull request" build? (from developer meeting)
1. Human interface guide (from developer meeting)
1. Best practice for changing rst files. Should common sense apply or should we write a guide (from developer meeting)
1. How TSC advertise itself better (from developer meeting)
1. Planned work on Multiple scattering #11106 (Anders) (SSC ticket #8926)

Minutes
=======
Present: Anders, Martyn, Stuart, Pete, Ross
Also attending: Steven, Andrei

1. Moved to next meeting as Owen not present
1. Moved to later meeting as not as high priority as other items
1. Martyn raised the question of merging MDEvents & DataObjects before looking at this. It was accepted as a good idea.
    * ACTION: Martyn will look at whether the proposed api for the objects makes sense
1. It was agreed that this would be a good opportunity to abstract the tokenizer behaviour behind our own Kernel::Strings to avoid furture problems such as this.
    * ACTION: Steven H. to look at this.
1. Federico's comments were discussed and it was agreed that the initial low-quality of the code is as big a factor in perceived degradation from changes. It was decided that the work 
to track these measures would not be valuable enough to warrant.
1. ACTION: Anders will look at starting a report for tracking design proposals.
1. The links are already on the wiki so no action needed.
1. ACTION: Anders to start a (long-running) design document for IDF v2
1. ACTION Martyn to add static analysis jobs to Ubuntu pull_request build
1. Moved to next meeting
1. Moved to next meeting
1. Moved to next meeting
1. Moved to next meeting
