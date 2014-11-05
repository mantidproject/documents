**Design considerations for Horace type interface**

We would like to create algorithms that mimic the functionality and
syntax of Horace commands

*1. gen\_sqw function*

The Horace function signature is as follows:

***gen\_sqw (spe\_file, par\_file, sqw\_file, efix, emode, alatt,
angdeg, u, v, psi, omega, dpsi, gl, gs)***

- Our implementation would be based on ConvertToMD

- Obviously we will get rid of spe files and par files. Instead we
should use processed nexus files. This is very much suited to
autoreduced data at SNS

- For processed nexus files, there is no reason to include efix

- The workspaces must be in units of energy transfer

- alatt, angdeg, u, v are used to set the UB matrix. One can set the UB
matrix before. If not empty, it will override and set the UB again

- omega, dpsi, gl, gs are angles for goniometer settings. This should be
in principle set on the input workspaces beforehand. If omega is set, it
should override the individual goniometer settings for each individual
workspace. Dpsi, gl, and gs are additional goniometer rotations. <span
id="__DdeLink__0_426426089" class="anchor"></span>**TODO:** decide if we
want to use any of the angles. Also, if omega is not set, do we use
dpsi, gl, and gs?

- There are some optional parameters grid\_size\_in that maps into the
“SplitInto” parameter in ConvertToMD, and urange\_in, which maps into
“MinValues” and “MaxValues”

Proposed workflow (1 algorithm):

- load each individual file. I propose that we require to be in units of
energy transfer

- set the UB matrix, if desired

- Optionally set the goniometer

- calculate limits (if not given)

- ConvertToMD

- SaveMD

- at the end, use MergeMDFiles

Question:

-   do we want to enforce that all input workspaces have UB matrices/
    goniometers set?

-   

Our Mantid-Horace proposed signature is as follows:

***gen\_sqw (data\_source, sqw\_file, emode, alatt, angdeg, u, v, psi,
omega, dpsi, gl, gs, execution)***

- The function would return an MDEventWorkspace. Depending upon the
options chosen (such as execution). This returned MDEventWorkspace may
be file backed or not.

- data\_source argument can either be a file or a workspace, or a list
of either (possibly a mix of both).

- If the execution argument is anything other than inmemory, then the
sqw\_file argument is required in order to save the merged results.

- execution is an optional flag that can be used to specify how memory
is used in the processing. Options are inmemory, ondisk, and autodecide.
The default option is autodecide.

*2. cut\_sqw function*

The Horace function signature is as follows:

***cut = cut\_sqw (data\_source, proj, p1\_bin, p2\_bin, p3\_bin,
p4\_bin, '-nopix', filename)***

- data source must be an MDEvent workspaces

- this will be a wrapper around BinMD/SliceMD

- the proj object will be a slightly modified table workspace. The
python bindings will allow Horace syntax like proj.u= “1,1,1”

- we can generate a proj object from an algorithm, something like
proj=GenerateSQWProj(arguments). If no arguments given, we will use
sensible defaults

- I propose we add proj.w, the third projection axis, since we can do
non-orthogonal axes. If not given proj.w is calculated as the cross
product of proj.u and proj.v

**TODO:** decide if we want to have the -nopix option on by default
(will use BinMD), and use SliceMD for the “-withpix” option

Proposed workflow (2 algorithms):

- first algorithm to generate projection

- second algorithm to produce the cut

Our Mantid-Horace proposed function signature is as follows:

***cut = cut\_sqw (data\_source, proj, p1\_bin, p2\_bin, p3\_bin,
p4\_bin, '-nopix', filename)***

- cut is an MDEventWorkspace

- data\_source could be a file, or a MDEventWorkspace (filebacked or
otherwise)

- filename is optional. If provided then the results will be saved to
this location.

- p1\_bin etc., will be provided exactly the same as the existing Horace
syntax. These can either be a single value step, or an integration
range. The function will accept these either as a python tuple or list.

*3. plot*

*plot(cut)*

- to be done at a later date

- it will be dependent on the dimensionality of the MD workspace

- plotMD is not exposed to python (yet). It should be similar to
plotSpectrum. This would be the preferred way to plot 1D, since it
allows control in python

- for more than one dimension, the only option that allows python
control (for now) it's SliceViewer. Need to check if we can do plot2D
(nicer printed graphics)

- for 3D or more we need to enable python control for vates

*4. Other issues*

- need to implement symmetrizing

- need to implement fitting


