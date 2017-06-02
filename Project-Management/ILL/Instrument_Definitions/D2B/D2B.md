# D2B Definition

This document describes the definition of D2B high resolution powder diffraction instrument at the ILL.
This definition is based on a Mantid instrument definition created a few years ago, so needs to be verified.

## Coordinate system

The global coordinate system used is the Mantid-default right-handed system: `z` axis is in the incoming beam direction while `y` axis points up. Spherical coordinates are used in the normal convnetion, x = r sin &theta; cos &phi;, y = r sin &theta; sin &phi;, z = r cos &theta;.

## Source

The monochromator, situated at `z = -2.997 m`, is defined as the beam source. 

## Monitor

There is one monitor present, situated at `z = -1.594 m`.

## Sample

Sample is located at the origin of the global coordinate system, that is at `r = 0`.

## Detector

Each detector tube is composed of 128 pixels. In terms of the pixel centres, the tubes start at -15 cm and go to 15 cm, so there is 30 cm between the top and bottom pixel centres. The pixels are evenly spaced with 2.362205 mm between pixel centres. Each pixel is treated as a cylinder, along the y-axis, with a radius of 1.27 mm and a height of 11.43 mm. The base of the cylidner is at -6.144 mm and the top of the cylidner at 5.290 mm. Hence between each pixel there is a large overlap (!).

There are 128 detector tubes are positioned at `r = 1.296 m` from the sample. The &theta; angle of the tubes in the default position goes from 165&deg; (tube 1) to 5&deg; (tube 128), but the position of the tube 1 is actually read from the NeXus or ASCII file. The angular spacing between tubes is 1.2598&deg;.

## Instrument view

Below is the view of the instrument in Mantid. Blue is the z-axis in the direction of the incoming beam. Green is the y-axis point to top. Red is the x-axis of the right-handed coordinate system.

![D2B][image-id]
	
[image-id]: D2B.png "D2B in Mantid" 

