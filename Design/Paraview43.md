Motivation
==========

Paraview 3.98 is quite old, and we've paid Kitware to add features to paraview which
will only be in newer (v4.3+) releases. There is also an issue with (specifically)
linux machines where users have come to expect that they can run development and
release versions side by side.

Possible Solutions
==================

The options below are in pseudo-random order, but one must be selected.

Bundle Paraview
---------------
The baiscs are to make mantid
[a custom paraview app](http://www.paraview.org/Wiki/Writing_Custom_Applications).
The idea is that if we include the necessary paraview libraries, it won't matter what
is installed in the system and mantid won't have to search for the libraries at
runtime.

**Advantages:** Less external dependencies.
**Disadvantages:** Bigger installer. Going against packaging policies for most linuxes.

Software Collections
--------------------
[Software collections](https://fedorahosted.org/SoftwareCollections/) are how mantid
works with Paraview 3.98 on RHEL6. A software collection is a way to install a paraview
parallel to whatever is on the system. The change that we would need is to have a
second collection for paraview 4.3+ from 3.98.

**Advantages:** We have some knowledge on how to do this already.
**Disadvantages:** Only applies to rpm based systems where software collections are available.

Modules
-------
[Modules](http://modules.sourceforge.net/) are another technique for parallel installs of
software.

**Advantages:** Works on things other than rpm based systems.
**Disavantages** Must install the software by hand on every system using modules from source.
