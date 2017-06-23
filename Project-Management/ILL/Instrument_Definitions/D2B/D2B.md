# D2B Definition

This document describes the definition of D2B high resolution powder diffraction instrument at the ILL.
This definition is based on a Mantid instrument definition created a few years ago, so needs to be verified.

## Coordinate system

The global coordinate system used is the Mantid-default right-handed system: `z` axis is in the incoming beam direction while `y` axis points up. Spherical coordinates are used in the normal convention, x = r sin &theta; cos &phi;, y = r sin &theta; sin &phi;, z = r cos &theta;.

## Source

The monochromator, situated at `z = -2.997 m`, is defined as the beam source. 

## Monitor

There is one monitor present, situated at `z = -1.594 m`.

## Sample

Sample is located at the origin of the global coordinate system, that is at `r = 0`.

## Detector Tubes
 * Number of pixels: 128
 * Tube height: 300 mm
 * Tube span: -150 mm (bottom of bottom pixel) -> 150 mm (top of top pixel) in vertical axis
 * Distance between pixels/pixel height = 300 mm / 128 pixels = 2.34375 mm
 * Pixel radius of cylinder: 1.296 m * sin(0.05&deg;) / 2 = 0.56549 mm

**Note:** The real tube has a diameter of 25.4 mm, but the collimator reduces the effective angular range of one detector to 0.05&deg;. This is used in Mantid, but care should be used when using algorithms that rely on the instrument geometry, to ensure this is the correct thing to use.

## Detectors

 * Number of detector tubes: 128
 * Distance from sample: 1.296 m
 * Angle between detectors: 1.25&deg;
 * Default position in IDF: Tube 1 at 165&deg;, Tube 128 at 6.25&deg;
  * Actual position of Tube 1 read from NeXus/ASCII file, making the above arbitrary

## Instrument view

Below is the view of the instrument in Mantid. Blue is the z-axis in the direction of the incoming beam. Green is the y-axis point to top. Red is the x-axis of the right-handed coordinate system.

Note that this image suffers from some artefacts due to the detector width, it is easier to see the instrument in Mantid itself.

![D2B][image-id]
	
[image-id]: D2B.png "D2B in Mantid" 

