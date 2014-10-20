Image handling methods for Matrix Workspaces
============================================

Motivation
----------

Handling Imaging data with Workspace 2D structures is awkward, both for storing data and for plotting.

Current system for handling imange data
---------------------------------------

There are two approaches that have been attempted:

1. Storing data using X and Y as the axes, and single value intensity as the pixel data.  This works well with data loading and simple plotting, but fails with more advanced plotting such as the instrument view and most algorithms wil not run.
2. Storing a single intensity value against the Pixel and having a number of spectra that equal the number of pixels.  This work well with algorithms and the instrument display, but is not straight forward for creation from images or extracting the data.

Design
------

The first vew of the design was to create an image workspace that stored the intensity values as a vector of vectors of doubles.  This unfortunately fails when you consider supporting the `mantidvec& dataY(size_t index)` method.  As we return a reference we are somewhat stuck as to what storage type we support.  We could cache the value and update later for any changes, but when is later?, and this is getting too inefficient and slow.  So this approach has been discontinued.

The susequent option is to add some image based helper methods to Workspace2D (and porbably MatrixWorkspace and therefore EventWorkspace as well) to better support importing and exporting data as an image.

### In detail

1. Add the following methods to MatrixWorkspace
  * `MantidImage_sptr getImageX (size_t start =-1, size_t stop =-1, size_t width = -1,size_t IndexStart =-1, size_t IndexEnd = -1)`
  * `void setImageX (MantidImage_sptr)`
  * and similar Y and E methods
1. SetImage will simply set all of the values of that dimension to the intesity values in the image ass efficiently as possible
1. GetImage will extract all the dimension values and present them in a 2D representation as efficiently as possible.
1. MantidImage_sptr will be a shared pointer to a vector of vectors of doubles, and will be defined in a typedef.


Following on from this there are some sensible changes we could make to plotting workspaces when they have no "TOF" dimension. This will not affect ploting at all if the data has more than one bin.

1. If a colour map is requested and the data has one bin, then plot the output of GetImageY instead.
2. If a PlotSpectrum is requested and the data has only one bin, then plot the bin instead.

Feedback
--------
M. Gigg:

1. The methods should follow the standard camelCase naming style and be called `getImageY`, `setImageY` etc. 
1. Would it not be better when using this that the integrated X range, currently given as `IndexStart` & `IndexEnd`, be given by the actual values rather than their indices? I would assume that most of the time a user of the method would have the real `X` values and not their indices.
1. I can understand the methods for `Y` & `E` data but does having one for X make sense? Surely all of the values would be the same so it seems a little bit wasteful?
1. I am also not sure about the changes to plotting. Could it not be confusing if someone asked for plot of the spectrum and then got a bin plot? They could be fooled into thinking their data is not what they thought?


N. Draper:

1. Done
1. Happy to be swayed on this one, I was just keen to keep things fast, as long as we don't get into partial bins on this I'm happy.
1. This was just completeness on this for the C data, but I agree it will probably not be used.
1. This is an interesting point, that concenred me a bit as well, but a plot of a spectrum of one data point is not helpfull, and neither is a plot of a colour map with one x data point.  I do agree is is worth logging a message at Notice level that it is plotting something different instead.  The main reason I'm interested in this is to be able to plot something reasonble for image data when the user selects an colour map plot.
