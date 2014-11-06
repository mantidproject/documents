
# Scope

The scope of this work has been summarised already [[1]]
> Keeping Horace interface would allow smooth transfer experience for all current Horace users and easy comparison of new and old well verified results, so it is suggested to keep Horace interface with only minor reasonable modifications. 

**This design document is to keep an incremental, running design on new phases of a mantid-horace syntax. It is NOT intended to detail (at time of writing) the complete set of mantid-horace, although that is the eventual aim.**

This document is intended to finally pull together contributions from several authors into a workable design document. Where possible the source of the syntax
will be referenced. The primary sources for this document have been:

* [Detailed Horace notes][1]
* [Horace][2]
* [Horace notes for Mantid implementation][3]
* [Horace style Plotting][4]

[2]: http://horace.isis.rl.ac.uk
[3]: https://github.com/mantidproject/documents/blob/master/Design/VATES/MantidHorace/horace-notes.md
[1]: https://github.com/mantidproject/documents/blob/master/Design/VATES/MantidHorace/horace-notes-horace-methods.docx
[4]: https://github.com/mantidproject/documents/blob/master/Design/VATES/MantidHorace/plot-commands.doc

# Contributors

Contributors in no particular order. These are people who have provided groundwork for the proposed syntax.

| Contributor        | Facility           |
| ------------- |:-------------:|
| Andrei Savici | SNS      |
| Stuart Campbell | SNS      |
| Alex Buts     | ISIS     |
| Owen Arnold     | ISIS |
| Toby Perring     | ISIS |
| Russell Ewings     | ISIS |
| Garret Granroth     | ISIS |

# Terminology

Mantid has it's own analogues to Horace objects. Mantid MDHistoWorkspaces are equivalent to Horace DND objects. Mantid MDEventWorkspaces are equivalent to Horace SQW objects. One major difference highlighted [[1]] is that and SQW object is a DND object, where as MDHistoWorkspaces and MDEventWorkspaces are fundamentally different types. The do share some properties, and where the type of the Mantid n-d workspace is of no importance, we refer to them in a generic way as MDWorkspaces.

# Syntax

The following commands will form part of the python CLI, and live in a python module **mantid.horace**

## cutMD

#### Brief

This is know as **cut_sqw** in Horace, but has been named cutMD since this fits better with Mantid, where *sqw* is not the genrally used term for n-dimensional datasets.

Where possible this function will attempt to handle a range of inputs provided including a range of file types (*.sqw, *.nexus) as well as the in-memory objects described as 
*data_source* in Horace's cut_sqw.

#### Detail

***cut = cutMD (data_source, proj, p1_bin, p2_bin, p3_bin,
p4_bin, '-nopix', filename)***

* data_source could be either an MDEventWorkspace, or iterable collection of workspaces, or, file, or iterative collection of files of type *.sqw, or *.nxs. Consideration could be given to allowing a mix of such input types in the same collection.
* This will be a wrapper around BinMD/SliceMD. The **-nopix** option would be used to specify the output type MDHistoWorkspace, or MDEventWorkspace [[1]], [[3]]
* The proj object will be a slightly modified Mantid TableWorkspace. The python bindings will allow Horace syntax like proj.u= “1,1,1” [[3]]
* We can generate a proj object from an algorithm, something like **proj=GenerateSQWProj(arguments)**. If no arguments given, we will use sensible defaults. [[1]], [[3]]
* I propose we add proj.w, the third projection axis, since we can do non-orthogonal axes. If not given proj.w is calculated as the cross product of proj.u and proj.v [[3]] 
* We suggest having the **-nopix** option on by default [[3]]
* filename is optional. If provided then the results will be saved to
this location. [[3]]
* p1\_bin etc., will be provided exactly the same as the existing Horace [[2]]
syntax. These can either be a single value step, or an integration
range. The function will accept these either as a python tuple or list.


##### Step 1. Generate the projections

We need a new algorithm to generate projections **GenerateSQWProj** [[1]], [[3]]

###### Detail

* Output should be a Mantid TableWorkspace
* Users should not need to know about this algorithm if running **cutMD** directly


##### Step 2. Performing the cut

**cutMD** could either be implemented as an algorithm or as a script. 

