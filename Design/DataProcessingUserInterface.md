#Data Processor User Interface#

##Motivation##

Mantid user interfaces, while simple to create, have caused some of the largest long-term problems in Mantid. Large numbers of users interact with Mantid via technique specific interfaces. Fragility of a single UI can taint the view of the whole project. On the other hand, maintenance has consuming valuable time in development resources for little benefit to the wider project. The movement towards MVP and similar approaches have mitigated some of these problems through the introduction of fast, automated testing. There are several very successful examples of where this approach has been applied to Mantid.

More recently, we developed a [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html), which has provided a neat and concise way to execute complex batch-processing via [DataProcessorAlgorithms](http://doxygen.mantidproject.org/nightly/dd/ddc/classMantid_1_1API_1_1DataProcessorAlgorithm.html). This was developed using our experience of the *MVP Passive View* approach. IOC has allowed us to impement some powerful and reusable features, such as Auto-completing option selection, Data searching/loading, Reduction settings loading, and pre and post-processing reduction in a way that does not strongly tie us into a given solution, or even to a specific techinque area.

Many technique areas have now developed DataProcessorAlgorithms, as this is now the accepted solution to the worflow algorithm problem. Several technique areas are now asking for similar functionality, and **it makes long-term sense to generalize what has been done in [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) to avoid the maintenace effort drain we see involved in looking after specific UIs**.

**Summary of benefits:**

* Much less effort expended looking after technique specific user interfaces
* Standardisation across similar user interfaces
* Would introduce a powerful and standard way to make batch processing User interfaces in Mantid with very few customisations required for each technique area.
* Auto-complete options for overriding defaults in each row. Options taken from DataProcessorAlgorithm, can optionally blacklist.
* Can include ICat and other mechanisms for Data search and batch generation
* DataProcessorAlgorithms record nested history. So GUIs that execute these algorithms give full algorithmic traceability.
* Linked to the above. We now have the ability to generate electronic notebooks via [GenerateIPythonNotebook](http://docs.mantidproject.org/nightly/algorithms/GenerateIPythonNotebook-v1.html). This feature has already been built into [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html)
* Hooks for pre and post processing available much like the operation of [StartLiveData](http://docs.mantidproject.org/nightly/algorithms/StartLiveData-v1.html)

##Requirements##

1. Should require minimal inputs to get things going. The DataProcessor algorithm should be the only required input.
1. Should be exposed to python
1. Should allow imports of existing table data as a ITableWorkpsace
1. Should allow saving of table data as a ITableWorkspace
1. Should allow optional hook for execution of row/run pre-processing such as is done [here](https://github.com/mantidproject/mantid/blob/master/MantidQt/CustomInterfaces/src/ReflMainViewPresenter.cpp#L545)
1. Should allow optional hook of row/run post-processing such as is done [here](https://github.com/mantidproject/mantid/blob/master/MantidQt/CustomInterfaces/src/ReflMainViewPresenter.cpp#L705:L717), albeit not well extracted at this time.
1. Should allow for treatment of *Grouped rows* or some other post-processing grouping.
1. Should allow blacklisting of DataProcessingAlgorith properties.
1. Should allow for renaming of column headings in the table, where the algorithm property names are not a good fit.


##Proposed Solution##

The high-level solution involves refactoring and further generalizing the Reflectometry Reduction Interface into a **Data Processor User Interface**.

**Key solution features**
* The bulk of the solution will be about generating a `MantidQt::API::UserSubWindow` subclass called `DataProcessorAlgorithmWindow`  
* `DataProcessorAlgorithmWindow`  will take the name of the `DataProcessorAlgorithm` as one of its construction arguments
* The `DataProcessorAlgorithmWindow` will provide both virtual functions for overriding a `preProcess` and `postProcess` step and signals for those events. I believe the signals will be more python friendly.


##Questions##

1. [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) has a nice mechanism for importing workspaces. It attempts to resolve the input either as a workspace, or as a file, and will add together listed runs separted by a `+`. Is this generic enough? Do we wish to further expand pre-processing steps?
2. Exactly how much of the [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) do we want to provide? Not all menus are needed. For example SlitCalculator is very specific. However Addition, deletion of row etc. Makes a lot of sense. What about the ICAT import?


