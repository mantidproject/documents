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

**Advantages:** No
