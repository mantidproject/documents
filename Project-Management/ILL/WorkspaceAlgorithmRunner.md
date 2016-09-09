# Managing data reductions with `WorkflowAlgorithmRunner`

When reducing the raw data of a complete neutron experiment, it is typical that dependencies occur between the datasets. For example, for vanadium normalization, the vanadium run has to be processed before the samples, and if an empty vanadium run exists, it has to be processed before the vanadium. Trying to incorporate such dependency resolution to the workflow algorithm tends to make the algorithm unnecessarily complex. One solution is to keep the workflow algorithm as simple as possible and outsource the dependency resolution to a 'master' or 'manager' algorithm. This algorithm is called `WorkflowAlgorithmRunner`. For `WorkflowAlgorithmRunner`, one specifies all the datasets to be processed and how they depend on each other. The algorithm then declares the order of processing and controls the information flow between the reductions. 

`WorkflowAlgorithmRunner` has three input properties: the name of the algorithm to run, a `SetupTable`, and an `InputOutputMap` table. `SetupTable` specifies each run of the managed algorithm and which values the input and output properties should have. `InputOutputMap` in turn contains information about how certain input properties depend on outputs of other runs. With its help, `WorkflowAlgorithmRunner` can decide which runs should be processed first and how to connect the inputs and outputs.

## Usage example

As an example, lets say we have an algorithm which has a single input property, `InputWorkspace`, and a single output property, `OutputWorkspace`. There are three datasets, **a**, **b**, and **c**, with the `InputWorkspace`s of **a** and **b** depending on the `OutpuWorkspace` of **c**. Thus, the `InputOutputMap` connects the `OutputWorkspace` property to the `InputWorkspace` property and the `SetupTable` looks like the following:

`Id`   | `InputWorkspace` | `OutputWorkspace`
-------|------------------|------------------
**a**  | **c**            |
**b**  | **c**            |
**c**  |                  | *c_out*

In the above, each row corresponds to a single call to the managed algorithm. The mandatory `Id` column specifies a unique identifier for each row while the `InputWorkspace` and `OutputWorkspace` columns represent the corresponding properties of the algorithm. When `WorkflowAlgorithmRunner` inspects the `SetupTable`, it encounters the **c** token in the `InputWorkspace` column on the **a** row. The mapping between the `InputWorkspace` and `OutputWorkspace` properties then prompts `WorkflowAlgorithmRunner` to look for the name of the output workspace of the **c** dataset in the `OutputWorkspace` column. `WorkflowAlgorithmRunner` also notices that **c** should be run before **a**. The same procedure repeats for the **b** row. Finally, the **c** row is inspected. It does not have an `InputWorkspace` and is already scheduled to run before both **a** and **b**.

Thus, to process the datasets specified above, `WorkflowAlgorithmRunner` would first make a call
```python
Algorithm(InputWorkspace='', OutputWorkspace='c_out')
```

followed by calls

```python
Algorithm(InputWorkspace='c_out', OutputWorkspace='')
Algorithm(InputWorkspace='c_out', OutputWorkspace='')
```

for the **a** and **b** datasets.

The `OutputWorkspace` properties in the above are empty strings for the **a** and **b** runs not only because the corresponding cells in the `SetupTable` are empty. `WorkflowAlgorithmRunner` automatically sets output properties to empty strings if they are not needed by any inputs. This is done to allow the algorithm to avoid perhaps unnecessary processing steps. To force output, the workspace names can be quoted:

`Id`   | `InputWorkspace` | `OutputWorkspace`
-------|------------------|------------------
**a**  | **c**            | 'a_out'
**b**  | **c**            | "b_out"
**c**  |                  | *c_out*

Additionally, quotes in the input columns are treated as 'hard workspace names', and no input-output resolution is done to them. Therefore, `SetupTable`

`Id`   | `InputWorkspace` | `OutputWorkspace`
-------|------------------|------------------
**a**  | **c**            | 'a_out'
**b**  | **c**            | "b_out"
**c**  | 'base'           | *c_out*

would result in calls (the last two call can be in any order)

```python
Algorithm(InputWorkspace='base', OutputWorkspace='c_out')
Algorithm(InputWorkspace='c_out', OutputWorkspace='a_out')
Algorithm(InputWorkspace='c_out', OutputWorkspace='b_out')
```

Values in the columns of `SetupTable` not mentioned in `InputOutputMap` are transferred to the managed algorithm as-is. So

`Id`   | `InputWorkspace` | `Param` | `OutputWorkspace`
-------|------------------|---------|------------------
**a**  | **c**            | 1       | 'a_out'
**b**  | **c**            | 3       | "b_out"
**c**  | 'base'           | 2       | *c_out*

would result in

```python
Algorithm(InputWorkspace='base', Param=2, OutputWorkspace='c_out')
Algorithm(InputWorkspace='c_out', Param=1, OutputWorkspace='a_out')
Algorithm(InputWorkspace='c_out', Param=3, OutputWorkspace='b_out')
```

## Planned use of `WorkflowAlgorithmRunner`

In conjunction with a well designed workflow algorithm, `WorkflowAlgorithmRunner` could make a powerful tool for data reduction, even for large datasets with complex dependencies. As `WorkflowAlgorithmRunner` takes care of dependency resolution and overall data flow management, the workflow algorithms can be kept relatively simple and understandable, and thus accessible for modification and extension. Usually, we expect `WorkflowAlgorithmRunner` to be used through some graphical user interface. However, wrapper algorithms specific for each workflow algorithm are planned to supply the `InputOutputMap`s which should ease the usage of `WorkflowAlgorithmRunner` if a user wants to call it manually. For simple reductions, a user can call the workflow algorithms directly, as well.
