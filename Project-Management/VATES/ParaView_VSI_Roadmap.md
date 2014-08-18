Roadmap for ParaView-VSI Development
================================

There are a number of feature requests for the VATES Simple Interface (**VSI**) that are beginning to warrant a major change in the current user interface. However, it has been known that ParaView development has been steadily progressing away from the version (3.98.1) that Mantid currently uses. The parts of the ParaView code base that would be used for the changes have been changed over the subsequent released versions. There are also other pieces that the **VSI** relies on that are being marked as deprecated and subject to removal in ParaView versions that will be released within the next 6 months. As such, the technical debt being incurred by staying on the current ParaView release along with proposed changes has the potential to require significant resources in adjusting any changes to the **VSI** with a more up-to-date version of ParaView. Also, there is the intention of moving forward with more Kitware work which means that this will only be available to us in their git-master or the most up-to-date version. 

With this in mind, we need to move forward again on trying to bring the Mantid code base up-to-date with the current latest (4.1) version of ParaView. This was tried previously using ParaView built kits in the hopes of getting out of that business, but this met with disaster. Therefore, we have to get back into building our own kits as the first step in the process. ?We do need to settle on the question of what version. ParaView 4.2 is slated to appear in September 2014 with 4.3 around January 2015. Is git-master a viable option as ParaView follows a similar development model to Mantid? ? The proposal is to proceed as follows:

* Create permanent build jobs for ParaView kit creation (scripts to git)
  * Windows and OSX will run from Superbuild (start with git-master)
    * Currently 4.1 will not build on OSX with clang. 
  * RHEL/Fedora could be handled by using copr resources?
  * Ubuntu done as tarball?
* Create permanent build jobs for building ParaView for Mantid builds
  * The idea here is to make deployment to a new machine a bit easier
* Create new software collections for RHEL where necessary
  * This needs to happen to ensure old and new versions of software don't step    on each other.

Once the above is established, there is already a current [branch](https://github.com/mantidproject/mantid/tree/feature/7363_vates_paraview_git) that has (mostly) been kept up-to-date with Mantid and ParaView. This will be updated jobs made to run against it. Once stabilized, the branch will become the "master" for all subsequent work (maybe move to pv-next-master branch?). Should a develop type (pv-next-develop) branch be created from the master to provide similar development workflow? Jobs will need to be created for this, but shouldn't be too hard. 

After all the above has been carried out and found to be working, subsequent development for new features can begin.  
