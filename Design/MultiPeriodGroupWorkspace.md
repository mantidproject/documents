Multi Period Group Workspaces
=========================

Introduction
------------
Mutli period group workspaces (MPGW) are conceptually as special type of group workspaces (GW) a.k.a workspace groups. Group workspaces in general, define a loose grouping of any workspaces that may exist for any convenient purpose. MPGWs on the other hand are a more strongly bound collection of workspaces. 

* All logs are identical, except for the current period number
* The X-axis is identical both in terms of range and units
* The instrument is shared amongst all members

Problem
------------
Users working with 50 workspaces comprising a MPGW are finding that the workspaces are too large on disk when saved, take ages to load, bloat memory, and are inefficiently processed by Mantid.  Consider a MPGW of 50 workspaces in our current structure undergoing ConvertUnits and then SaveNexus, and you can see how inefficient our current mechnisms are.

This is primarily an ISIS problem, but it does seriously affect Reflectometry and SANS techniques.

Solution Objectives
--------------------

* Provide a good way to identify a MPGW so that algorithms can treat them differently, but allow the MPGW to be processed as a normal GW as a fall-back.
* Provide a lower memory overhead version of a GW, for example having a shared x-axis, instrument and run, but having independent y and e arrays for each member.
* Possibly as a separate step, handle the IO problems by having a file format which matches the above restrictions.


Candidate Solutions Ideas
--------------------------
* Keep existing structures, but look at fixing and optimising smart-pointer usage (cowp ideally) so that MPGWs have the same log objects. Probably the quickest route, but does not constitute a full solution. Will not tackle IO problem and each sub workspace still has a redundant x-axis.
* Address the loading/saving issue. This may be best done by introducing new load/save rountines if a good speedup can be made by restructuring.
* Recognise a new type of workspace in Mantid of MPGW (subtype GW) and keep end-user behaviour as close as possible to GW. Have a shared x-axis, run object and instrument. Have selected algorithms able to identify such workspaces and provide accelerated processing if desired.
* 

Decision based on TSC meeting 27th August 2014
-----------------------------------------------

* Make decisions based on profiling results
* Do not look at introducing a new workspace type at this stage
* Use profile guided optimisation. If loading is a problem, then load/save could be extended or adapted.
* Look at smart pointer usage to reduce log overhead. Pete also mentioned a x-axis factory.

