Pull Requests for Testing Work in Mantid
========================================
There is a strong desire among the development team to move towards pull requests for verifying work done on Mantid. It is already being used to process changes from external contributors, and recent changes to Trac and Jenkins allows for opportunity to change the project's methodology for verifying work. This document is intended to outline the process in detail.

There are a couple of assumptions that are made in this new workflow:
* Trac will continue to be used for tracking work to be done in Mantid and demonstrate the status of milestones as they approach completion.
* To help guide developers to the pull requests, milestones will be replicated in Github, but they will be mostly just passthroughs to the original versions in Trac.
* The developers are professionals that can follow instructions and talk with each other when there are issues.
* As deemed appropriate, Trac tickets will be automatically updated to reduce the probability of errors from hand synchronization of information. However, the process detailed below should be such to make it easier to verify tickets.

Benefits of Pull Requests with Build Server Support
---------------------------------------------------
1. The `develop` branch no longer needs to exist. 
- Since the build servers will build each pull request individually (after merging locally to master), the pull request will be automatically annotated with the build results independent of all other issues. This gives the tester better certainty that the changes work on all supported platforms.
- The git workflow will be similer, and easier for developers to understand on a fundamental level
- The resources allocated to develop can be reassigned as they will not be required
1. Unification of verifying work between mantid developers and outside contributors. This will help spread the work load of processing outside contributions between more developers.

The Recommended Process
-----------------------
1. Work happens in Trac as usual. The developer accepts a ticket and works on it to completion on their local development machine. If something needs to be cross platform, then the developer can check out the same branch across multiple machines.
2. When the work is finished the developer looks at the branch on Github and presses the "compare and create pull request". This view will let the developer know whether or not it will cleanly merge to master. If it doesn't, they are responsible for merging master into their branch so it does.
3. Create the pull request. This should have a reasonable summary (can be copied from the Trac ticket), should contain a link back to the original Trac ticket for the full description, and have instructions for verifying it. There will be hooks on the Trac server to automatically create a link from the Trac ticket to the pull request and change the state to "verify".
4. If the pull request creator is on a white list, the builds will automatically start, otherwise one of the people on the white list will have to approve it. This is to reduce the exposure to malicious code in a pull request damaging build servers.
5. Jenkins will run the builds and annotate the ticket. If there are issues discovered by the build server, the developer should address them on the branch that the pull request was created from. The Trac ticket doesn't need to change state because the developer is diligent and confirms that the builds passed.
6. A tester will look at the list of open pull requests, discover work to verify, and assign the pull request to themselves. The Trac ticket will automatically update the state to "verifying".
7. Annotations on the pull request (e.g. comments about the code, references to created follow-on tickets, etc) will be added as comments to the Trac ticket. The Trac ticket will remain in the "verifying" state and the pull request will remained assigned. 
8. If the work was done sufficiently well. Merge into master and delete the branch.
9. If the work is not sufficiently done, comment and leave the pull request assigned and the Trac ticket in verifying. The developer will notice the email from Github and address any issues either by making additional changes or by commenting on the pull request. When the corrections are made the developer will comment on the pull request and work will repeat starting from step 7.

This recommended process is mostly a refinement of the existing process for much of the development team. The main changes are clearer information on the changes affects on builds and a clearer view of the conversation during verification. Tickets infrequently change testers through the process so keeping the pull request assigned is codifying this practice. 

We recommend that the new method is run in tandem with the exising one for the time being. They can coexist while we extend the trial to other developers. We suggest avoiding a sudden change. During this time `develop` will still need to exist.

Issues with Pull Requests
-------------------------
1. If a pull request requires changes in system tests, the link to that pull request needs to be done by hand. This is no different than current workflow in Trac.
2. Until the entire development team is using pull requests, some compromises will need to be made to keep the hybrid system running. Specifically: branches for pull requests will be merged into develop so it does not get out of sync with master.
2. The builds do not have good testing against system tests and may create issues in master after the pull request is merged. There does not appear be a solution to this other than developers paying attention to nightly clean builds being broken. There will be a build that takes all open pull requests and merges them onto master and does the full deep testing (usage docs, system tests, etc). This is currently under active development. A way to think of this is as a rolling develop, similar to paraview's `next` branch.
