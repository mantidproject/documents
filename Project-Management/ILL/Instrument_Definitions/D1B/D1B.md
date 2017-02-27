# D1B Definition

This document describes the definition of D1B powder diffraction instrument at ILL.
The full instrument description can be found at 
[D1B paper](http://iopscience.iop.org/article/10.1088/1742-6596/549/1/012003/pdf "D1B") and [D1B summary](https://www.ill.eu/instruments-support/instruments-groups/instruments/d1b/description/instrument-layout/)

## Coordinate system

The global coordinate system used is the Mantid-default right-handed system: `z` axis is in the incoming beam direction while `y` axis points up. 

## Source

The monochromator, situated at `z = -2.986m`, is defined as the beam source. 

## Monitor

There is one monitor present, situated at `z = -0.476m`.

## Sample

Sample is located at the origin of the global coordinate system.

## Detector

The entire detector is composed of `1280` evenly spaced cells with height of `0.1m` placed at `1.5m` from the sample. Each cell covers *0.1&deg;* in scattering angle. The overall coverage of the detector is thus *128&deg;* spanning from *0.8 < 2&theta; < 128.8&deg;*.

## Instrument view

Below is the view of the instrument in Mantid. Blue is the z-axis in the direction of the incoming beam. Green is the y-axis point to top. Red is the x-axis of the right-handed coordinate system.

![D1B][image-id]
	
[image-id]: D1B.png "D1B in Mantid" 

