# Loading Sample Environments
## Design Document

## Introduction
Absorption corrections rely on having a sample and environment, but currently we only allow simple shapes for both, or loading a sample shape from a .stl file. Complex shapes should also be allowed for the environment following a similar method of loading them from .stl files.  Using this method would allow users to take 3d scans of discrete pieces of the sample environment to create .stl files to then scan in to Mantid to allow for more accurate representations of the sample environment for absorption corrections.

The goal of this document is to outline a plan for `LoadSampleEnvironment` and to work out how to handle the various complications with implementing loading environments from .stl when compared with sample shapes.

## Complications

 ### Problems
There are several issues that make Loading a sample environment more complicated that loading a sample.
 * A sample has a single component, whereas an environment may have many`
 * A sample has a single material, whereas the environment may have components made up of several different materials.
 * A sample is centered, an environment will need to have each of its components translated and rotated into there proper position, this is increasingly problematic, as this cannot be defined within the .stl file.
  * The example environments given are far larger than samples have been in past, and exceed the capacity of MeshObject
 ### Possible Solutions
  * Allow loading an environment to either overwrite the current one acting as the can, or add it to the pre-existing environment.
  * Add a way to save commonly used environments so they can be loaded back in as a whole rather than having to individually load each component
  * Assign the material to the environment components individually.
  * Add a rotation and translation field to the algorithm, and create a script that puts the components into their proper places by loading each with specific values.
  * Make the algorithm read a file similar to the instrument definition file that contains the amount to rotate and shift each part of the environment, this method would require a way of generating definition files for a set environment, and would have to be easily adjustable (e.g. altering a field to adjust a components angle)
  * Increase the maximum size of MeshObject from uint16_t's max to uint32_t's, this may have an affect on the performance of other parts of Mantid that make use of meshObject
  
## Reuse of old code
A large proportion of LoadSampleEnvironment can be simply lifted from LoadSampleShape, all of the stl file reading can simply be called from LoadSTL much as LoadSampleShape currently does.

## Changes to code
The majority of the changes to the code will be in LoadStl and MeshObject, both of these files currently only support Loading files containing up to 65535, however some of the examples given by the scientists contain 6 times this number.  Other than the adjustments necessary for larger files, the rest of the new code/changes to code will likely be in LoadSampleEnvironment and be in place to implement whatever method is decided on to translate and rotate components into place.  Depending on how this is implemented this may not actually to different to the code used for instrument view, and so it may be possible to re-use code for this as well.
  
  
  
  
  
  
  
 ## Testing
  As well as unit tests to ensure the algorithm works properly, performance testing should be done, both with a large number of small components, and with very large components.
  
## Relevant Files for `LoadSampleEnvironment`
  [LoadSampleEnvironment.h]
  [LoadSampleEnvironment.cpp]
  [LoadSampleShape.h](https://github.com/mantidproject/mantid/blob/ef3ccb58e40735781011335e6b447a9ddd4d6e74/Framework/DataHandling/inc/MantidDataHandling/LoadSampleShape.h)
  [LoadSampleShape.cpp](https://github.com/mantidproject/mantid/blob/c17af71170b86e9ed4739364537d25e9e8ea49cb/Framework/DataHandling/src/LoadSampleShape.cpp)
  [MeshObject.h](https://github.com/mantidproject/mantid/blob/ef3ccb58e40735781011335e6b447a9ddd4d6e74/Framework/Geometry/inc/MantidGeometry/Objects/MeshObject.h)
  [MeshObject.cpp](https://github.com/mantidproject/mantid/blob/ef3ccb58e40735781011335e6b447a9ddd4d6e74/Framework/Geometry/src/Objects/MeshObject.cpp)
  [Container.h](https://github.com/mantidproject/mantid/blob/ef3ccb58e40735781011335e6b447a9ddd4d6e74/Framework/Geometry/inc/MantidGeometry/Instrument/Container.h)
  [Container.cpp](https://github.com/mantidproject/mantid/blob/ef3ccb58e40735781011335e6b447a9ddd4d6e74/Framework/Geometry/src/Instrument/Container.cpp)
  [LoadStl.h]
  [LoadBinaryStl.h]
  [LoadBinarySt;.cpp]
  [LoadAsciiStl.h]
  [LoadAsciiStl.cpp]
  