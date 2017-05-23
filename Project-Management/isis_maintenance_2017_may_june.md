# Pair Programming during the maintenance period @ISIS

## Pair programming

See [here](https://en.wikipedia.org/wiki/Pair_programming) and [here](https://blogs.sourceallies.com/2011/03/pair-programming-101/) for an overview of pair programming.

#### Expeted benefits

* Increased quality of code and design (instant 4-eye review)
* Can be nicer to work with other people
* Knowledge sharing
* Enhanced communication (even after the maintenance phase)

#### Risks

 * Decrease productivity (items/hour) in the short term (which may be offset by fewer support hours, ie time spent on bug fixes).
 * One person does all the work
 * Can be exhauting
 
## Pair Programming during the maintenance phase

As a trial we would like to pair two developers to a small team to tackle the maintenance tasks. Some points are:

* This is an experiment. If you feel it is not for you for any reason, then let us know and we will rearrange the setup.
* Every developer should spend the same amount of time on the keyboard. So swap maybe every 30 minutes or less.
* One of the main benefits of pair programming is a constant discussion about the code and issue you are working on. If the two of you are silent for too long, take it as a sign that something is not quite right.
* Traditionally you have a driver (who codes) and a navigator (who keeps track of the issue and stirs development), this might be a good pattern to follow since it ensures that everyone is engaged.

* Any maintenance issue is suitable for pair programming, but we should start with the investigation of the failing unit tests on the build servers.

### Paring people

The initial pairs are chosen via the script below. 

TODO: Modify script to have only one group of people

import numpy as np
import pprint as pp


def get_random_index(high_value):
    return int(np.random.uniform(low=0, high=high_value, size=None))


def pair_people(group):
    pairs = {}
    unpaired = None
    number_of_groups = len(group)/2

    for index in range(number_of_groups):
        person1_index = get_random_index(len(group))
        person1 = group.pop(person1_index)

        person2_index = get_random_index(len(group))
        person2 = group.pop(person2_index)
        pairs.update({person1: person2})
    return pairs, group


def generate_pairs(group):
    pairs, unpaired = pair_people(group)
    print("+++++++++++++++++++++++++++++++")
    print("Groups")
    print("+++++++++++++++++++++++++++++++")
    pp.pprint(pairs)
    if unpaired:
        print("The unpaired is {}.".format(unpaired))
    else:
        print("Everyone has been paired.")
    print('\n\n')


group_people = ["P1", "P2", "P3", "P4"]
generate_pairs(group_people)


group_people = ["P1", "P2", "P3", "P4", "P5"]
generate_pairs(group_people)

```

The idea is to have new teams every two days.

## Task list

During the retrospecitve of the last release a lot of developers mentioned that the false-positives on the build serves are a major impediment to our productivity. There is a reocurring set of tests which tend to be producing false-positives. We would like to fix these tests if possible.

During the last months/weeks everyone has been collecting data which can be found [here](https://docs.google.com/spreadsheets/d/1qs81x3ZDDxvEu3H5Zg1KN8Qfu54dIVWKI2f3-zxFaFg/edit#gid=1630384006)

The first set of tests we want to tackle are:

* APITest.AsynchronousTest.testCancelGroupWS	
* SliceViewerMantidPlotTest_SliceViewerPythonInterfaceTest	
* MantidPlotProjectSerialiseTest.test_project_file_with_plotted_spectrum	
* CustomInterfacesTest.ALCDataLoadingPresenterTest.test_customGrouping	
* PlotAsymmetryByLogValueTest.test_skip_missing_file	
* CrystalTest.OptimizeCrystalPlacementTest.test_tilt	

The available developers are:

* Martyn
* Anton
* Pranav
* David
* Louise
* Anthony
* Nick
* Owen
* Lamar
* Dimitar

* Roman (some time)
* Anders (some time)
* Gemma (some time)

### How to approach failing tests?

Some methods are:
* Check if unit test generates a file. Check if another test uses and deletes a file with the same name.
* Run all tests in Windows debug mode.
* Try setting `OMP_NUM_THREADS` to a value above the number of cores you have to stress the test.
