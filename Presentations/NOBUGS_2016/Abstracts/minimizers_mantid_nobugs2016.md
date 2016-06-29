# Comparing local minimizers for fitting neutron and muon data with the Mantid framework

Fitting is the process of trying to fit a mathematical model or
function to some data, where the data may originate from measurements
at beamlines or simulations. A simple example could be the problem of
fitting a polynomial background function plus a set of peak functions
to a spectrum. Fitting is commonly a core functionality in neutron,
muon and x-ray data reduction and analysis software packages. It is
required in tasks such as instrument calibration, refinement of
structures, and various data analysis tasks specific to different
scientific techniques.

The [Mantid software project](http://www.mantidproject.org) provides
an extensible framework that supports high-performance computing for
data manipulation, analysis and visualisation of scientific data. It
is primarily used for neutron and muon data at several facilities
worldwide. One of the core sub-systems of Mantid is the curve fitting
system. Mantid also includes generic and technique-specific fitting
graphical user interfaces.

The Mantid fitting system offers a great deal of flexibility in that
it is possible to add and combine different functions, minimizers,
types of constraints, and cost functions as plug-ins. Users can apply
different combinations of these elements through the same user
interface either via scripting (commands and algorithms) or graphical
user interfaces. In addition, some of these elements, such as
functions, are easy to add as plug-ins via scripting in Python.

Minimizers play a central role when fitting a function to experimental
or simulated data. The minimizer is the method that adjusts the
function parameters so that the model fits the data as closely as
possible, whereas the cost function defines the concept of how close a
fit is to the data. Local minimizers are widely used to fit neutron &
muon data. Several local minimizers are supported in Mantid (as in
other software packages used in the neutron, muon and x-rays
community). However there is a lack of openly available comparisons.

We have included in the latest release of Mantid (v3.7) [a
comparison](http://docs.mantidproject.org/nightly/concepts/FittingMinimizers.html)
of the performance of 8 different minimizers in terms of goodness of
fit (chi-squared or similar statistics) and run time. The comparison
has been done against the [NIST nonlinear regression
problems](http://itl.nist.gov/div898/strd/general/dataarchive.html).
This can inform users and developers as to:

- What performance can be expected from different minimizers in
  relative terms and what alternatives might be more appropriate for
  different applications.
- How modified minimizer methods or newly added ones perform as
  compared to already available alternatives.

For the next releases of Mantid we plan to extend the comparison with
test problems from neutron and muon data, considering different
scientific areas, and also further visualization of fitting results.
Furthermore, on the basis of our comparisons, we intend to incorporate
a new, flexible minimizer, RAL-NLLS, whose aim is to improve the
reliability and broaden the functionality of the Mantid fitting
system.
