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

##Target User Interfaces and Technique Areas##
We believe that the following Technique areas would benefit from this design. There are likely to be many more areas that would benefit.

| Tehnnique        | Facility           | Reasons Why  |
| ------------- |:-------------:| -----:|
|  Reflectometry    | ISIS | Already have a well-tested precursor of this design. But would benefit from common code and shared effort.  |
|  SANS   | ANSTO      |  Want batch mode processing of SANS data |
|  SANS   | ISIS      |  Have batch mode processing, but it's very basic, and are now talking about embedding python scripts into their csv batch table, to get around the lack of the `Options column. See below` |
| Powder | SNS | See justification below in selected use cases|
| SCD | SNS | See justification below in selected use cases |

##Requirements##

**Must Haves**

1. Should require minimal inputs to get things going. The DataProcessor algorithm should be the only required input.
1. Should be exposed to python
1. Should allow imports of existing table data as a ITableWorkpsace
1. Should allow saving of table data as a ITableWorkspace
1. Should allow optional hook for execution of row/run pre-processing such as is done [here](https://github.com/mantidproject/mantid/blob/master/MantidQt/CustomInterfaces/src/ReflMainViewPresenter.cpp#L545)
1. Should allow optional hook of row/run post-processing such as is done [here](https://github.com/mantidproject/mantid/blob/master/MantidQt/CustomInterfaces/src/ReflMainViewPresenter.cpp#L705:L717), albeit not well extracted at this time.
1. Should allow for treatment of *Grouped rows* or some other post-processing grouping.
1. Should have property mapping behaviours
 1. Should allow blacklisting of DataProcessingAlgorithm properties so that they can Never be specified.
 1. Should allow for white listing for *Optional* column. 
 1. Should allow for white listing for *Table* columns. Properties that will appear as table entries. Mandatory mapping must be provided.
1. Should have indirection between the `Presenter` and the `AlgorithmManager` via an `AlgorithmRunningService` not done in the current layout such that other ways of running the algorithm in the future (such as batch processing) via a job submission service could be supported. `AlgorithmRunningService` must be injectable.
1. Should have a way of brining in settings information that can not be derived from the other inputs. Such information would be added to *Hidden* table columns (in the gui), or most likely the Options column, so that exported ITableWorkspaces are self-contained.
2. 

**Should Haves**

1. Should have property mapping behaviours. Should allow for white listing for *Common Settings* area (Properties that are fixed for all reductions)  
1. Should allow for processing rows via remote launching
1. Should be easy to opt-in to parts of the above toolkit without having to implement everything. There should be default *behaviours* pre-configured. For example a `NullTransferStrategy` because transfers are going to be technqiue area specific. Another example might be that the `AlgorithmRunningService` is configured to use some `AlgorithmManagerVariant`
1. Should not assume that the AlgorithmRunningService is synchronous. Async behaviour is likely to be introduced, so would be best if the interface was set up to allow polling, or publish-subsribe notifications for completion.

**Could Haves (Future considerations)**

When it comes to batch processing variants. `AlgorithmRunningService`. We need a way to distribute the items in the table to acheive a good load-balancing. The problem comes with acheiveing post-processing on the server side. Post processing does not preclude inter-row dependencies. One way get around this would be to distribute according to equivalent group number. Another way would be to perform all post-processing on the client side.
 

##Selected Use cases##

1. `SNSPowderReduction` could benefit greatly from this as when users want to re-reduce they want to change a couple of parameters and re-reduce the whole experiment. Things that make this interesting:
  * There is a CharacterizationsFile which contains much of the information that could be used for filling in the table. Currently the information is brought (mostly) into a TableWorkspace via [PDLoadCharacterizations](http://docs.mantidproject.org/nightly/algorithms/PDLoadCharacterizations-v1.html) and then the correct row is selected with [PDDetermineCharacterizations](http://docs.mantidproject.org/nightly/algorithms/PDDetermineCharacterizations-v1.html). The user has the option to override the values found this way, but it gives a very good start.
  * Many of the parameters are common to the whole experiment's reduction (calibration file, final binning, output file formats, etc). The solution should have the ability to have an area for setting these common parameters, rather than forcing them to appear in every row.
2. For Single Crystal Diffraction (XSD) there is some amount of "twiddling" before reducing each of the individual goiniometer settings to a set of integrated peaks. Then the workflow requires combining all of the individual integrated peaks and finding a common UB matrix and re-indexing all of the peaks. One of the missing pieces in the current reduction, is moving parameters from the individual run to the batch run. This is currently done by hand.

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
* The deliverable will be a `QWidget` subclass called `DataProcessorAlgorithmWidget`. This widget provides table and table editing features. Visually, the widget will provide a graphical interface similar to the one currently provided for ISIS reflectometry data processing:

![refl_table](http://docs.mantidproject.org/nightly/_images/ISIS_Reflectometry_(Polref)_groupProcessPane_widget.png) 

* Clients provide a `DataProcessorPresenter` 
* This `DataProcessorPresenter` defines how the batch reduction occurs
* `Presenter` and related types are customizable both on the python and c++ side.


##Solution Details##



* `DataProcessorAlgorithmWidget`  will be the concrete form of a `DataProcessorAlgorithmView`
* The `DataProcessorAlgorithmWidget` will accept an abstract `DataProcessorPresenter`
* Double dispatch via a visitor setup, will be used to register the `DataProcessorAlgorithmView` and `DataProcessorPresenter` together
* A `GenericDataProcessorPresenter` will be provided and will cover the majority of the use-cases.
* The `GenericDataProcessorPresenter` will take behaviours as arguments.

**Key Principles**
* All behaviours are injectable. Each behaviour is defined as a new axis for change. No template methods.
* The `DataProcessorPresenter` interacts with the view via the `DataProcessorAlgorithmView` never the concrete subtypes of the view.
* Aside from the Visitor `accept` method on the view and `DataProcessorPresenter`, The `DataProcessorPresenter` takes all other arguments constructor arguments. This is particularly true of the behaviours.
* Where a behaviour cannot have a sensible defualt. A `NullObject` implementation must be created.
* Each `DataProcessorAlgorithmView` may only notifiy the `DataProcessorPresenter` about a change via a `notify(Flag)`. Otherwise it does not interact with any other aspect of the framework.

**Desired Principles**
* The first implementation of the framework should set to replace/refactor the ReflMainViewPresenter and related views. This would be the fastest way to prove the framework.
* Concrete views should be implemented at the last possible moment in the development lifecycle. Early creation of the views will tend to act as a inferior proxy for proper unit testing.

###Low Level Design (subject to change)###
**Presenter Inputs**

| Input        | Type | Mandatory  | Notes |      
| ------------- |:-------------:|-------------:|-------------:|
| DataProcessorAlgorithm | string | yes | |
| WhiteList | map<string, string> | yes | Defines table columns. key is algorithm property name, value is column name in table | 
| BlackList | vector<string> | no | Properties blacklisted from Options Column |
| PreProcess* | PreProcessStep** | NullObject | |
| PostProcess* | PostProcessStep** | NullObject | |

*This is a behaviour
**An abstract type with a concrete implementation done as Type2Type for type safety.


**Example: Simple Use Case In Python - Defaults for All**
```python
# Minimal use case.
presenter = GenericDataProcessorPresenter(data_processor_algorithm='ReflectometryReductionOne', property_white_list=['InputWorkspace', 'InputTheta'])
self.layout().addWidget(DataProcessorAlgorithmWidget(presenter));
# Table with 4-columns and the standard editing features added. Group and Options are added to the above. All other properties can be modified via the OptionsColumn.
```

**Example: Complex Use Case In Python - Lots of Customization**
```python

pre_process = {'algorithm':'LoadAndAdd', 'column_name':'Runs(s)', 'direct_output_to':'InputWorkspace'}
post_process_groups{'algorithm':'Stitch1D', 'directed_input_from':'OutputWorkspaces'} # This is what I'm going to do with thing's I have grouped.
white_list = {'Angle':'InputTheta', 'WavMin':'WavelengthMinimum'} # I don't want to call my columns the same thing as my property names.
black_list = ['OutputWorkspaceWavelength'] # Things I never want to specify


presenter = GenericDataProcessorPresenter(data_processor_algorithm='ReflectometryReductionOne', property_white_list=white_list, pre_process_step=pre_process, post_process_step=post_process, property_black_list=black_list)
self.layout().addWidget(DataProcessorAlgorithmWidget(presenter));
# Table with 3-columns and the standard editing features added. All other properties can be modified via the OptionsColumn.
```

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

