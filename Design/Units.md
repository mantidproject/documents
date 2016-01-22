Motivation
----------

Reactors

Requirements
------------

1. Must still be able to convert to/from TOF for appropriate units
2. Comparison between reactor and tof neutron units should return true (e.g. `dspacing == dspacingTOF`)
3. For generic unit conversion, [boost::units](http://www.boost.org/doc/libs/1_40_0/doc/html/boost_units/Units.html) may work.
4. It would be helpful to be able to change between certain units in the presentation layer (`cm^-1` and `meV` and `micro-eV`)
45. It would be helpful to make the units user extensible

Design
------
