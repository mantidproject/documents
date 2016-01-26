
# Some highlights from Ross Steward's slides about ISIS, and discussions

- Joe Kelleher: types that users can define/extend via plugins
- Muon: Mantid used by 50% (alternative: WiMDA). Origin used for graphs
- Powder, 3 alternatives: a) WISH, b) POLARIS, GEM, HRPD, c) OSIRIS
- **Common requirements: multiple scattering, absorption corrections**
- Waterfall plots (much interest from Powder diff.)
- Publication quality graphics!
- Overall perception of slow progress. Advances in visualization, powder,
indirect and adoption of engineering/imaging.
- Usability of visualization tools (MD): SANS, reflectometry
- Stability of GUIS (Muon gets broken too often)

Following the points in Nick's slides about current Mantid status and news

# 1D plotting

- Excel plots are easy but with Mantid I need to teach myself everytime (Joe Kelleher)
Counterarguments: do we want full blown plots in Mantid? Is this our mission?
- error bars: horizontal caps too big (Ron Smith and others).
- is it possible to drag curve from one plot to another plot? Wanted: more drag&drop and
intuitive visual feedback
- **Save project**, lots of demand. Takes long, it should not save files over and over.
- Graph management: yes, improvements would be nice, **but priorities are: multiple scattering,
etc. which should be the focus of Mantid**.
- With plots and graphs in general: nice to have simple "export to .txt" for loading in 3rd
party tools.
- Waterfall plots, with multiple axes, and surfaces (lots of parallel discussions hard to track).
- **Defaults for plots**. Put somewhere in the IDF. There are common algorithms that use similar
mechanisms. 
- Further on defaults for plots. There could be specific template or common plots that show up 
in right-click/context menu of workspaces when data comes from a particular instrument. Example:
ENGIN-X, both detectors on color plots side-by-side. Have a mechanism to define templates and 
use them based on the instrument (from the IDF). Otherwise, they'll do their scripts for these
plots but then the usability is poor.

# 2D Plots, color-fill plot

- **Change the quantity that is plotted: ToF to dSpacing, etc., ToF to Energy**
(keeping track of conversions when you go back and forth). Demand from both ISIS and SNS.

- ***General point about plots: link different plotting tools (3D view, SliveView, 2D plots)***.
Link the different views of the same data. This was one of the requirements from single crystal
(Christina Hoffmann). Much emphasis from Garreth, Pascal, Christina. Note: in discussions 
next day, a "synchronize" button was seen as a good option, as you don't always want continuous, 
real-time sync between plots.

- Side discussion about waterfall & other plots: they use autoreduction to write text files, but
then the plots just show spectra (not the headers).


# Slice Viewer + Instrument Viewer

- **Ross: cuts, they define them numerically, to batch-apply to different datasets, and they 
currently need to repeat tedious steps.**
- An option to have "Many cuts collection" - that's not good, not enough. It should be **like
MSlice** (very simple overplots): ability to find the cut quickly and overplot the cuts quickly.
- ***Non-orthogonal axes***, like ParaView does. Pascal & Ross.
- On the contrary, scripting is fine, but SliceViewer doesn't remember settings.
- Again: good defaults, capability to remember settings (including positions).
- SliceViewer 1D plotting: needs to be easier to use, "quicker feel". Ask the excitations group,
those who use it. They don't feel comfortable with it. The feeling of the tool is not good, not
quick as MSlice (they're happy with). With SliceViewer they are not happy, probably because MSlice
is more adapted to specific needs of particular instruments.
- From previous point: **adapted interfaces for ISIS-excitations**. Deviate from the approach of 
providing a generic tool? There's also demand from SNS: something like MSlice (so you don't need 
to fill in so many boxes), but better because Mantid has crystallography information.

# Documentation

- General: maths and formulas are lacking, for example when they use the GSL for a spline.
- **Search**: improve search (google, tags, meta-info). Keyworkds messed up (workspace group, 
group workspace).
- Change insane names of algorithms (make..., create..., generate...) maybe by deprecating?
[Side discussion from William (SNS SANS) they use Mantid for visualization but for algorithms
they use their own, as they've had bad experiences with modifications made by others].

- **Put more (automated) information in the algorithms documentation pages: info from validators.
For example if values need to be positive, if it only applies to some type of workspaces, etc.**
[FMP: Strong support and apparently consensus this is worth and doable]

- Do something to integrate instrument specific documentation (like for example the SANS technique
wiki pages.

# Fitting

Joe Kelleher with strong support from many:
- doesn't remember parameters
- doesn't remember limits
- which line is the peak? Make more obvious that the lines can be dragged.

- Expose statistics  [FMP: I think this is covered by the largely unknown alg. CalculateChiSquare]
- Other ways of outputting how the fitting worked: a python dict, export HDF, etc.

Sangamitra: 
- fitting doesn't work for some conditions

## Sequential fitting

You want to plot the output of the fits. Plot against run numbers, for example for muons (Steve Cottrell, Pascal)

# Scripting

All good

# Script Repository

All good

# Python plugins

Ross' comment: speak to Duc Le (implying it is a pain).

# IPython notebooks

All good.

# Pyplot

Nothing to say.

# Other topics:

- They like the idea of having meetings with instrument scientist groups
- About release presentations: if during cycles, avoid the mornings
 
