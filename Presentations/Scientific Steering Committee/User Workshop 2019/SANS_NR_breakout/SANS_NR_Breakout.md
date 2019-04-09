Mantid User Workshop 2019
===

Meeting minutes from the SANS and Reflectometry breakout sessions on Thursday 11th and Friday 12th April.


Attendees
---------
- Jos Cooper (ISIS) - chair
- Gemma Guest (ISIS) - secretary
- Ricardo Ferraz Leal (SNS)
- Roman Tolchenov (ISIS) (day 1 only)
- Nick Draper (ISIS)
- Gagik Vardanyan (ILL)
- Igor Gudlich (ESS) (day 1 only)
- Verena Reimund (ILL)
- Thomas Saerbeck (ILL)
- Max Skoda (ISIS) (day 2 only)
- James Lord (ISIS) (day 2 only)

Workbench
---------
- Not used in production yet. ISIS SANS GUI only recently ported so not had much testing. ISIS reflectometry GUI not ported yet and reflectometry also require slice viewer before they can move to Workbench.

Slice viewer / MD data
----------------------
- Consenus that requirements will include visualisation of multi-dimensional data, selecting ROIs and masking.
- TS: For 80% of experiments, basic requirements are a 2D tool to select a region and to be able to project along one of the axes.
- JC: Would like the ability to script modification/duplication/sectorisation of shapes, and to create multiple ROIs and save them as different workspaces.
- SK: Possible overlap with fibre diffraction?
- **ACTION** JC and GG to come up with mockups for the required interface as a starting point for further discussion.

Roadmap
-------
- JC: 2D detectors are main focus for reflectometry at ISIS
- TS: faster (sub-second) time slices. Kinetic measurements. Different measurement techniques (rainbow) - waiting on detector technology.
- SK: Big things coming are SESANS and polarization analysis for ZOOM.
- RFL: Problems storing uncertainties for 2D data - need new workspace type until using Dataset is practical (IG: Can put together demos of dataset if people contact him with examples). Also need to rewrite workflow algorithms to provide output at every child step and better errors. 

Stability
---------
- Overall seems much improved, although JC still seeing crashing every 1 or 2 days when running live data and scripts continuously.
- MS: INTER also still experiencing problems with slow down/leaks.
- ND: Recent fix for very long logs could help.
- **ACTION** New ISIS support person (when recruited) to investigate instability/slow-downs with long-running instances.
- SK: Problems with size and speed of saved project files - can cause crash if fills disk. Reduction speed is improved with the new backend but could still be better. 
- **ACTION** Devs to investigate adding warnings when saving large projects and/or option to save the project as a script.

IDFs
----
- JC: Problems knowing which IDF is associated with a run. Should we embed the IDF in the nexus file?
- JC: Problem defining absolute positions (cumulative errors).
- **ACTION** ND and GG to set up meeting to discuss options.

User community
--------------
- RFL: Users don't like scripts. Want GUI and drag-and-drop from spreadsheets. Scientists use a range of different tools. Could move to autoreduction if we think ahead when set up experiment (can always change options and re-reduce). Not all users go away with reduced data. 
- SK: Same GUI used by 4 instruments. Enter data manually or in spreadsheet and batch reduce. Users do the reduction themselves and most go home with at least some data reduced but also take the raw data. User file and spreadsheet mean that it is reproducible.
- TS: Pre-mantid: users do the reduction and take reduced data home. Raw data available on the cloud. Some want GUI and spreadsheet, others prefer scripts for reproducibility.
- JC: 5 instruments. Some use GUI, one uses jupyter notebooks, 1 uses python scripts written by scientists (not tested but easy to call for users).

Developer interactions
----------------------
- Recent trial support role at ISIS looked promising but responses (e.g. to error reporter) have been poor recently due to resourcing problems - recruitment is under way for a new support person. Potential for the QA role to expand further in future if this is a success.
- Some confusion over best way to report problems - the forum is now the recommended way. The old help email can still be used but will now forward to the forum (this should make it easier as it avoids needing a login).
- **ACTION** devs to investigate ways to notify interested parties (other than submitter) when changes go into nightly (e.g. categorised weekly github summary). Mixed feelings about whether this would be looked at.

