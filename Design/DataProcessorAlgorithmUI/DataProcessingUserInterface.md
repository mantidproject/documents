#Data Processor User Interface#

##Motivation##

Mantid user interfaces, while simple to create, have caused some of the largest long-term problems in Mantid. Large numbers of users interact with Mantid via technique specific interfaces. Fragility of a single UI can taint the view of the whole project. On the other hand, maintenance has consuming valuable time in development resources for little benefit to the wider project. The movement towards MVP and similar approaches have mitigated some of these problems through the introduction of fast, automated testing. There are several very successful examples of where this approach has been applied to Mantid.

More recently, we developed a [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html), which has provided a neat and concise way to execute complex batch-processing via [DataProcessorAlgorithms](http://doxygen.mantidproject.org/nightly/dd/ddc/classMantid_1_1API_1_1DataProcessorAlgorithm.html). This was developed using our experience of the *MVP Passive View* approach. IOC has allowed us to implement some powerful and reusable features, such as Auto-completing option selection, Data searching/loading, Reduction settings loading, and pre and post-processing reduction in a way that does not strongly tie us into a given solution, or even to a specific techinque area.

Many technique areas have now developed DataProcessorAlgorithms, as this is now the accepted solution to the workflow algorithm problem. Several technique areas are now asking for similar functionality, and **it makes long-term sense to generalize what has been done in [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) to avoid the maintenace effort drain we see involved in looking after specific UIs**.

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
2. Should allow for processing rows via remote launching

##Current Structure##

**Top Level Class Diagram**

![Top level class diagram](https://github.com/mantidproject/documents/blob/master/Design/DataProcessorAlgorithmUI/TopLevel.png)
* ReflMainView : Abstract View
* IReflPresenter : Abstract presenter. Has simple notification interface used by the QtReflMainView.
* ReflMainViewPresenter : Concrete IReflPresenter. Does all UI logic.
* IReflSeracher : Abstract service to allow searching of runs via instrument and investigation_id (or some other key)
* IReflTransferStrategy : Abstract strategy for brining runs into the table, grouping them, etc.

**Table Centric Class Diagram**

![Table class diagram](https://github.com/mantidproject/documents/blob/master/Design/DataProcessorAlgorithmUI/TableModel.png)
* QReflTableModel: Implements QAbstractModel. Is the MVC model.
* QReflTableView : Takes a QAbstractModel via setModel. Renders the table on the QReflMainView
* ITableWorkspace : Should be built from the DataProcessorWorkspace description. Defines the data for the batch processing

**Other Important Actors**
* HintingStrategy : Abstraction of a mechanism to provide hinting information in for a TableColumn (Options column)
* AlgorithmHintingStrategy : Concrete HintingStrategy taking a DataProcessorAlgorithm and a blacklist of property names not to show.
* HintingLineEdit : Line editor which applies the HintingStrategy and is set to the QtTableView via setItemDelegateForColumn. Provides the Options column ability.

##Proposed Solution##

The high-level solution involves refactoring and further generalizing the Reflectometry Reduction Interface into a **Data Processor User Interface**.

**Key solution features**
* The bulk of the solution will be about generating a `QWidget` subclass called `DataProcessorAlgorithmWidget`  
* `DataProcessorAlgorithmWidget`  will take the name of the `DataProcessorAlgorithm` as one of its construction arguments
* The `DataProcessorAlgorithmWidget` will provide virtual functions for overriding a `preProcess` and `postProcess` 
* We also need a way to customise the output table in circumstances that direct mapping between `DataProcessorAlgorithm` properties and the viewable batch Table do not make sense. Currently `QReflTableModel` is specifically set up to do this for the `ReflectometryReductionOneAuto` DataProcessorAlgorithm.
* 

##Prototyping##

**Notes from Owen**

I've checked that sip exports of c++ QtObject base classes will behave as we expect on the python side. 

One problem that we will encounter is how to get sip and boost python exported representations to play together. The situations in which this would occur are where we want ot provide a custom `preProcess` and `postProcess` step, where by we need the ability to receive and modify workspaces, and run algorithms. I propose that a solution to this would be for the preProcess and postProcess steps to return the name of `Algorithms` that the algorithm manager on the c++ side could create and execute on their behalf. The API for these Algorithms would need to be fixed, and well tested to prevent runtime-issues.


##Questions##

1. [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) has a nice mechanism for importing workspaces. It attempts to resolve the input either as a workspace, or as a file, and will add together listed runs separted by a `+`. Is this generic enough? Do we wish to further expand pre-processing steps?
2. Exactly how much of the [Reflectometry Reduction Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html) do we want to provide? Not all menus are needed. For example SlitCalculator is very specific. However Addition, deletion of row etc. Makes a lot of sense. What about the ICAT import?
3. How do we deal with properties that should be shared for the entire table? Should there be a way to fill in an entire column, or a part of the gui that holds the "common" properties.

##Commments##
**Anders**

1. Design should be able to handle future formats users would like to use to set up algorithm properties and to save to such formats to, for example csv format
2. Would it be possible to list existing interfaces in Mantid that could potentially benefit from this design?
3. An answer to question 2 above: I favour a minimum set. If the list in the bullet point above is made (and for interfaces planed in the near future) a minimum feature set which satisfy these may be chosen

