Python algorithms for processing MDEventWorkspaces
==================================================

1. Motivation
+++++++++++++

Labeling neutron scattering events (or groups of neutrons) with
several parameters (such as Q components, energy trasfer, temperature, etc)
are the closest thing to physical models that we can provide in Mantid.
Scientists would likely express most of their problems in terms of such
multi-dimensional coordinates, rather than time of flight and detector coordinates.
For quick prototyping and for bespoke algorithms and data analysis scripts,
we should provide a simple and intuitive Python api for MD events, and MDEventWorkspaces.
While the rest of the document exemplifies this using reactor based experiments,
this is a more general and urgent problem.

A majority of the new instruments at reactor sources do not have
the time-of flight structure of the data that instruments at
spallation sources have. Trying to use matrix workspaces (either 
workspace2D or event workspaces) to store the raw data will cause
confusion and complications down the line. Here are some examples:

 - Suppose that data is stored in a matrix workspace, one event or 
   one bin corresponding to each scan point, with the X coordinate 
   given by the scan index. It is possible to add two workspaces together
   using Plus algorithm for two scans with the same length. If two points
   corresponding to the same X coordinate have been measured at different 
   conditions (say different detector orientation), the sum might not have
   a physical meaning. 
 
 - Assume a multi detector diffractometer, where the detectors can move
   during the scan (HB2A at HFIR). At some point in the processing,
   data will be stored in a matrix workspace with all detectors in one 
   spectra, and the X coordinate being the theta angle of the particular
   detector. It is likely that the best option would be to store it as 
   events, as to be able to add contributions from detectors at same or close
   scattering angles. The correlation between each event and the scan 
   configuration is then lost (which event originated in which detector).
 
 - For triple axis one would need to store more than one coordinate.
   It is possible to store each scan point as an event, with a corresponding
   "wallclock time", and all coordinates to be stored in the run object as time 
   series properties. The regular algorithms, such as Plus would be confusing,
   since the coordinate that we are interested is not the X axis, but a 
   log value.
   
 
2. Advantages of storing as MD events
+++++++++++++++++++++++++++++++++++++

A possible solution would be to store each scan point as an MD event with
several coordinated (such ad scattering angle or H, K, L, E),
the detector information, and a corresponding experiment info. Each scan point
will have a different ExperimentInfo that stores any additional parametrers,
such as temperature. It is possible in this way to either display the
MDevents as a function of one of the coordinates (plot a scan as a 
function of theta for diffraction, where all the detectors are shown). It is,
in principle possible to write an algorithm to sort through these MDevents, 
and group by detector number. One can then generate an instrument view.
PlusMD should just append data points and experimentInfos from multiple 
scans. Changing the step size of a plot, with overlapping contributions from
different detectors is done using BinMD. 

Neutron experiments at reactor source can be seen as a collection of measurment points.
Each measurement point contains the counts of all detectors for a certain amount of time
and the corresponding sample environemnt logs' value.  
The index of such measuring point can be mapped to the class variable 'run' of an MDEvent.  
By using 'run', an equivalence of event filtering operation can be applied to MDWorkspace. 

3. Unsolved problems
++++++++++++++++++++

In either case (matrix workspace or MDEvent workspace) new algorithms need 
to be written. All exsting algorithms need to be checked if they work with
reactor based instruments. It would help if some of the workload can be 
done by software scientists at ILL/Ulich or even instrument scientists
at the reactor sources.

The most basic algorithm would be a ConvertUnits equivalent. 
This would be easy to do as a python algorithm for a matrix
workspace, with a correct storage solution, but such a storage solution
would run into the problems exposed in the motivation section.
For MDEvent workspace choice, writing python algorithms is virtually
impossible at the moment, since accessing MDEvents or their coordinates 
is not exposed to python. In fact, what is somehow confusing even in C++
is that we don't have a way to loop over all MDEvents, but instead we loop
over the MDBox structure first.

4. Possible solution
++++++++++++++++++++

I propose that we develop a simple python interface to MDEvent workspaces
and MDAlgorithms that would enable people with less programming skills 
to develop/prototype algorithms and reduction/analysis procedures. 
Here are some of the requirements:

 a. It should expose MDEvents from a workspace directly, as a python list.
    One needs to somehow check if we can safely do this in memory (people
    should not attempt to run a for loop over all the events in a 24 hour 
    white beam measurement on TOPAZ)
 
 b. Related to the previous point, dealing with the box structure should 
    be optional for the potential programmer. The new python MD algorithm
    class should have a method to quicly loop over the events and to 
    recalculate the box structure. Advanced users should have the option of 
    overloading this function, such as to improve speed
 
 c. Here is a snippet of what I would like to do to change 
    from theta to d-spacing:
 
 .. code::
 
    import numpy as np
    data,norm=Load("HB2A_run_number.dat")
    #data,norm are MDEvent workspaces. The MDevents in
    #data and norm have only one dimension "theta", and each
    #MDevent in data has a corresponding weight, at the same 
    #coordinate, in norm
    for event,monitor in zip(data.getEventList(),norm.getEventList()):
        theta=event.getCoordinate(0)
        wl=event.getCorrespondingEventInfo().run()['wavelenght'].value
        dpacing=wl/(2*np.sin(0.5*theta)  #2 d sin(th/2)= lam
        event.setCoordinate(0,dspacing)
        monitor.setCoordinate(0,dspacing)        

 Another example would be to calculate |Q| from a triple axis 
 experiment. This will go from 4 dimensions (H, K, L, E) to one.
 It should be forbidden to write inplace a workspace if one
 changes dimensionality.
 
 .. code::
    
    data,norm=Load("TipleAxisData_1234.dat")
    newWS=CreateMDEventWorkspace(data,dimensions=1)
    for event,newevent in zip(data.getEventList(),newWS.getEventList()):
        Q=event.getCorrespondingEventInfo().sample().getOrientedLattice().getUB()*
         V3D(event.getCoordinate(0),event.getCoordinate(1),event.getCoordinate(2))
        newevent.setCoordinate(0,Q.norm())

d. Usually the first step to load reactor-source experiment data is to create an MDWorkspace
   real space.  The number of MDEvents and their coordinates are determined by the 
   number of mearurement points and the position of the detectors at each measurement points.
   Thus it can be convenient to program in python script, if a set of APIs are defined and implemented 
   to (1) construct an MDWorkskpace by detectors positions and then 
   (2) modify the detectors' counts by index measurement point and detector ID. 
