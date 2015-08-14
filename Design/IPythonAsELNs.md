# Feasibility study of using IPython notebooks as electronic laboratory notebooks (ELNs)

The purpose of this document is to investigate the use of IPython notebooks as
electronic laboratory notebooks (ELNs) in Mantid.

This document address github issue [#10085] (https://github.com/mantidproject/mantid/issues/10085).

## Overview

Currently (v3.4), the Mantid Framework works well inside of IPython Notebooks.
All the features provided by the Python bindings function correctly, with the
obvious exception of the MantidPlot integration.

Example IPython Notebooks demonstrating the use of Mantid are available from the
[Mantid Download Page](http://download.mantidproject.org/). These use Mantid to
load and process data, and matplotlib to embed graphs of the data into the
IPython Notebook.

## Questions

1. Given a collection of ELNs, are/can they be searchable?
2. Can graphs be interactive, zoomable?
3. Can we get input to the notebook from instrument control, etc?

### 1. Searching Notebooks

IPython notebooks are plain-text JSON files. Filesystem tags are not very portable,
so the obvious solution would be putting keyword tags in a metadata JSON entry
in each notebook. Some kind of autocompletion of tags to avoid use of subtly
different keywords would need to be implemented.

The [IPython documentation] (https://ipython.org/ipython-doc/dev/notebook/nbformat.html)
gives advice on adding custom metadata to the notebook.

### 2. Interactive Graphs

Graphs can be made interactive by using the "nbagg" matplotlib backend. The 
example notebook on the [Using Ipython Notebook] (http://www.mantidproject.org/Using_IPython_Notebook)
Mantid web page can be changed to display plots with zoom and pan tools by replacing the 
line
```
%matplotlin inline
```
with
```
%matplotlib nbagg
```

Further interactive features, for example plotting different data by dragging a slider, 
can be provided by ipython widgets. The nbagg backend and ipython widgets require no 
changes to Mantid's current python environment.

If users require more powerful features, other options that are currently available are:
-[Plotly] (https://plot.ly/),
-[Bokeh] (http://bokeh.pydata.org/) and
-[mpld3] (http://mpld3.github.io/).

Plotly is very powerful and pretty, but has commercial licensing.

Bokeh is more powerful than mpld3 but also heavier and requires some learning
on the part of the user. It is in active development.

mpld3 has the advantages of being lightweight and that the user requires little
knowledge beyond matplotlib. By default, plots can be zoomed and panned. Many more
tools are available and are extensible via [plugins] (https://mpld3.github.io/notebooks/custom_plugins.html). 
Unfortunately the mpld3 project no longer seems to be in active development.

### 3. Input from Instrument Control

IPython notebooks are plain-text JSON files, it is therefore relatively
straightforward for other software to edit or create them. For example, instrument
control software could create a new notebook at the time of running an experiment and
insert paths to data files, experimental parameters and the time and date of executing the
experiment as metadata.

Since notebooks may contain executable code, the security implications
of write access to the notebook file from other software or even across a
network should be considered. IPython has a trust-based security system which
aims to ensure that "no code should execute just because a user has opened a notebook
that they did not write. Like any other program, once a user decides to execute
code in a notebook, it is considered trusted, and should be allowed to do anything.".
Further details are available in the [IPython documentation] (https://ipython.org/ipython-doc/3/notebook/security.html).
