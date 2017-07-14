<!-- TOC -->

- [1. Motivation](#1-motivation)
- [2. Old Tomography GUI Design](#2-old-tomography-gui-design)
- [3. Addressing of old Tomography GUI problems with the new Python GUI](#3-addressing-of-old-tomography-gui-problems-with-the-new-python-gui)
- [4. User Requirements](#4-user-requirements)
- [5. Development Requirements](#5-development-requirements)
- [6. Terminology](#6-terminology)
- [7. Finalising name choice](#7-finalising-name-choice)
- [8. Project setup](#8-project-setup)
    - [8.1. Continous Integration with Coverage](#81-continous-integration-with-coverage)
    - [8.2. Installation](#82-installation)
    - [8.3. Testing](#83-testing)
    - [8.4. Interfaces](#84-interfaces)
        - [8.4.1. Core](#841-core)
        - [8.4.2. GUI](#842-gui)
- [9. Guidelines for ISIS Imaging CORE](#9-guidelines-for-isis-imaging-core)
    - [9.1. Filter implementation expansion](#91-filter-implementation-expansion)
        - [9.1.3. cupy](#913-cupy)
        - [9.1.4. OpenCV](#914-opencv)
        - [9.1.5. numba](#915-numba)
        - [9.1.6. dask](#916-dask)
        - [9.1.7. VTK Imaging](#917-vtk-imaging)
    - [9.2. Reconstruction tools expansion](#92-reconstruction-tools-expansion)
    - [9.3. Problems with moving to Python 3.5+](#93-problems-with-moving-to-python-35)
    - [9.4. File Structure](#94-file-structure)
    - [9.5. Filters - General implementation structure](#95-filters---general-implementation-structure)
- [10. Guidelines for ISIS Imaging GUI](#10-guidelines-for-isis-imaging-gui)
    - [10.1. General Structure](#101-general-structure)
    - [10.2. ui Compiling](#102-ui-compiling)
    - [10.3. Using iPython](#103-using-ipython)
    - [10.4. Loading](#104-loading)
    - [10.5. Handling multiple stacks in dialogues](#105-handling-multiple-stacks-in-dialogues)
    - [10.6. Saving](#106-saving)
    - [10.7. Visualisation](#107-visualisation)
    - [10.8. Histograms](#108-histograms)
    - [10.9. Contrast normalisation](#109-contrast-normalisation)
    - [10.10. Applying a filter](#1010-applying-a-filter)
        - [10.10.1. Dynamic dialogue building](#10101-dynamic-dialogue-building)
        - [10.10.2. Transferring information from the dialogue (the parameters) to the execution](#10102-transferring-information-from-the-dialogue-the-parameters-to-the-execution)
    - [10.11. Preview a result](#1011-preview-a-result)
    - [10.12. Undoing an operation](#1012-undoing-an-operation)
    - [10.13. Process List](#1013-process-list)
        - [10.13.1. Store image state as part of the History in the process list](#10131-store-image-state-as-part-of-the-history-in-the-process-list)
        - [10.13.2. Exporting of Process List](#10132-exporting-of-process-list)
    - [10.14. Processing a full volume](#1014-processing-a-full-volume)
    - [10.15. Issues with Finding Center of Rotation and Reconstruction](#1015-issues-with-finding-center-of-rotation-and-reconstruction)
        - [10.15.1. Automatic Center of Rotation (COR) with imopr cor](#10151-automatic-center-of-rotation-cor-with-imopr-cor)
        - [10.15.2. Center of Rotation (COR) with imopr corwrite](#10152-center-of-rotation-cor-with-imopr-corwrite)
        - [10.15.3. Tilt correction](#10153-tilt-correction)
        - [10.15.4. Visualising the tilt](#10154-visualising-the-tilt)
        - [10.15.5. Calculating the real tilt angle](#10155-calculating-the-real-tilt-angle)
    - [10.16. Reconstruction](#1016-reconstruction)
    - [10.17. Tools and Algorithms](#1017-tools-and-algorithms)
    - [10.18. Remote submission and MPI-like behaviour](#1018-remote-submission-and-mpi-like-behaviour)
        - [10.18.1. Remote compute resource used at ISIS: SCARF](#10181-remote-compute-resource-used-at-isis-scarf)
        - [10.18.2. MPI-like behaviour](#10182-mpi-like-behaviour)

<!-- /TOC -->

The user requirements for the interface have been listed [here](https://github.com/mantidproject/isis_imaging/wiki/High-Level-User-Requirements-and-Use-Cases) and have been reviewed and confirmed by the imaging scientists.

The development requirements, following from the user requirements, are listed [here](https://github.com/mantidproject/isis_imaging/wiki/High-Level-Development-Requirements-and-Guidelines)

# 1. Motivation

The current [Tomography Reconstruction](https://github.com/mantidproject/mantid/tree/043095a619bc8851942a31253a1a8f8b820ab30f/MantidQt/CustomInterfaces/inc/MantidQtCustomInterfaces/Tomography) interface was found to not satisfy the current imaging requirements. An easy solution to the problems was not found. With the agreement of the IMAT imaging scientists and senior members of the Mantid team, work is to be started on this design for a rewrite of the interface. Python is the preferred language here, in order to be able to make use of visualising libraries like Matplotlib and interactions with Python based reconstruction packages like Tomopy.

# 2. Old Tomography GUI Design

- Note: In the images all things in red rectangles do not work. All things in blue rectangles DO work.

The `Run` tab handles the selected tool and it's parameters, the logging into the compute resource for remote reconstruciton, and the directories for input images. All of these things can be provided through a File/Action menu to not clutter the screen, as all of them need to only be performed once.

![Run Tab](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/runtab.png)

---

The `Filters` tab contains all available filters. They are not automatically generated, and need to be manually changed to reflect any additions or removals.

The interface of this tab does not allow for an easy way to apply a filter to the visualised images and see the results. The option to apply a filter could be provided by adding buttons for each filter, but that would also require to import the Python module in the C++ code to run the actual processing.

The user will also not be able to see the results without switching to the `ROI etc` tab, which does the visualisation.

![Filter Tab](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/filtertab.png)

---

The `Convert` and `Energy bands` tabs don't need to be independent tabs, as their functionality can be provided through simpler File/Action menu options:

![Convert and Energy tabs](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/convertandenergytabs.png)

---

Confusing `System` tab to handle all possible paths, except the data paths, which are handled in the `Run` tab:

![System tab](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/systemtab.png)

---

The Region of Interest tab is the hardest one to fix, as we need to manually implement automatic scaling to window size, correct region of interest translation that takes into account the scaling, zoom, moving the image after zoom, and other features that are expected to be present in an imaging program:

![ROI tab 1](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/roitab1.png)

![ROI tab 2](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/roitab2.png)

---

Other functional problems with the GUI:

- No flexible layout
- Cannot load more than one image/image volume at any time
- Cannot preview results from filters
- Cannot easily handle and move data around. From Python Numpy arrays to C++ is possible, but when we add more reconstruction tools, CuPy(CUDA), OpenCV, etc, handling the data in C++ gets a lot harder than it is in Python.
- Communication between different tabs was necessary, making the code _very_ convoluted when each tab is an MVP.
- Tedious and error prone manual updating of any CLI changes

Drawbacks of switching to a Python GUI:

- The GUI has to be redesigned and implemented
- We cannot reuse the existing mocking and testing
- We cannot reuse the remote submission algorithm, unless we want to have dependency on the Mantid Framework for a single algorithm

# 3. Addressing of old Tomography GUI problems with the new Python GUI

Usage of Matplotlib to implement a new ROI tab comes with all the features we would need to manually implement otherwise, and is one of the biggest PROs for a GUI in Python.

In Python we also get easier integration with the rest of the reconstruction scripts (the `isis_imaging.core` package), previously there were a lot of files that were just plain data structures that hold all of the available filters and their command line parameters. This means a change in the `core` scripts needs to be _manually_ reflected into the GUI code.

The `core` scripts were rewritten in January 2017, to fix previous problems they had with handling larger stacks and generally poor documentation/structure, making maintenance and testing impossible, and any extension with filters or reconstruction tools hard. This rewriting broke the ability to run a reconstruction from the old Tomography GUI, because the CLI changed, but the old CLI was hard-coded to the C++ interface.

- No flexible layout
- Cannot load more than one image/image volume at any time

The Python GUI makes use of the `QDockWidget` class to provide a layout that is flexible and supports different ways to view and structure the visualisation. An example of that can be seen here:

![Main Window with all possible stack window positions](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/all_views.png)

This image shows off a few ways that loaded stacks can be positioned. It allows for any combination of any preferred positioning.

- Cannot preview results from filters

As seen in the image above, there is a `Filter` submenu. That menu lists all available filters, and they can be applied to a selected stack, visualising the results immediatelly. A preview option will be provided for each filter in order to be able to preview the result on the stack, without processing all of the images it contains.

- Cannot easily handle and move data around. From Python Numpy arrays to C++ is possible, but when we add more reconstruction tools, CuPy(CUDA), OpenCV, etc, handling the data in C++ gets a lot harder than it is in Python.
- Tedious and error prone manual updating of any CLI changes

Because now we can easily interface with the `core` package, we can access all of its CLI directly, and we don't have to manually change it in another file. Filters are registered dynamically, and any future additions, from developers or users, can easily be added to extend the available functionality.

- Communication between different tabs was necessary, making the code _very_ convoluted when each tab is an MVP.

The new Python GUI structure currently uses the Main Window's model to only _track_ the existence of loaded stacks' windows, and call the necessary deletion when they are closed.

There is no information that is shared between the stacks. Any operations on the actual images are forwarded to the stack window itself, which also stores any information related to the image volume its holding.

It is still possible to globally share by storing the _shared_ information into the Main Window's Model, it will be available to every stack that has been loaded, in a more convenient and centralised way, but there has not been a use case for that functionality so far.

- We cannot reuse the existing mocking and testing

The new GUI will implement the MVP pattern, whenever sensible, to make sure that the testing is fully automated. Combined with the reduced complexity of the new GUI, the new testing coverage should be better than the old one.

- We cannot reuse the remote submission algorithm, unless we want to have dependency on the Mantid Framework for a single algorithm

There is an example provided, in Python, for communicating with the REST API of the SCARF cluster. Reimplementing such a connection will be much easier in Python than C++.

# 4. User Requirements

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

# 5. Development Requirements

1. Unit testing for CORE
1. GUIs use MVP pattern with mocking and unit testing for GUIs
1. System tests to ensure larger module functionality
1. Maintain Documentation
1. Continous Integration on Github
1. Installation

# 6. Terminology

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

# 7. Finalising name choice

- MantidImaging
- ISIS_Imaging
- Other suggestions?

# 8. Project setup

## 8.1. Continous Integration with Coverage

The package should have a continous integration flow on Pull Requests, which runs all of the CORE and GUI tests. This should also include coverage.

After sphinx documentation is added, the contiguous integration could also check if it builds successfully.

## 8.2. Installation

We can either work towards the package being installable using `python setup.py install`, making it available system wide. The alternative solution is to use it from the folder and provide global access like [the example here](https://mantidproject.github.io/isis_imaging/user_guide/setting_up.html#global-access-to-the-package)

## 8.3. Testing

Testing will use `nose` to run the tests and `coverage` to compute the tests' coverage. The actual unit tests should use the built-in `unittest`, and some might have to use `numpy.testing` for asserting equality for `numpy.ndarrays`.

A module to run the tests has been provided and is called `run_tests.py`, in the root of the repository. It takes as an argument the names of different packages, and then runs the tests specifically for them. The possible arguments are listed via `-h` flag, or at the top of the file in the source.

There is currently no integration with Mantid's testing.

## 8.4. Interfaces

The project aims to have multiple interfaces:

- Command Line Interface (CLI)
- Graphical User Interface (GUI)
- iPython interface (also helps development IDEs for suggestions)

This is currently achieved by manually structuring the public API of each package. This can be seen in most `__init__.py` files. They import specific files, or only specific functions from the files, which are visible to the external caller.

This also allows for a full separation of the GUI from any of the other interfaces. This is required because we do not want to install PyQt5 and other GUI packages on SCARF, and is also good practice.

### 8.4.1. Core

Every module should have associated unit tests, unless there is good reason not to have one.

There should also be a collection of system tests to make sure that the functionality works on a higher level than unit tests.

### 8.4.2. GUI

The GUI should use the MVP pattern, making it easier to mock and unit test. Mocking should be done with the python built-in `mock`. There should be an associated mock and presenter unit testing for every MVP used.

Simpler cases like the `load`/`save` dialogues do not need to use MVP, because they have very little, if any, logic.

# 9. Guidelines for ISIS Imaging CORE

Issues related to the `core` package of ISIS Imaging have the `Component: Core` label, following the Mantid Repository issue structure. [Link to issues for core](https://github.com/mantidproject/isis_imaging/issues?q=is%3Aopen+is%3Aissue+label%3A%22Component%3A+Core%22)

## 9.1. Filter implementation expansion

Integrating a package that supports CUDA has potential for improvement and expansion of the imaging filters.

A potential problem for CUDA is for machines with low VRAM, transferring the data multiple times might be slower that just doing it in a bulk in the CPU, if it has a lot of RAM.

### 9.1.3. cupy

- Note: [Link, Supports Python 3](https://docs-cupy.chainer.org/en/stable/install.html)

This package supports CUDA and nicely implements most of the `numpy` API, meaning it can make transition over to GPU processing easy, for filters that only use `numpy` functions (background correction, contrast normalisation, etc).

For filters requiring custom code, kernels for other filters like Median, Gaussian, etc, can be written additionaly. [Related issue on repository.](https://github.com/mantidproject/isis_imaging/issues/50) This issue links to a response in the CuPy repository about how to write CUDA kernels in external files and then compile them inside during Python execution.

I would recommend asking on the [CuPy repository](https://github.com/cupy/cupy) for implementation (and performance wise) advice before finalising the implementation of any filter.

### 9.1.4. OpenCV

- Note: [Link, Supports Python 3](https://pypi.python.org/pypi/opencv-python)

This is a library for image processing and computer vision, it has a lot of features, but is also quite large. I have added it here as it should be considered if there is anything available that is needed. It is available on the SCARF/Emerald cluster, making it potentially usable.

Something that might cause issues - I am not sure how well it integrates with `numpy` arrays, for C++ they use their own internal type `cv::Mat` and I have not used the Python bindings.

### 9.1.5. numba

- Note: [Link, Supports Python 3](http://numba.pydata.org/numba-doc/latest/user/overview.html)

Numba is a compiler for Python array and numerical functions that gives you the power to speed up your applications with high performance functions written directly in Python.

Numba generates optimized machine code from pure Python code using the LLVM compiler infrastructure. With a few simple annotations, array-oriented and math-heavy Python code can be just-in-time optimized to performance similar as C, C++ and Fortran, without having to switch languages or Python interpreters.

### 9.1.6. dask

- Note: [Link, Supports Python 3](https://dask.pydata.org/en/latest/)

Dask is a flexible parallel computing library for analytic computing.

Dask is composed of two components:

Dynamic task scheduling optimized for computation. This is similar to Airflow, Luigi, Celery, or Make, but optimized for interactive computational workloads.
“Big Data” collections like parallel arrays, dataframes, and lists that extend common interfaces like NumPy, Pandas, or Python iterators to larger-than-memory or distributed environments. These parallel collections run on top of the dynamic task schedulers.

### 9.1.7. VTK Imaging

- Note: [Doesn't seem to have a Python 3 version in Conda or Pip](http://www.vtk.org/features-imaging/)

In the context of visualization, image processing is most often used to manipulate image content (either two- or three-dimensional images) and improve the results of subsequent processing and interpretation. VTK is quite capable at working with images. It has a large number of filters dedicated to the purpose, most of which are multi-threaded, and support for streamed processing of regions of interest is built into the pipeline.

## 9.2. Reconstruction tools expansion

- [Astra Toolbox](http://www.astra-toolbox.com/), [Supports Python 3](http://www.astra-toolbox.com/docs/install.html#for-python)
- [MuhRec](http://www.imagingscience.ch/downloadsection/), No Python Bindings

## 9.3. Problems with moving to Python 3.5+

In an attempt to move the Python version requirement to 3.5, I have come across an extreme slowdown in initial memory allocation and processing performance.

The reason has been outlined in [http://bugs.python.org/issue30919](http://bugs.python.org/issue30919), and it seems to be a behaviour change in `multiprocessing`'s shared memory allocation on Unix systems between python 2.7 and 3.5.

- In 2.7 the memory was actually allocated in memory, and then shared with subprocesses.
- In 3.5 the memory is written out as a file, which is then used as the 'shared memory' between subprocesses. The reason for that is that Python 3.x supports more ways of creating subprocesses, so this was the only way to support all of them. This means that memory initialisation and processing are now IO bound.

However, as I do not think any of the additional ways of creating subprocesses are useful for this package, this change makes moving to 3.x impossible, until a workaround is found. I have taken the following steps as possible solutions:

- I've asked on the Python issue board if anyone has a way to force the python 2.7 behaviour in python 3.5, this would by far be the easiest solution, as no significant code change will be necessary. However it might require changes to the Python source code, which I am not happy about, as I want to use a standard python distribution
- I am looking into packages that can be used instead of the built-in `multiprocessing`, to handle the parallel processing. Some have already been added to the design document, like `dusk` and `numba`. The problem with this approach is that neither `dask` nor `numba` are available on SCARF right now, but they can be requested and added.

## 9.4. File Structure

Using Python's modular structure is encouraged. Focus on having stateless free functions within modules.

Custom objects should be used where state needs to be preserved, for example the `core.imgdata.saver.Saver` stores all necessary information about saving, so that further function calls are simplified. However, the actual `save` function is a module function that can be accessed without creating an instance of the class.

Another example is in the `core.tools` module, we want to enforce a common interface. This is done via having an `AbtractTool` that the other tools should inherit from, and should implement its interface.

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

## 9.5. Filters - General implementation structure

- Filters should be inside a package that only exposes `execute`, `gui_register`, `cli_register`, and any other functions desired to be part of the public API. This will be enforced in the package's `__init__.py`
  - This allows to have a strict API regardless of the internal implementation inside the package, so that is left is up to the developer. They could be in a single `.py` module, or in a separate module for each large function -> `execute.py`, `gui.py`, `cli.py`, etc.
- All of the filters must implement an `execute` function that takes the image volume as its first parameter. The following parameters should be the ones necessary for execution, and the last two should be `cores` and `chunksize`. The reason for having `cores` and `chunksize` in every filter's API is to make them usable standalone through iPython, or external scripts without having to construct a configuration object.
- All filters must implement a parallel and sequential execution. How that is done is up to the developer.
- Future extensions could be adding CUDA execution to some/all fitlers. This would ideally be handled as part of the checks for parallel inside the `execute` function, but if that is not possible or desirable, a new function might be added to the API specifically for CUDA execution.

# 10. Guidelines for ISIS Imaging GUI

Issues related to the `GUI` package of ISIS Imaging have the `Component: GUI` label, following the Mantid Repository issue structure. [Link to issues for GUI](https://github.com/mantidproject/isis_imaging/issues?q=is%3Aopen+is%3Aissue+label%3A%22Component%3A+GUI%22)

## 10.1. General Structure

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

![Main Window with all possible stack window positions](https://github.com/mantidproject/documents/blob/tomography_gui/Design/. $/all_views.png)

The Main Window allows us to place the stack in multiple different places:

- As tabs (seen bottom left)
- On the right of the tabs, inside the main window
- Floating around

## 10.2. ui Compiling

Currently the `.ui` is compiled dynamically while running. It might be better if this is changed to the mslice approach where all of the `.ui` files are compiled during 'build' and `.uic` files are created.

## 10.3. Using iPython

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

## 10.4. Loading

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

## 10.5. Handling multiple stacks in dialogues

It will be possible to have more than one stack loaded at a time. A unique ID will be generated for each new stack that is loaded. The ID is then stored with the folder name as a 'user friendly name', and a reference to the QObject containing the stack. The unique ID will be generated using python's `uuid` package.

On closing the image volume window we need to remove any references to the stack. Qt provides `closeEvent` which is triggered when the user clicks the `X` button. Each stack window will know it's own unique ID, it should delete it from the dictionary, and also remove the reference to any data it might be holding.

Building the selection for the user will be an iteration of the dict, sorted by key and displaying the user friendly name, but also store the uuid to be able to reference the data afterwards.

## 10.6. Saving

The saving dialogue will have a drop down menu, kept up to date with what active stacks there are in the main window. The user can then select a stack, select the format (by default `.tiff`) and save it out to the path they point to. The supported formats dropdown menu will be populated at runtime by using the loader's available extensions function, which is already used when building the command line interface help (-h).

## 10.7. Visualisation

The MainWindow will have a `QDockWidget`. Each image volume will be a child `QWidget` inside the main `QDockWidget`. This allows usage of the flexibility of `QDockWidget`, making it possible to have docked windows, docked tabs, floating windows, or any combination of those. The users will be able to arrange the visualised stacks in any way they want. The first stack visualised should be docked inside the MainWindow, be centered and take up all of the space. Any consecutive stacks that are loaded will be placed inside the MainWindow automatically by Qt.

For the actual visualisation `FigureCanvasQtAgg` will be used with the default drawing algorithms. If this proves to be too slow, the drawing function may need to be changed or adapted.

The visualisation must have a rectangle ROI selection, that is persistent if the image underneath is changed. Matplotlib provides a `RectangleSelector` class which will be used to do the ROI selection. It changed dynamically with size and correctly translated the coordinates regardless of image scale, zoom or position.

The user must be able to go to any index from the volume. This will be done via a slider. The implementation of the slider should be generic, and allow to have a few different sliders with different look and feel.

The visualisation should also have the toolbar that appears on plots in Matplotlib, the functionality that comes with the default toolbar works with the images.

## 10.8. Histograms

Computation of the histograms should be done only on the ROI, if no ROI is selected the whole image will be used. The computation itself should be implemented in the `core.algorithms` package. It might be necessary to do so asynchronously. The `matplotlib` histogram feature was found to be quite slow. An alternative could be `np.histogram`, but that has not been benchmarked.

Visualisation should be a small independent widget detached from the stack. This histogram needs to provide a way for the user to select a range of values that are to be used for contrast normalisation.

Maybe the default `matplotlib.pyplot` can be used, if there is a way to keep track of the range of values that the user has selected and feedback to the contrast normalisation.

For the histogram window an `mslice` approach could be taken where the user can choose to:

- `Keep` the histogram, meaning new histograms will take place in a new window
- `Current selection` on the histogram, meaning new histogram will replace the one in the window

Keeping multiple histograms around shouldn't be a memory issue, and they be binned, reducing the memory usage further.

## 10.9. Contrast normalisation

Matplotlib provides a method to specify contrast range via `set_clim` method on the image. The values will be read from the histogram and the image will be changed when the user changes the selected range of values in the histogram.

## 10.10. Applying a filter

Applying a filter will bring up a dialogue in which the user has to select on which stack to apply the filter via a dropdown menu, and fill in the required parameters the filter has.

Any filters should be dynamically registered using the [registrator](https://github.com/mantidproject/isis_imaging/blob/master/isis_imaging/core/algorithms/registrator.py) style approach. Filters will have to implement `cli_register` and `gui_register` functions that register them with the command line and graphical interface, respectively, in order to be visible on each of the interfaces.

Current issues for this section:

### 10.10.1. Dynamic dialogue building

- Solution is to use an approach like the `cli_registrator`, but pass in the QObject in which the filters will register themselves in
- Dialogue registration is a bit more complicated, because we have to connect the dropdown menu to the dialogue's `.show()` method.

### 10.10.2. Transferring information from the dialogue (the parameters) to the execution

- The filter should be executed from inside the image visualiser. The main window does not have reference to any data, only the QWidgets that contain the visualisation.
- Using a partial function, we can decorate with all of the parameters. No other function down the chain of execution will have to worry about the parameters that way.
    - Alternative is to store the state as a global object inside each filter's module. On `execute` if no parameters are provided, then they are read, by default, from the global object.
- Requesting a parameter from the visualiser
    - There are some filters that operate on a region of interest of the image volume.  Because the dialogue and the image stacks have no way to communicate, there is no way to read in what region has been selected by the user.
    - A possible solution is to allow the dialogues to 'request' for a parameter from the image visualiser. The parameters that would be available initially are Region of Interest, flat/dark images.
- Handling filters with multiple steps
    - Background correction and contrast normalisation need to calculate values for scaling, do the filter execution, and then apply the scaling to the images.
    - Currently the solution is to apply a monad style approach.

## 10.11. Preview a result

This can be an option in the filter dialogue. It will be passed as a parameter to the image visualiser. If preview is selected the data will be deepcopied and processed, resulting in a new stack with the processed data.

## 10.12. Undoing an operation

Building the Undo operation may be complicated and turn out to consume too much memory, but provides better functionality. Initially should not be part of the implementation.

Some issues:

- Storing the original state as a deepcopy, and then applying the filter inplace on the volume of images, works best with single image.
- Serious memory implications for large volumes.
- Can easily store a single undo (like imagej, only for single images), multiple undos can be hard to implement efficiently because of all the memory being copied

## 10.13. Process List

Every operation on the image volume should be saved in a `ProcessList`, which can then be exported and re-used on another image volume. The process list acts like a `queue`, first-in first-out.

A problem that appears with that approach is that some images need more than one stack for an operation, e.g. background correction needs flat and dark images as well. Running a process list on a different stack will not know from where to read in the flat and dark images, they would need to be specified by the user. Possible solutions:

- Ask for flat and dark paths in image loading dialogue and cache them for the loaded stack, then the process list can reuse them
- Ask for flat and dark paths when the filter is popped from the Process List queue

### 10.13.1. Store image state as part of the History in the process list

This is not done in the current implementation of the `ProcessList`. This could be added as a replacement for [Undoing an operation](#undoing-an-operation), but it suffers from the same issues as undoing.

### 10.13.2. Exporting of Process List

This is something considered as part of the [remote submission](#remote-submission-and-mpi-like-behaviour) implementation. It will require implementing functions to export an exsiting process list to a format that later can be read back and construct a new Process List.

## 10.14. Processing a full volume

A process list should provide the option to be applied to the whole stack locally. Details for the implementation need to be considerend alondside the [Undoing an operation](#undoing-an-operation) implementation.

The process list will store the operation(+params) that needs to be applied. Doing this for the whole stack would simply require walking through the process list. There is _nothing_ currently implemented in the `core` module that allows for that.

A new configuration might have to be added in `core.configurations` to handle this type of ordered filter application. A class that takes the name and dynamically imports/applies the operation might also be required.

## 10.15. Issues with Finding Center of Rotation and Reconstruction

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

### 10.15.1. Automatic Center of Rotation (COR) with imopr cor

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

### 10.15.2. Center of Rotation (COR) with imopr corwrite

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

### 10.15.3. Tilt correction

Sometimes the samples are tilted slightly. On the one above, the difference in COR between the top and the bottom looks like this:

| Slice |  COR  |
| ----- | ----- |
|  422  |  542  |
|  822  |  540  |
| 1222  |  540  |
| 1622  |  537  |
| 1822  |  536  |

As you can see there is a bit of a difference near the top (slice 422) and the bottom (slice 1822). In this case it's not a lot, only 6 pixels.

However it needs to be accounted for during the reconstruciton. This is currently done in `core.algorithms.cor_interpolate`, which requires the information above (slice and associated COR) and interpolates the rest of the CORs for the slices in between. This method has worked quite well so far, because Tomopy lets us specify a COR for each slice, by providing a list that is of the same length as the number of sinograms.

We can supply the slice/cor information through the command line:

`isis_imaging -i /some/data --cors (the cors from the table) --cor-slices (the slices from the table) ...`

The number of cors and the slices is enforced to be equal. The only exception is that we can provide a single number to `--cors`, which will then be assigned to the whole stack. Some lucky samples happen to have the exact same COR for every slice.

### 10.15.4. Visualising the tilt

Knowing the COR for each slice (or interpolating the approximation) gives us information that we could display back to the user. Every COR for a slice maps back to a pixel on the projection image. This means we can create a line that is slightly tilted and crosses the projection's center. An exaggerated visualisation looks like this (done by hand, not accurate to the actual COR, but converys the idea):

![Exaggerated Tilt](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/exaggeratedtilt.png)

This is something that has been expressed as a required feature by the scientists, anmd should not be too hard to implement. The rectangle selection class, also has an option to be a line. We could create it as a line and display it as a separate object on the visualisation.

### 10.15.5. Calculating the real tilt angle

This is a technique for calculating the angle of tilt, which hasn't been verified by the scientists so it might not be correct, but it doesn't hurt to document it. Having the tilt line (as in the exaggerated tilt above), we can add another line, which is straight and is the length of the image's width, like this:

![Straight line and Tilt line](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/straightlinetilt.png)

We can see there is an angle where they cross. That angle should be how far the sample is tilted from the perfect straigth line. If we move the line to end at the last COR, the calculation can be a bit easier:

![Moved straight line and tilt line](https://github.com/mantidproject/documents/blob/tomography_gui/Design/ISIS_Imaging/straightlinetilt2text.png)

Calculating the theta angle from the image above should give us the actual tilt. I am not sure if the technique is accurate or correct, and suggestions for improvements are welcome.

## 10.16. Reconstruction

The reconstruction works on sinograms and will be done via third party tools Tomopy, Astra Toolbox, MuhRec, etc.

Specific dialogues might have to be created for each tool, to handle the different parameters each one has.

The package has been expanded to require the `--reconstruction` flag to be specified, in order to run the actual reconstruction code. Currently there is a problem that the pre-processing and the reconstruction cannot be done in a single execution, because we cannot convert to sinograms without breaking the contiguous memory and increase the memory usage. The current solution is to convert to sinograms first, save out, and reload the data into a reconstruction run.

A reconstruction submission requires CORs to be specified, and would look like this:

Specifying a common COR for every slice:

`isis_imaging -i /some/sinograms --cors 440 --reconstruction -o /some/output`

Specifying CORs from which the rest will be interpolated:

`isis_imaging -i /some/sinograms --cors 440 450 460 470 --cor-slices 100 200 300 400 --reconstruction -o /some/output`

The reconstruction of a single slice is an atomic operation on the slice. The way it runs in parallel is that each thread/process gets a slice and reconstructs it.

## 10.17. Tools and Algorithms

The tool and algorithm defaults are `tomopy` and the algorithm `gridrec`. The tool can be specified with `-t` or `--tool`, the algorithm with `-a` or `--algorithm`.

## 10.18. Remote submission and MPI-like behaviour

Remote submission needs to be supported, that means we need to be able to submit the reconstruction/processing parameters through the REST API they provide. Information about the reconstruction should be stored in a `ProcessList`, which can be serialised and then recreated anywhere with the `--process-list` flag.

### 10.18.1. Remote compute resource used at ISIS: SCARF

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

### 10.18.2. MPI-like behaviour

Integration of MPI into the scripts was considered, but the cost of having to transfer the large data over the network is too high.

An alternative approach will be taken - since we can specify indices that can be loaded, the 'MPI' can simply be wrapped in a bash script that launches multiple reconstruction jobs, each one with different indices. The indices are also taken into account when saving out so that no files will be overwritten.
