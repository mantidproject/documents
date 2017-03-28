# Custom URL for algorithm not part of the regular mantid distribution

The help button in the algorithm dialog is useless for python algorithms registered at runtime, this is really frustrating when the user clicks for help.

The help button ends up invoking `MantidHelpWindow::showAlgorithm(const string &name, const int version)` wherein a local URL address is constructed.
One way to rescue the functionality of the help button is to implement a method `const string IAlgorihtm.helpUrl()`, and in `MantidHelpWindow::showAlgorithm`
check for the return of this function. If not empty, then use it in place of the local URL.

The overhead of this method is that one unmanaged algorithm has to be instantiated in order to execute the method. Maybe there's a more efficient way.
