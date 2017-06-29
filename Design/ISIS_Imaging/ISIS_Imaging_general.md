<!-- TOC -->

- [Motivation](#motivation)
- [User Requirements](#user-requirements)
- [Development Requirements](#development-requirements)
- [Terminology](#terminology)
- [Finalising name choice](#finalising-name-choice)
- [Project setup](#project-setup)
    - [Continous Integration with Coverage](#continous-integration-with-coverage)
    - [Installation](#installation)
    - [Testing](#testing)
        - [Core](#core)
        - [GUI](#gui)
- [Guidelines for ISIS Imaging CORE](#guidelines-for-isis-imaging-core)
    - [CUDA filter expansion](#cuda-filter-expansion)
        - [CuPy](#cupy)
        - [OpenCV](#opencv)
    - [Reconstruction tools expansion](#reconstruction-tools-expansion)
    - [File Structure](#file-structure)
    - [Filters - General implementation structure](#filters---general-implementation-structure)
- [Implementation for ISIS_Imaging GUI](#implementation-for-isis_imaging-gui)
    - [General Structure](#general-structure)
    - [.ui Compiling](#ui-compiling)
    - [Using iPython](#using-ipython)
    - [Loading](#loading)
    - [Handling multiple stacks in dialogues](#handling-multiple-stacks-in-dialogues)
    - [Saving](#saving)
    - [Visualisation](#visualisation)
    - [Histograms](#histograms)
    - [Contrast normalisation](#contrast-normalisation)
    - [Applying a filter](#applying-a-filter)
        - [Dynamic dialogue building](#dynamic-dialogue-building)
        - [Transferring information from the dialogue (the parameters) to the execution](#transferring-information-from-the-dialogue-the-parameters-to-the-execution)
    - [Preview a result](#preview-a-result)
    - [Undoing an operation](#undoing-an-operation)
    - [Process List](#process-list)
        - [Store image state as part of the History in the process list](#store-image-state-as-part-of-the-history-in-the-process-list)
        - [Exporting of Process List](#exporting-of-process-list)
    - [Processing a full volume](#processing-a-full-volume)
    - [Issues with Finding Center of Rotation and Reconstruction](#issues-with-finding-center-of-rotation-and-reconstruction)
        - [Automatic Center of Rotation (COR) with imopr cor](#automatic-center-of-rotation-cor-with-imopr-cor)
        - [Center of Rotation (COR) with imopr corwrite](#center-of-rotation-cor-with-imopr-corwrite)
        - [Tilt correction](#tilt-correction)
        - [Calculating the real tilt angle](#calculating-the-real-tilt-angle)
    - [Reconstruction](#reconstruction)
    - [Remote submission and MPI-like behaviour](#remote-submission-and-mpi-like-behaviour)
        - [Remote compute resource used at ISIS: SCARF](#remote-compute-resource-used-at-isis-scarf)
        - [MPI-like behaviour](#mpi-like-behaviour)

<!-- /TOC -->

The user requirements for the interface have been listed [here](https://github.com/mantidproject/isis_imaging/wiki/High-Level-User-Requirements-and-Use-Cases) and have been reviewed and confirmed by the imaging scientists.

The development requirements, following from the user requirements, are listed [here](https://github.com/mantidproject/isis_imaging/wiki/High-Level-Development-Requirements-and-Guidelines)

# Motivation

The current [Tomography Reconstruction](https://github.com/mantidproject/mantid/tree/043095a619bc8851942a31253a1a8f8b820ab30f/MantidQt/CustomInterfaces/inc/MantidQtCustomInterfaces/Tomography) interface was found to not satisfy the current imaging requirements. An easy solution to the problems was not found. With the agreement of the IMAT imaging scientists and senior members of the Mantid team, work is to be started on this design for a rewrite of the interface. Python is the preferred language here, in order to be able to make use of visualising libraries like Matplotlib and interactions with Python based reconstruction packages like Tomopy.

# User Requirements

1. Visualisation of single or volume of images
    - Contrast adjustment on the visualised image
    - Good performance with 2048x2048 and 4096x4096 images
    - Selection of region of interest(ROI) on the visualisation
1. Applying an operation to the visualised image
    - This could be a filter or a single slice reconstruction
    - Images can be rectangular or squares
1. Storing history of applied filters in a Process List
    - Can be used to process a different volume independently (on a remote cluster or locally)
1. Histogram computation for the ROI on the visualised image
1. Processing a full volume locally or on a remote computer via job submission
1. Finding the Center of Rotation and ability to manually reconstruct single slices with different CORs
1. Reconstruction using different algorithms, provided by external tools
1. Remote submission and MPI-like behaviour
1. User facing documentation
    - API documentation
    - Usage documentation/tutorial

# Development Requirements

1. Unit testing for CORE
1. GUIs use MVP pattern with mocking and unit testing for GUIs
1. System tests to ensure larger module functionality
1. Maintain Documentation
1. Continous Integration on Github
1. Installation

# Terminology

Projection - Look towards the object from the side, image with the histogram:
![Projection image](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/projection.png)

How a projection looks after pre-processing, image with the histogram:
![Pre-processed](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/pre_processed.png)

Radiograms - Multiple projections for a _single_ angle

Tomography - Multiple projections for more than one angle. Usually 360 degrees around the object.

Processing a Tomography as volume of Projections - This is the data is loaded initially, it forms a 3D volume. `array[Z, X, Y]`.

- Each index corresponds to a different projection angle.
- Each image's dimensions are described with X and Y.
- The Z axis is used to traverse the images. Note: some packages may use the format `array[X, Y, Z]` for traversal

Sinograms - same as volume of Projections, however the traversal is done on the X axis in `array[Z, X, Y]`, giving the horizontal movement of the object throughout the tomography for each row. An image of the sinogram with it's histogram:
![Sinogram](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/sinogram%2Bhistogram.png)

Slices - referrs to a reconstructed sinogram. ![Reconstructed slice](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/reconstruction.png)

Attenuation - the result from performing a `-ln(image)`, which can be written as `numpy.negative(numpy.log(image))`. Depending on the dataset adding the `-log` to pre-processing can _significantly_ improve the reconstruction results and help remove noise!

# Finalising name choice

- MantidImaging
- ISIS_Imaging
- Other suggestions?

# Project setup

## Continous Integration with Coverage

The package should have a continous integration flow on Pull Requests, which runs all of the CORE and GUI tests. This should also include coverage.

After sphinx documentation is added, the contiguous integration could also check if it builds successfully.

## Installation

We can either work towards the package being installable using `python setup.py install`, making it available system wide. The alternative solution is to use it from the folder and provide global access like [the example here](https://mantidproject.github.io/isis_imaging/user_guide/setting_up.html#global-access-to-the-package)

## Testing

Testing will use `nose` to run the tests and `coverage` to compute the tests' coverage. The actual unit tests should use the built-in `unittest`, and some might have to use `numpy.testing` for asserting equality for `numpy.ndarrays`.

A module to run the tests has been provided and is called `run_tests.py`, in the root of the repository. It takes as an argument the names of different packages, and then runs the tests specifically for them. The possible arguments are listed via `-h` flag, or at the top of the file in the source.

There is currently no integration with Mantid's testing.

### Core

Every module should have associated unit tests, unless there is good reason not to have one. 

There should also be a collection of system tests to make sure that the functionality works on a higher level than unit tests.

### GUI

The GUI should use the MVP pattern, making it easier to mock and unit test. Mocking should be done with the python built-in `mock`. There should be an associated mock and presenter unit testing for every MVP used. 

Simpler cases like the `load`/`save` dialogues do not need to use MVP, because they have very little, if any, logic.

# Guidelines for ISIS Imaging CORE

## CUDA filter expansion

Integrating a package that supports CUDA has potential for improvement and expansion of the imaging filters.

A potential problem for CUDA is for machines with low VRAM, transferring the data multiple times might be slower that just doing it in a bulk in the CPU, if it has a lot of RAM.

### CuPy

This package supports CUDA and nicely implements most of the `numpy` API, meaning it can make transition over to GPU processing easy, for filters that only use `numpy` functions (background correction, contrast normalisation, etc).

For filters requiring custom code, kernels for other filters like Median, Gaussian, etc, can be written additionaly. [Related issue on repository.](https://github.com/mantidproject/isis_imaging/issues/50) This issue links to a response in the CuPy repository about how to write CUDA kernels in external files and then compile them inside during Python execution.

I would recommend asking on the [CuPy repository](https://github.com/cupy/cupy) for implementation (and performance wise) advice before finalising the implementation of any filter.

### OpenCV

This is a library for image processing and computer vision, it has a lot of features, but is also quite large. I have added it here as it should be considered if there is anything available that is needed. It is available on the SCARF/Emerald cluster, making it potentially usable. 

Something that might cause issues - I am not sure how well it integrates with `numpy` arrays, for C++ they use their own internal type `cv::Mat` and I have not used the Python bindings.

## Reconstruction tools expansion

- [Astra Toolbox](http://www.astra-toolbox.com/)
- [MuhRec](http://www.imagingscience.ch/downloadsection/)

## File Structure

The aim is to make use of Pyhton's modular structure as much as possible. There is very little actual Object Oriented Programming used within the files, and I would discourage its use, unless it makes sense, for example the `core.imgdata.saver.Saver` is a class that can store all necessary information about the saving, so that when used in `core.configurations.default_flow_handler` we don't have to repeatedly pass in arguments, however the `save` function is globally available without needing to create instance of the class, making it very convenient to use through command line.

Another example is in the `core.tools` module, we want the tools to implement a common API, so that if we want to change the tool we can just import another one, and it _should_ work. This is done via having an `AbtractTool` that the other tools should inherit from, and should implement its interface.

---

Currently the scripts expect the folder structure to be:

``` text
<repository_folder>/
└── isis_imaging
    ├── core
    │   ├── aggregate
    │   ├── algorithms
    │   ├── configs
    │   ├── configurations
    │   ├── convert
    │   ├── filters
    │   ├── imgdata
    │   ├── imopr
    │   ├── parallel
    │   └── tools
    ├── gui
    ├── systemtests
    └── tests
```

It is not expected to have many changes of this top level structure. If any structural changes are made, they will break `registrator` and `finder` from `core.algorithms`. They expect to have this structure in order to dynamically register the files inside `filters` and `algorithms`. However the changes that will need to be done to reflect such a change are contained within the `finder` and `registrator` modules. This has been tested by:

- Renaming `core` to something else, e.g. `thecore`. A find and replace of `core` to `thecore` made the package usable again.
- Adding another level before the `core` package, so the structure would be:

``` text
└── isis_imaging
    └── another_level_package
        └── core
```

- A find and replace of `core` to `another_level_package.core` made the package usable again.

Having this structure also allows to expose a consistent Public API through the `__init__` files, making the suggestions in iPython only show what we have exposed to the Public API.

## Filters - General implementation structure

- Filters should be inside a package that only exposes `execute`, `gui_register`, `cli_register`, and any other functions desired to be part of the public API. This will be enforced in the package's `__init__.py`
  - This allows to have a strict API regardless of the internal implementation inside the package, so that is left is up to the developer. They could be in a single `.py` module, or in a separate module for each large function -> `execute.py`, `gui.py`, `cli.py`, etc.
- All of the filters must implement an `execute` function that takes the image volume as its first parameter. The following parameters should be the ones necessary for execution, and the last two should be `cores` and `chunksize`. The reason for having `cores` and `chunksize` in every filter's API is to make them usable standalone through iPython, or external scripts without having to construct a configuration object.
- All filters must implement a parallel and sequential execution. How that is done is up to the developer.
- Future extensions could be adding CUDA execution to some/all fitlers. This would ideally be handled as part of the checks for parallel inside the `execute` function, but if that is not possible or desirable, a new function might be added to the API specifically for CUDA execution.

# Implementation for ISIS_Imaging GUI

## General Structure

Main Window (top level)

- QMenu with options: File (load, save, quit), Filters (dynamically registered filters should appear here)
- QDockWidget that will hold all of the image volume windows
- Knows what stacks are alive and their unique IDs and references with which they can be accessed
- Forwards any requests from filters' dialogues onwards to the target stack

Stack Visualiser (Image Volume)

- It is a child of the Main Window' QDockWidget
- It contains reference to the data, and the ability to execute operations on it
- It contains functions providing capability to filters to 'request' certain parameters, that would not be obtainable otherwise, like what region of interest is currently selected by the user, flat and dark images to be loaded and forwarded as arguments.
- It stores and shows the Process List for the image volume that it is handling
- It allows the user to initiate computation of histogram
- It allows the user to initiate contrast adjustment
- It visualises the images
- On destruction removes itself from the parent, and the list of unique IDs. It also removes any references to the data so it can be GC by Python

![Main Window with all possible stack window positions](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/all_views.png)

The Main Window allows us to place the stack in multiple different places:

- As tabs (seen bottom left)
- On the right of the tabs, inside the main window
- Floating around

## .ui Compiling

Currently the `.ui` is compiled dynamically while running. It might be better if this is changed to the mslice approach where all of the `.ui` files are compiled during 'build' and `.uic` files are created.

## Using iPython

The benefit of .ui compiling at runtime is that we can quickly run the `MainWindow` inside an `iPython` instance. A simple example of that:

``` py
In [1]: %load_ext autoreload
In [2]: %autoreload 2

In [3]: mw = isis_imaging.main_window.MainWindowView(None)

In [4]: mw.show()

# close the window manually, we get error if we try to show
In [7]: mw.show()
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-7-1b92a2253c98> in <module>()
----> 1 mw.show()

RuntimeError: wrapped C/C++ object of type MainWindowView has been deleted

In [8]: mw = isis_imaging.main_window.MainWindowView(None)

In [9]: mw.show() # works again
```

## Loading

Loading of the images must be done via the `core.imgdata` module, which already handles loading of any supported image types.

The Loading will be done via a dialogue:

- It will ask for the paths for the images.
- The selection will require the user to select a file, NOT a directory.
- The image format will be determined from the selected file.
- The absolute path to the directory will be determined from the selected file.
- An option for ImageJ-like virtual stack should be available.
- The user can specify indices in 3 spinboxes for [Start, Stop, Step]. Boundaries are: 
    - The spinboxes cannot be negative.
    - Max value of Start is Stop - 1.
    - Min value of Step is 1, and max value of Step is the value of Stop.
    - Max value of Stop is the number of files with the extension (detected dynamically after selection of the file). 
        - Stop does not have a lower bound, meaning the user can select a Stop value lower than the Start value. Doing so will result in a ValueError.
        - This can be avoided with a signal triggered by changing the Start spinbox, that changes the setMinimum of the Stop spinbox. (low priority)

Initially, while browsing for a folder, the files will not be filtered out by file extension. This could be a potential improvement if it proves to be necessary or requested by users.

After loading the paths should be cached inside the created image volume window, so that they can be accessed by the Process List or any filters that require the loading of flat/dakr images.

## Handling multiple stacks in dialogues

It will be possible to have more than one stack loaded at a time. A unique ID will be generated for each new stack that is loaded. The ID is then stored with the folder name as a 'user friendly name', and a reference to the QObject containing the stack. The unique ID will be generated using python's `uuid` package.

On closing the image volume window we need to remove any references to the stack. Qt provides `closeEvent` which is triggered when the user clicks the `X` button. Each stack window will know it's own unique ID, it should delete it from the dictionary, and also remove the reference to any data it might be holding.

Building the selection for the user will be an iteration of the dict, sorted by key and displaying the user friendly name, but also store the uuid to be able to reference the data afterwards.

## Saving

The saving dialogue will have a drop down menu, kept up to date with what active stacks there are in the main window. The user can then select a stack, select the format (by default `.tiff`) and save it out to the path they point to. The supported formats dropdown menu will be populated at runtime by using the loader's available extensions function, which is already used when building the command line interface help (-h).

## Visualisation

The MainWindow will have a `QDockWidget`. Each image volume will be a child `QWidget` inside the main `QDockWidget`. This allows usage of the flexibility of `QDockWidget`, making it possible to have docked windows, docked tabs, floating windows, or any combination of those. The users will be able to arrange the visualised stacks in any way they want. The first stack visualised should be docked inside the MainWindow, be centered and take up all of the space. Any consecutive stacks that are loaded will be placed inside the MainWindow automatically by Qt.

For the actual visualisation `FigureCanvasQtAgg` will be used with the default drawing algorithms. If this proves to be too slow, the drawing function may need to be changed or adapted.

The visualisation must have a rectangle ROI selection, that is persistent if the image underneath is changed. Matplotlib provides a `RectangleSelector` class which will be used to do the ROI selection. It changed dynamically with size and correctly translated the coordinates regardless of image scale, zoom or position.

The user must be able to go to any index from the volume. This will be done via a slider. The implementation of the slider should be generic, and allow to have a few different sliders with different look and feel.

The visualisation should also have the toolbar that appears on plots in Matplotlib, the functionality that comes with the default toolbar works with the images.

## Histograms

Computation of the histograms should be done only on the ROI, if no ROI is selected the whole image will be used. The computation itself should be implemented in the `core.algorithms` package. It might be necessary to do so asynchronously. The `matplotlib` histogram feature was found to be quite slow. An alternative could be `np.histogram`, but that has not been benchmarked.

Visualisation should be a small independent widget detached from the stack. This histogram needs to provide a way for the user to select a range of values that are to be used for contrast normalisation. 

Maybe the default `matplotlib.pyplot` can be used, if there is a way to keep track of the range of values that the user has selected and feedback to the contrast normalisation.


For the histogram window an `mslice` approach could be taken where the user can choose to:

- `Keep` the histogram, meaning new histograms will take place in a new window
- `Current selection` on the histogram, meaning new histogram will replace the one in the window

Keeping multiple histograms around shouldn't be a memory issue, and they be binned, reducing the memory usage further.

## Contrast normalisation

Matplotlib provides a method to specify contrast range via `set_clim` method on the image. The values will be read from the histogram and the image will be changed when the user changes the selected range of values in the histogram.

## Applying a filter

Applying a filter will bring up a dialogue in which the user has to select on which stack to apply the filter via a dropdown menu, and fill in the required parameters the filter has.

Any filters should be dynamically registered using the [registrator](https://github.com/mantidproject/isis_imaging/blob/master/isis_imaging/core/algorithms/registrator.py) style approach. Filters will have to implement `cli_register` and `gui_register` functions that register them with the command line and graphical interface, respectively, in order to be visible on each of the interfaces.

Current issues for this section:

### Dynamic dialogue building

- Solution is to use an approach like the `cli_registrator`, but pass in the QObject in which the filters will register themselves in
- Dialogue registration is a bit more complicated, because we have to connect the dropdown menu to the dialogue's `.show()` method.

### Transferring information from the dialogue (the parameters) to the execution

- The filter should be executed from inside the image visualiser. The main window does not have reference to any data, only the QWidgets that contain the visualisation.
- Using a partial function, we can decorate with all of the parameters. No other function down the chain of execution will have to worry about the parameters that way.
    - Alternative is to store the state as a global object inside each filter's module. On `execute` if no parameters are provided, then they are read, by default, from the global object.
- Requesting a parameter from the visualiser
    - There are some filters that operate on a region of interest of the image volume.  Because the dialogue and the image stacks have no way to communicate, there is no way to read in what region has been selected by the user.
    - A possible solution is to allow the dialogues to 'request' for a parameter from the image visualiser. The parameters that would be available initially are Region of Interest, flat/dark images.
- Handling filters with multiple steps
    - Background correction and contrast normalisation need to calculate values for scaling, do the filter execution, and then apply the scaling to the images.
    - Currently the solution is to apply a monad style approach.

## Preview a result

This can be an option in the filter dialogue. It will be passed as a parameter to the image visualiser. If preview is selected the data will be deepcopied and processed, resulting in a new stack with the processed data.

## Undoing an operation

Building the Undo operation may be complicated and turn out to consume too much memory, but provides better functionality. Initially should not be part of the implementation.

Some issues:

- Storing the original state as a deepcopy, and then applying the filter inplace on the volume of images, works best with single image.
- Serious memory implications for large volumes.
- Can easily store a single undo (like imagej, only for single images), multiple undos can be hard to implement efficiently because of all the memory being copied

## Process List

Every operation on the image volume should be saved in a `ProcessList`, which can then be exported and re-used on another image volume. The process list acts like a `queue`, first-in first-out.

A problem that appears with that approach is that some images need more than one stack for an operation, e.g. background correction needs flat and dark images as well. Running a process list on a different stack will not know from where to read in the flat and dark images, they would need to be specified by the user. Possible solutions:

- Ask for flat and dark paths in image loading dialogue and cache them for the loaded stack, then the process list can reuse them
- Ask for flat and dark paths when the filter is popped from the Process List queue

### Store image state as part of the History in the process list

This is not done in the current implementation of the `ProcessList`. This could be added as a replacement for [Undoing an operation](#undoing-an-operation), but it suffers from the same issues as undoing.

### Exporting of Process List

This is something considered as part of the [remote submission](#remote-submission-and-mpi-like-behaviour) implementation. It will require implementing functions to export an exsiting process list to a format that later can be read back and construct a new Process List.

## Processing a full volume

A process list should provide the option to be applied to the whole stack locally. Details for the implementation need to be considerend alondside the [Undoing an operation](#undoing-an-operation) implementation.

The process list will store the operation(+params) that needs to be applied. Doing this for the whole stack would simply require walking through the process list. There is _nothing_ currently implemented in the `core` module that allows for that.

A new configuration might have to be added in `core.configurations` to handle this type of ordered filter application. A class that takes the name and dynamically imports/applies the operation might also be required.

## Issues with Finding Center of Rotation and Reconstruction

Normally the data volume will be loaded in as radiograms: 
![Pre-processed](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/pre_processed.png)

During the pre-processing stage we can process only a few images to see the results from the applied filter, the full stack _does not need_ to be processed, until we are happy with the effects.

Doing operations like finding the Center of Rotation requires the image to be Sinograms:
![Sinogram](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/sinogram%2Bhistogram.png)

An example of how to do that with the package is `isis_imaging -i /your/data --convert --swap-axes -o /output/path`. In the end it boils down to a simple `np.swapaxes(data, 0, 1)`. 

If `np.swapaxes` is done during processing, it breaks the contiguous order of the data. Attempting a reconstruction while the data is not in contiguous order will cause `tomopy` to manually copy the data inside the `tomopy.recon` function.

We can manually make the array contiguous with `np.ascontiguousarray`, but it increases the memory usage by about 30-50%. 

Currently we avoid loading the whole stack during the pre-processing, or until we want to work on the sinograms. This means we apply the pre-processing on the radiograms, and then when happy, convert to sinograms, and continue pre-processing or start looking for the center of rotation.

A feature that might help is a Region of Interest (ROI) load, which would load the image, and save just the ROI we want. For example this will help us load only the first row from every projection, constructing the first sinogram. I am not aware of any package that lets you control what region to load, they usually load the whole image, thus it may be possible to:

- Load the full image
- Use it to construct the first row of _every_ sinogram of the stack
- Repeat and keep adding a row from each image

### Automatic Center of Rotation (COR) with imopr cor

Once we have the histograms into memory with contiguous order, we can proceed to find the Center of Rotation for each sinogram.

Currently the automatic COR calculation is done on the sinograms and uses `core.imopr.cor`. Ideally we want to keep that behaviour. Slight change might be necessary to the `core.imopr.cor` module, as currently it does not return the CORs, but only prints them in the console.

That usage can be accessed via `isis_imaging -i /some/sinograms/ --imopr cor --indices 0 1800 100`, this will automatically calculate the COR for every 100th image of all the 1800 images we have. The output looks like this:

``` text
➜  ~/temp/chadwick isis_imaging -i sinograms --imopr cor --indices 0 1800 100
 >> WARNING: No output path specified, no output will be produced!
Sample: [========================================]20 / 20
Data shape (20, 1570, 1070)
*********************************************
*
*     Running IMOPR with action COR. This works ONLY with sinograms
*
*********************************************
 ---Importing tool tomopy
 ---Tool loaded. Elapsed time: 9.70363616943e-05 sec.
Calculating projection angles..
Running COR for index 0 [ 1510.95703125]
Running COR for index 100 [ 751.5078125]
Running COR for index 200 [ 1157.7734375]
Running COR for index 300 [ 753.1796875]
Running COR for index 400 [ 723.50390625]
Running COR for index 500 [ 677.9453125]
Running COR for index 600 [ 676.2734375]
Running COR for index 700 [ 674.18359375]
Running COR for index 800 [ 673.765625]
Running COR for index 900 [ 673.34765625]
Running COR for index 1000 [ 673.765625]
Running COR for index 1100 [ 681.2890625]
Running COR for index 1200 [ 677.109375]
Running COR for index 1300 [ 677.109375]
Running COR for index 1400 [ 677.109375]
Running COR for index 1500 [ 677.109375]
Running COR for index 1600 [ 677.9453125]
Running COR for index 1700 [ 676.2734375]
Total execution time was 164.612098932 sec
```

As you can see the COR can get confused for some slices, for example slice 0, which is basically empty:
![Sinogram 0](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/sino0.png)

But for the sinogram on position 200, it look okay, just the algorithm was wrong:
![Sinogram 200](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/sino200.png)

### Center of Rotation (COR) with imopr corwrite

This is the manual way to determine the COR. It can be accessed with:

`isis_imaging -i /some/sinograms/ --imopr 660 680 1 corwrite --indices 0 1800 100 -o /output/path/required` 

This has output path required, and will not execute if not provided one. It saves out reconstructed slices with a range of CORs. The range is specified in `--imopr 660 680 1`, the format is `--imopr start_cor end_cor step`. An output from that command could be:

```text
➜  ~/temp/chadwick isis_imaging -i sinograms --imopr 660 680 1 corwrite --indices 0 1964 100 -o ./cors
Sample: [========================================]20 / 20
Data shape (20, 1570, 1070)
*********************************************
*
*     Running IMOPR with action COR using tomopy write_center. This works ONLY with sinograms!
*
*********************************************
 ---Importing tool tomopy
 ---Tool loaded. Elapsed time: 4.50611114502e-05 sec.
Calculating projection angles..
[660, 680, 1]
Starting writing CORs for slice 0 in ./cors/0
Starting writing CORs for slice 100 in ./cors/100
Starting writing CORs for slice 200 in ./cors/200
Starting writing CORs for slice 300 in ./cors/300
Starting writing CORs for slice 400 in ./cors/400
Starting writing CORs for slice 500 in ./cors/500
Starting writing CORs for slice 600 in ./cors/600
Starting writing CORs for slice 700 in ./cors/700
Starting writing CORs for slice 800 in ./cors/800
Starting writing CORs for slice 900 in ./cors/900
Starting writing CORs for slice 1000 in ./cors/1000
Starting writing CORs for slice 1100 in ./cors/1100
Starting writing CORs for slice 1200 in ./cors/1200
Starting writing CORs for slice 1300 in ./cors/1300
Starting writing CORs for slice 1400 in ./cors/1400
Starting writing CORs for slice 1500 in ./cors/1500
Starting writing CORs for slice 1600 in ./cors/1600
Starting writing CORs for slice 1700 in ./cors/1700
Finished writing CORs in ./cors
Total execution time was 103.075942993 sec
```

In the output folder `./cors` we can see a structure like this:
![CORs Folder](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/corsstruct.png). If we have a look at the COR slices that have been produced, slice 500 with COR 667:

![Slice 667, bad recon slice](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/badreconslice.png). This was reconstructed with a COR of 667. Initially it is not quite clear if it's a good slice or not, but looking at this:

![Slice 667, bad recon slice with text](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/badreconslicecircle.png)

We can see the out 'shadow' is because we've missed the COR by quite a bit. Here is slice 500 with COR 530, which is closer to the correct COR:
![Slice 667, bad recon slice, closer COR](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/badreconslice2.png)

It still has that 'shadow' circle around the object, because we're not quite there yet, but close.

The slice with the correct COR looks like this:

![Slice 667, bad recon slice, closer COR](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/goodreconslice.png)

The 'shadow' has now merged into the object in the middle. This is now correct.

We want to keep that behaviour as is, with the addition that after the process of saving out is finished, we visualise them back from the user, so they can select the best COR by seeing which is the best reconstructed slice.

### Tilt correction

Sometimes the samples are tilted slightly. On the one above the difference in COR between the top and the bottom looks like this:

| Slice |  COR  |
| ----- | ----- |
|  422  |  542  |
|  822  |  540  |
| 1222  |  540  |
| 1622  |  537  |
| 1822  |  536  |

As you can see there is a bit of a difference near the top (slice 422) and the bottom (slice 1822). In this case it's not a lot, only 6 pixels.

However it needs to be accounted for during the reconstruciton. This is currently done in `core.algorithms.cor_interpolate`, which requires the information above (slice and associated COR) and interpolates the rest of the CORs for the slices in between. This method has worked quite well so far, because Tomopy lets us specify a COR for each slice, by providing a list that is of the same length as the number of sinograms.

### Calculating the real tilt angle

TODO draw the triangle on the image

## Reconstruction

Once the sinogram issue has been resolved, we will have the sinograms in contiguous memory. This section will assume we already have solved that.

The reconstruction works on sinograms and will be done via third party tools Tomopy, Astra Toolbox, MuhRec, etc.

Specific dialogues might have to be created for each tool, to handle the different parameters each one has.

## Remote submission and MPI-like behaviour

Remote submission needs to be supported, that means we need to be able to submit the reconstruction/processing parameters through the REST API they provide. Information about the reconstruction should be stored in a `ProcessList`, which can be serialised and then recreated anywhere with the `--process-list` flag.

### Remote compute resource used at ISIS: SCARF

General information on the SCARF cluster, which uses the Platform LSF
scheduler, can be found at http://www.scarf.rl.ac.uk. It can be used
via:

- remote login
- a web portal: https://portal.scarf.rl.ac.uk
- a web service

The IMAT GUI utilizes a RESTFul web service provided by Platforms
LSF's Platform Application Center, as described here:
https://github.com/mantidproject/documents/tree/master/Design/Imaging_IMAT/SCARF_Platform_LSF/
(with Python client scripts).

### MPI-like behaviour

Integration of MPI into the scripts was considered, but the cost of having to transfer the large data over the network is too high. 

An alternative approach will be taken - since we can specify indices that can be loaded, the 'MPI' can simply be wrapped in a bash script that launches multiple reconstruction jobs, each one with different indices. The indices are also taken into account when saving out so that no files will be overwritten.
