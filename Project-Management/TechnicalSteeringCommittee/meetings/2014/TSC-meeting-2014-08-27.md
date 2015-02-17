Agenda
======
1. Actions from last meeting
2. Owen to discuss [Multi Period Workspace Groups issue and possible design choices](https://github.com/mantidproject/documents/blob/master/Design/MultiPeriodGroupWorkspace.md)
5. Ubuntu 14.04 in matrix build
6. Look over [skipped system tests report](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/SystemTests.md) - Pete
4. Discuss future of [tcmalloc](https://gist.github.com/martyngigg/39716a22b159e0918e48) - Martyn
5. Assign any outstanding pull requests
3. Owen to raise GUI testing (still unresolved)

Notes
=====
1. ACTION: Stuart to look into creating a generic mantid copr account. [EmbeddedInstrumentInfoNexus](https://github.com/mantidproject/documents/blob/master/Design/EmbeddedInstrumentInfoNexus.md) got approved
2. Owen has more work to do on filling in the design, but the preference is to not add another object to the workspace hierarchy.
3. Ubuntu 14.04 will replace 12.04 in the matrix build. Martyn at ISIS, Stuart at SNS
4. AI Pete modifies system tests so they can write out why they are skipped
5. AI Martyn modifies the linux startup scripts and modify the [etc scripts](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Build/CMake/LinuxSetup.cmake). TCmalloc is turned off for all compilations.
6. Done
7. AI Owen will set up a build job for his squish tests. AI Michael will send Owen information about the old squish tests.

Next meeting should be in one week.
