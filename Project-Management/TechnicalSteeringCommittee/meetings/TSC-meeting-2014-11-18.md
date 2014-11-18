Agenda
======
* Linode maintenance - Jenkins backup (Martyn)
* Adding ESS to Slack
* Update Poco on Ubuntu (Martyn)
* Consider different JSON parser, [jsoncpp?](https://github.com/open-source-parsers/jsoncpp). There is a showstopping bug in boost version on RHEL6 - (Martyn)
* Brief chat about http://trac.mantidproject.org/mantid/ticket/10501. (Owen)
* F20 testing update (Ross/Pete)
* Statistics server update [link](http://django-mantid.rhcloud.com/) (Pete)
* HDF5 vs NeXus API performance (Owen/Pete)
* Visual Studio 2013 Community (Stuart)

Minutes
=======
 * We should login regularly and run updates regularly (i.e. apt-get dist-upgrade).  Also we need to update the jenkins configuration.  ACTION: Martyn will have a look to see if there is any sensitive information in the config dump.
 * Everyone agreed to add the ESS domain to allowed slack users (@esss.se)
 * Problem with Poco version on Ubuntu that prevents https downloading.  The version on debian is very out of date, and this problem has been fixed in newer versions (even on RHEL!).  ACTION:  Martyn will rebuild Poco 1.42 (same version as Fedora/RHEL) for ubuntu and put into the ppa.
 * We decided to start to use JSONCPP for parsing JSON rather than upgrading Boost.  ACTION: Martyn will build for Windows and Mac Intel.  ACTION: Stuart will try and rebuild for RHEL6 on COPR.  A formula exists for homebrew.
 * Discussion of [link](http://trac.mantidproject.org/mantid/ticket/10501):  Everyone thought this was a good idea to move forward with.
 * ACTION: Stuart to repackage Paraview 3.98 as a Software Collection for Fedora 20.
 * Pete has a draft of the JSON format.  He is planning to use OpenShift and Mathieu has offered to provide some UI and plotting for django.  The code is [here](https://github.com/mantidproject/webapp/).
 * Owen has a repo under his account [link](https://github.com/OwenArnold/hdf5_vs_nexus/).  The perfomance results are in this repo from running on Owen's and Pete's machines.  The results seem counter intuitive so far.  The tests need to be fleshed out more.  Other people who know the HDF5/NAPI should have a look at the code.
 * Everyone agreed it was a good idea to move to VS 2013.  For people who want to develop non-OSS software (i.e. ISIS people) they would need 2013 Standard/Pro.  The would reduce the cost drastically for ORNL.  We will plan to move to VS2013 during the maintenance period after the release.
  * [ ] ACTION: Stuart will test building with VS2013 against the existing 3rd Party.  
 
