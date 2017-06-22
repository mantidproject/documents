<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. User Meeting Large Scale Structures Minutes</a>
<ul>
<li><a href="#sec-1-1">1.1. Monday 12th June 2017</a>
<ul>
<li><a href="#sec-1-1-1">1.1.1. Attendees</a></li>
<li><a href="#sec-1-1-2">1.1.2. Feedback regarding the user meeting</a></li>
<li><a href="#sec-1-1-3">1.1.3. User files</a></li>
<li><a href="#sec-1-1-4">1.1.4. Autoreduction</a></li>
<li><a href="#sec-1-1-5">1.1.5. Plotting</a></li>
<li><a href="#sec-1-1-6">1.1.6. X error bars</a></li>
<li><a href="#sec-1-1-7">1.1.7. Simplifying Mantid</a></li>
<li><a href="#sec-1-1-8">1.1.8. Analysis</a></li>
<li><a href="#sec-1-1-9">1.1.9. Keep/make-current</a></li>
<li><a href="#sec-1-1-10">1.1.10. Python API</a></li>
</ul>
</li>
<li><a href="#sec-1-2">1.2. Tuesday 13th June 2017</a>
<ul>
<li><a href="#sec-1-2-1">1.2.1. Attendees</a></li>
<li><a href="#sec-1-2-2">1.2.2. Python API</a></li>
<li><a href="#sec-1-2-3">1.2.3. Algorithm renaming</a></li>
<li><a href="#sec-1-2-4">1.2.4. Download size</a></li>
<li><a href="#sec-1-2-5">1.2.5. Support</a></li>
<li><a href="#sec-1-2-6">1.2.6. Community/analysis</a></li>
<li><a href="#sec-1-2-7">1.2.7. Slice viewer</a></li>
<li><a href="#sec-1-2-8">1.2.8. File storage</a></li>
<li><a href="#sec-1-2-9">1.2.9. Q resolution</a></li>
<li><a href="#sec-1-2-10">1.2.10. Misc</a></li>
<li><a href="#sec-1-2-11">1.2.11. Reflectometry tickets</a></li>
<li><a href="#sec-1-2-12">1.2.12. SANS github tickets</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>


# User Meeting Large Scale Structures Minutes<a id="sec-1" name="sec-1"></a>

## Monday 12th June 2017<a id="sec-1-1" name="sec-1-1"></a>

### Attendees<a id="sec-1-1-1" name="sec-1-1-1"></a>

-   Andrew Jackson, SANS at ESS (also an occasional user at ISIS)
-   Chris Stanley, EQ-SANS at SNS
-   Steve King, LOQ and sometimes Sans2d at ISIS
-   Stephen Cottrell, Muons at ISIS
-   Anton Piccardo-Selg (Mantid developer at ISIS)
-   Gemma Guest (Mantid developer at ISIS)
-   Nick Draper (Mantid project manager at ISIS)
-   No representatives from reflectometry.

### Feedback regarding the user meeting<a id="sec-1-1-2" name="sec-1-1-2"></a>

-   Scientists had late notice of workshop and registration process.
-   SC tried to organise pre-meetings ith team leaders and provided questions, but this was not fed down. Suggests emailing scientists individually in future.
-   AJ Regular group meetings happen at ESS anyway. Suggests providing structure for pre meetings and chase people.
-   AJ and ND suggested that it's hard to encourage people from ESS and ILL to come because they are only in the first stages of using Mantid. However, it is still important for people to be involved.
-   AJ: the user workshop is a good opportunity to tell each other what [algorithms etc.] we've been working on
-   CS: this meeting is a good break from the day to day business where we can focus on sharing things we've been working on. We aim to do it anyway but it tends to fall by wayside.

### User files<a id="sec-1-1-3" name="sec-1-1-3"></a>

-   CS We don't have a settings file but can save & reload. We have a config file with .<run<sub>number</sub>> but this is primarily for masking.
-   AJ Would like to save state from GUI rather than have user file. Not mission critical.
-   All dislike current user file format and would like improved format e.g. json or yaml, and something that can be modified programatically. Want to be able to generate user file from GUI rather than writing by hand.
-   SK Will probably aim for better way than current user file format for ZOOM.
-   AP Saving state is also a requirement for reflectometry. Richard has some ideas on a new format for the user file

### Autoreduction<a id="sec-1-1-4" name="sec-1-1-4"></a>

-   CS This keeps coming up. Some users come up with their own autoreduction. Have some settings saved but have to tell users where to load it.
-   SK Can't see way of totally automating. Batch reductions create too many workspaces - cleanup is better than before but room for improvement e.g. remove diagnostic files. Want to keep transmissions but this could all go in a subfolder/group.
-   AJ If the option to output to disk is on, could there be an option to clear up completely (e.g. if using on a laptop). Although if plotting were nicer, would probably use Mantid instead of outputting.
-   ND More cleanup would be good, especially in simple mode where you may not even see the workspace list. We can also use workspace groups to keep things cleaner.
-   CS After running overnight users can get lost if there are too many workspaces.

### Plotting<a id="sec-1-1-5" name="sec-1-1-5"></a>

-   SK Would like to be able to show instrument for several nexus files at once (say 6 to 12 typically; possibly up to 50) and simultaneously vary contour level. Currently have to crop and save each image separately for publications. Would also want the same colour scale.
-   ND Could be a performance issue (~2 secs each) but this could be improved to some extent. Could probably save images via a script.
-   AJ It would be good to be able to apply plot preferences to a series of plots.
-   CS Could we have different defaults for 2D vs 1D plots?
-   ND 2D plots should have a different set of settings to 1D plots though some preferences will apply to both.
-   SK Could we have technique specific graph legend placement, e.g. for SANS, top right corner.
-   ND A legend placement preference would be good.

### X error bars<a id="sec-1-1-6" name="sec-1-1-6"></a>

-   AJ Incorrect to represent resolution as error bars. Ultimately want to write out for use in analysis. May not need to carry around in Mantid. Resolutions more of an issue with long pulses (ESS). Some estimate is better than none. Don't know good way to represent it. Plot the resolution function e.g. to see the effect of the binning scheme. Not relevant for users. QResolution needs to be able to store arbitrary resolution function in the future.
-   ND We store and carry around info in workspaces as a single value. Can draw X errors. Have not done work to pass them through to the graph for SANS. Error bars possibly not the best way to draw it. May not need in workspace unless want to visualise. Could just do in save step? We need to ask reflectometry whether it's correct to show as error bars. More correct as a histogram?
-   SK Currently have a known equation for calculating the resolution.

### Simplifying Mantid<a id="sec-1-1-7" name="sec-1-1-7"></a>

-   AJ No problems for us but some instrument-specific interfaces could be designed better (too fussy). In Mantid 4 could we go through all interfaces and identify what functionality is for edge cases (ND: out of scope to simplify all interfaces for Mantid 4.0).
-   SK We turn off icons for users. We need diagnostics but could hide this for users. The logging tab on the SANS interface can be removed. 1D analysis tab can also probably go.
-   CS Things are ok but a basic mode would be good.
-   SC A simple mode for new users would be good but switching to full mode once familier.
-   ND Debug options on interfaces could also be off in simple mode (i.e. have one option to control this)

### Analysis<a id="sec-1-1-8" name="sec-1-1-8"></a>

-   CS Users get data reduced before they leave and do analysis after they leave. Could we do more analysis while in progress?
-   SK/AJ General analyisis is performed via SASView but better analyisis features via imported SASModels might be good
-   AJ Piping to SASview seems to be not working (potential issue with SasView on Windows).

### Keep/make-current<a id="sec-1-1-9" name="sec-1-1-9"></a>

-   AJ Like drag-and-drop. 90% of time want to compare plots. Default of overwriting would be annoying. However in the GUI would like overplot.
-   SK Plot result on batch reduction is off by default or you get loads of windows.
-   AJ/CS 'replace' option not wanted.
-   CS Need to be cautious about a change in the way Mantid works.

### Python API<a id="sec-1-1-10" name="sec-1-1-10"></a>

-   CS We export from UI to create scripts for batch runs and this can evolve, so old scripts could be problematic. But generally based on history => sequence of algorithm calls. We generate multiple scripts per experiment.
-   SK Users not affected. Main worry is if changes need beta testing in Feb/March (busy with end of winter shutdown & neutron training course).
-   SC Testing and deployment should be group determined.
-   ND Yes, this won't fit into a standard release cycle.

## Tuesday 13th June 2017<a id="sec-1-2" name="sec-1-2"></a>

### Attendees<a id="sec-1-2-1" name="sec-1-2-1"></a>

-   Andrew Jackson, SANS at ESS (also an occasional user at ISIS)
-   Chris Stanley, EQ-SANS at SNS
-   Steve King, LOQ and sometimes Sans2d at ISIS
-   Stephen Cottrell, Muons at ISIS
-   Max Skoda, Reflectometry at ISIS
-   Anton Piccardo-Selg (Mantid developer at ISIS)
-   Gemma Guest (Mantid developer at ISIS)
-   Pranav Bahuguna (Mantid developer at ISIS)

### Python API<a id="sec-1-2-2" name="sec-1-2-2"></a>

-   MS Not directly using core algorithms (used via higher level algorithms). Clear boundary between base level and higher level but not clear which are which. Workspace calls are used occasionally but we've gone away from that primarily. It would be good if you don't have to import stuff that you won't use.

### Algorithm renaming<a id="sec-1-2-3" name="sec-1-2-3"></a>

-   AJ: Objection to bundling reactor methods into one box and about facility-specific then instrument-specific levels. Would prefer to keep techniques close to each other rather than facilities.
-   SC: How do we keep track if people are creating quick experimental functions?
-   AJ: Making the metadata on algorithms richer might be helpful

### Download size<a id="sec-1-2-4" name="sec-1-2-4"></a>

-   MS Noticed that Mantid's size on disk has increased a lot.
-   AP Other stuff is shipped with it, e.g. paraview.
-   SK/MS/AJ Would like to be able to select the requried components in the installer or have a slimmed down installtion for a particular instrument.
-   AJ Sourceforce downloads are very slow.

### Support<a id="sec-1-2-5" name="sec-1-2-5"></a>

-   MS Support is ok but continuity is a problem (2 staff changes recently).
-   GG We're trying to address this with knowledge sharing in sub-teams.
-   AJ Only 1 or 2 people doing everything for ESS?

### Community/analysis<a id="sec-1-2-6" name="sec-1-2-6"></a>

-   CS We've always used Mantid on EQ-SANS and are trying to fold in other SANS instruments. Users use SANS GUI for almost everything. Scientists use Mantid more (testing etc.)
-   SK SANS users generally happy but grumble sometimes about performace. Doesn't think they have a feel for the size of data they are working on. Only 1 or 2 users use the scripting interface; most use the GUI.
-   AJ Would need more good worked examples if you want to encourage more use of scripting.
-   MS Users should be shielded from scripting by the scientists.
-   SK Some users shouldn't be allowed to use scripting!
-   MS ~90% of users (INTER) happy with autoreduction and just use Mantid for plotting. They don't use GUI/scripts much except to tweak values. Autoreduction not used on all reflectometry beamlines yet. Aim to have this as a button on the GUI. The autoreduction script saves to the user directory. The way data is recorded has to be in a suitable format e.g. title so you can identify the correct runs. There's also a script to automate this formatting. Users just set the title once. In theory should be able to set this from nexus but haven't got this to work and it's also slow to load the file - loading titles from ICat is fast, but doesn't work reliably. Could ICat be modified to return other file attributes quickly? Users like the current setup but colleagues on other beamlines like to fiddle - not sure why!
-   SK/CS No users do analysis in Mantid (not a complaint!). MS agrees.
-   CS Did have ability to run SasView side by side on linux, but this no longer works.
-   MS We don't need hard core analysis in Mantid, just some tools to check data.
-   CS Yes, useful for diagnostics.
-   SK Simple linearlisation type functions useful. Functionality is there but that tab in the GUI has not been developed further.
-   MS Fit functions more complicated. Analysis tools used include Rascal, GenX, MotorFit and many others (all very similar); the reflectometry community hasn't converged. Typically export 4 column ASCII data, which these tools can use. We'll have more off-specular data in future and will want to manipulate this more before fitting.
-   SK/MS All users use Mantid for reduction.

### Slice viewer<a id="sec-1-2-7" name="sec-1-2-7"></a>

-   SK Would like to be able to draw region in slice viewer and integrate. Slice viewer has an unintuitive interface. Integrated intensity against angle. There are some tickets regarding this. In SasView can only do it on reduced data. Advanced cutting features in SliceViewer (MS wants this too): Annular cuts for example.
-   MS When we have 2D detectors we will also want to define regions like this. Define sector as well. Fit2D has a lot of those sort of features.
-   CS Our group doesn't use slice viewer.

### File storage<a id="sec-1-2-8" name="sec-1-2-8"></a>

-   SK: Everything we have, reflectometry will need, ie flat cell files, detector pixel efficiency files, pixel mask files, etc (things that the ISIS SANS user file slurps in unknowingly to users) . As reflectometry adds 2D detectors these things will become important.
-   MS: Need some way of storing and datestamping this info. Changing and datestamping IDF or params file is a nightmare. ICat should allow us to upload files but doesn't seem to work. But that would allow users to download remotely - favoured solution would be a web interface. A good thing about ICat is that it limits access by user.
-   SK/AJ: SANS stores on archive of instruments (on network). Separate folder for user files. Some stored locally for speed. Could store in nexus file and cart around with data.
-   AJ: User needs to remember to take mask file away with the files it references. Also some issues with getting the path correct.
-   SK: Files can change from experiment to experiment and it's easy to pick up the wrong one. The name extends over several lines in user file.
-   AP: We won't have an all-in-one file, but the algorithm could point to the user file which could extract all of the dependencies to a directory.
-   MS: Our users go away with reduced ASCII data. Rare they want to re-reduce and if so they ask scientists.
-   SK: We give them the user file with default conditions. They go away and start to model fit it and may want to rebin or something or decide they want 2D data.
-   AJ: Some users do it more often but maybe we should focus on getting them the right answer first time. Not sure how long users will be able to process on their own machines anyway due to performance.
-   CS: We have a remote analysis cluser available via analysis.sns.gov. We keep a series of directories from each cycle with flood/mask files. Paths never change. Reduction never needs changing and you can reprocess remotely through a browser (like VNC). Ricardo has web interface.
-   MS: We'd like to aim for this. What you want to get out is a small 1D file. Processing quite involved though so good to do that server side.
-   AJ: Will probably end up wanting to store user file data with processed data in a standardised location with a standardised name. all data including masks etc. needs to be available to be reprocessed. If you change settings in user file it needs to be rewritten back to user file. (MS Same for reflectometry GUI)
-   AP: History is saved (it's just getting it back into the GUI)
-   CS: When you open a file, does this repopulates the GUI? Stored in processed nexus file? Can then click to see history and copy to clipboard and paste into a script to use? (Although not sure as usually using recently reduced workspaces so there anyway)
-   AK: Need some thought about what gets written to nexus file. User file name currently exported but not changed when settings in GUI are updated. SANS reduction saves reduced data to bat file? But not raw data. Important thing is to avoid divergence between what was actually done to data and what was nominally done (relying on user file being correct). Or have version control of user files, but that gets hairy.
-   AP: Mentioned yesterday move to yaml or something for user file. Could be joint effort with reflectometry (MS agrees).
-   SK: Much content would actually be similar.
-   MS: Transmissions are per experiment rather than per sample. Will move more towards the things SANS have.

### Q resolution<a id="sec-1-2-9" name="sec-1-2-9"></a>

-   MS: In reflectometry we are now starting to worry about Q resolutions. Need to chat to SANS(SK) about this. AJ would like to be kept in the loop.
-   AJ: Currently pretend final resolution is gaussian. Long term go to more complex description of resolution. Mentioned a paper published by David Mildner & Jack Carpenter in the 80's.
-   AJ: Discussion has been for 1D data. For 2D data another kettle of fish.

### Misc<a id="sec-1-2-10" name="sec-1-2-10"></a>

-   AJ: reduction compute at ESS will need to be near file store. Lots of things not worth doing until after GUI refactored - need to make sure not doing work that would be wasted effort.

### Reflectometry tickets<a id="sec-1-2-11" name="sec-1-2-11"></a>

-   The current list of SSC tickets is not very up to date. We should close the ones not valid.
-   15052 from ISIS. Relates to sum in Q (purely specular reflection on linear detector)
-   9771 "everywhere" a strong term. Relates to harmonisation of instruments.
-   MS: QuickNXS probably an SNS thing; and REFL #12148 too?
-   MS: SNS relflectometry use mantid but in very different ways. May be worth presenting our GUI and autoreduction to them when ready to see if it may be useful. First we need to sort out #15052. Shouldn't be too hard. Can be included in the specular GUI we have. Processing 2D detector data (this is one issue but there are many others).
-   \#10139? SNS. Owen looked into it but too complex would have to rework from scratch. Would like it looked into so we can pick nice features from it.  SNS gui QuickNXS (which is on github).
-   \# refl imple will be got rid of when happy with new features. gui working with most instruments except offspec (now works with offspec data to some extent). Finishing #15052 should resolve this?

### SANS github tickets<a id="sec-1-2-12" name="sec-1-2-12"></a>

-   AP: #12138 Remove this item. New reduction back end deals with this
-   HFIR: #12100 CS: from when collected twice from same sample and try to bring together. AJ: always a nightmare. scientists need to decide what wanted.
-   \#12097 SK: re: ways to interact with 2D image. Niche area at the moment; still relevant for future. AJ: something we'll need for ESS but at ILL they'll probablly keep using grasp(?)
-   \#12094 AJ takes blame for this ticket. SK: priority is probably 3-4.
-   \#12093 AJ: not sure what it's about. Will need to process giSANS data at ESS. SK: priority 2 fair. Relevant to all facilities, probably.
-   SK: raft of second level corrections that we're aware of but do nothing about at the moment.
-   Also now multiple scattering to add to this (SK: we may have a formula for how to do this soon).  AJ: this is for warning user about multiple scattering. SK: flag something up in the gui as a warning e.g. 90% chance affeted by multiple scattering. Then store. CS: sounds like it would be useful for SNS too. AJ: someone is working on algorithms for identifying multiple scattering issues. Would be nice to have. CS: good if could run as a side thing to check a sample (initially, then fold in?) AJ: not instrument dependent so could be generally applicable once added to mantid. At least as high priority as other corrections e.g. priority 2.
-   larger solid area of pixels at wider angles. Still relevant. CS: poss. relevant to SNS in future.
-   \#12088 AJ: can't actually measure it? SK: no one's sure how to do it? priority 4 still true. Needs more thought.
-   \#12078: SK: should just do this one. CS: we are doing it. AP: thinks we have dark current but SK says not using it. To check with Richard. AP showed this option on reduction settings tab in GUI and will demo to SK at some point. Not 100% sure work is what's needed. Will check with CS to compare with what SNS have done.
-   \#12130 AJ: can get rid of this.
-   Need to create a new ticket re multiple scattering
