Image handling methods for Matrix Workspaces
============================================

Motivation
----------

Handling Imaging data with Workspace 2D structures is awkward, both for storing data and for plotting.

Current system for handling imange data
---------------------------------------

There are two approaches that have been attempted,
1. Storing data using X and Y as the axes, and single value intensity as the pixel data.  This works well with data loading and simple plotting, but fails with more advanced plotting such as the instrument view and most algorithms wil not run.
2. Storing a single intensity value against the Pixel and having a number of spectra that equal the number of pixels.  This work well with algorithms and the instrument display, but is not straight forward for creation from images or extracting the data.

Design
------

The first vew of the design was to create an image workspace that stored the intensity values as a vector of vectors of doubles.  This unfortunately fails when you consider supporting the `mantidvec& dataY(size_t index)` method.  As we return a reference we are somewhat stuck as to what storage type we support.  We could cache the value and update later for any changes, but when is later?, and this is getting too inefficient and slow.  So this approach has been discontinued.

The susequent option is to add some image based helper methods to Workspace2D (and porbably MatrixWorkspace and therefore EventWorkspace as well) to better support importing and exporting data as an image.

### In detail

1. Add the following methods to MatrixWorkspace


Feedback
--------

