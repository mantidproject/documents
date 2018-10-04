
## General

* #### Mantid freezing/crashing if serdon is not responding.

This was a problem with serdon file server that has been fixed by IT. 
It is not related to mantid, since the same was happening with a pure python script trying to open many files on serdon. 

* #### MantidPlot GUI is less stable, using mantid from python is very stable

Issues are continually being fixed with MantidPlot GUI. A project recovery service has been implemented, so that even in case of crash, one could recover the latest auto-saved checkpoint. Additionally, a crash reporting service is put in place, so that the crashes are reported to the developer team, so that they can reproduce and work on the fix. Also a large rewrite of the GUI, mantid workbench, will be released next year with higher stability and a different technology used for plotting.

* #### Continous development for techniques deployed

Resources to be allocated to provide continuous development and support.

* #### Post-reduction functionality missing or not easily accessible

Some post-reduction (pre-analysis) facilities exist in mantid for some techniques, but more work is required to adopt them and make them usable as plug and play right after the reduction. 

* #### Single page documentation for dummies for each technique and more training is needed

Hands-on tutorials will be organized in the upcoming months for each technique separately. Brief first-try documentations will be provided together with a template of user scripts for each technique. This will also contain the links to the detailed user documentation of each algorithm used within the workflow. 

* #### GUI issues on macOS

There are some known issues with the GUI windows on macOS. More resources need to be allocated to solve them. 

* #### Python 3 support

Python 3 builds are available for Ubuntu 16.04 only.

## Technique specific

### Backscattering – IN16B

* #### Absorption corrections not evident

There has been a large effor by ISIS to refactor the absorption corrections, which is now finished. While hiding the internals, this lead to only two algorithms to be exposed to the user: one for calculating the corrections (CalculateMonteCarloAbsorption) and one for applying those (ApplyPaalmanPingsCorrections). A template script will be provided with an example of how to use them in the worfklow.

* #### Functionality like superplot in LAMP is missing

There is an interface in Interfaces > General > Data Comparison, that allows for the same functionality.

* #### Scriptable plotting with standard style is missing

A successful example of this is implemented for TOF, will be implemented for other techniques in future.

* #### Maximum number of files not sufficient for fixed window scans

The default value, which is 1000 for ILL, will be increased to 10000. In any case, this setting is configurable by the user.

* #### Better visibility and browsing of the GUI dialogs in MantidPlot main window

The dialogs can be undocked from MantidPlot main window and managed as free floating windows.

### TOF – IN4, IN5, IN5

* #### S(Q,E) does not fulfill detailed balance

This is currently under investigation.

* #### Error bars in Q-scans incorrect for IN4

The magnitude of the errors is correct and comparable to the result of the other SofQW algorithms. The misleading smoothness is an artifact of the SofQWNormalisedPolygon algorithm. It takes the size of the detector pixels into account, hence the same detector contributes to many neighbouring Q bins increasing the bin-to-bin correlations and resulting to a smoothening effect. Current heuristics to define the Q bins results in too fine binning than what physical resolution allows for IN4 (not position sensitive detectors). Too fine bins cause very large bin-to-bin correlations, hence a smooth result. In the limit of point like detectors, the results become similar to the output of other (simpler) SofQW algorithms.

* #### Phonon density of states unusable

There are issues in the existing algorithm. New method should be implemented to use S(Theta, Omega) as input.

* #### No friendly GUI for TOF reduction

A new GUI is envisaged for data reductions at the ILL.

### Powder diffraction – D2B

* #### A problem in normalisation for 1D output

This has been fixed now, the fixed version is deployed.
