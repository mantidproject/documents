Motivation
----------

Reactors

Requirements
------------

1. Must still be able to convert to/from TOF for appropriate units
2. Comparison between reactor and tof neutron units should return true (e.g. `dspacing == dspacingTOF`)
3. For generic unit conversion, [boost::units](http://www.boost.org/doc/libs/1_60_0/doc/html/boost_units/Units.html) or [uduints](http://www.unidata.ucar.edu/software/udunits/) may work.
4. It would be helpful to be able to change between certain units in the presentation layer (`cm^-1` and `meV` and `micro-eV`)
45. It would be helpful to make the units user extensible
2. Logs should have proper units

This work will require a new version of `ConvertUnits` that uses the new quantities.

Design
------

