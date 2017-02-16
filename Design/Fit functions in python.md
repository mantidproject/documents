# Working with fit functions in python

Although fitting functions have some of the functionality exposed to python the use of it is very limited and functions are constructed via strings. Values of the optimised parameters get extracted from TableWorkspaces output from the Fit algorithm. Both function construction and extraction of the results are cumbersome and error prone. This document describes a design of a python fitting API aiming to overcome these problems. The main idea of the solution proposed here is to create and manipulate a C++ IFunction object from python directly.

