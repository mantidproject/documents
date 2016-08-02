Release Planning for Mantid version 4.0
=======================================

Motivation
----------

We have a number of desired changes that will break backward compatibility for users scripts, and potentially ways of working with 
Mantid and Mantidplot.  While we can make these kind of changes in a planned way with carefull communication, we cannot follow that up
with other breaking changes soon afterwards.

In order to decide on the changes to make it into this major release, and to align them to deliver together we will document the planned changes
to include here.

List of breaking changes 
------------------------

1. Change from qwt5 graphs to ? [3 people 1-3m]]
1. Move to Python 3 on all platforms [1 person 2m]
1. Sanitise Algorithm and property names (including merging) [Plan - 1 person 2w, Impl 3 people 1-3m]
1. Removing InOut workspace usage [1 person 2w]
1. ?Moving the Python API from the SimpleAPI (the impacts of this need further consideration) [????????]

List of other changes
---------------------

These changes are not bound to be included in this release, but being significant changes it would be good to include them together if
the timing and resource allows.

1. Instrument 2.0 [2p 4m]
2. Upgrade to Qt5 [2p 2m]

The guestimates provided in [ ] are included at present only to propose a starting point for further conversation. 
