# Application design philosophy

This application is designed along the MVC (Model-View-Controller) philosophy, where data storage, user interface and data access control/logic
are separated with minimal interfaces. Since the data structure in this application is not too complex i decided to combine Model and Controller
to save multiple files and code lines. Further, this application contains a network modul and a file for utility functions like conversions and
formatting.

## Communication

Every board in this project sends a beacon each seconds to announce itself and its capabilities to any UI applications in the network. An exact
definition of this beacon and the information it provides can be found in `Headers.py`.  
Whenever an application picks up a board it offers the user to set a trigger on that board. Such a trigger specifies a voltage and channel next
to management data.  
Once a trigger is hit by the board it will transmit all available samples in fragments to the application for user inspection. Those fragments
are collected by the application and, if complete, presented to the user.

## Application

### Module `network`

Core of the network module is the `Headers.py` file. This file handles parsing from and to binary data and is the primary conversion utility for
any communication with the board. The code for the board contains a similar file and those files are required to match. To ensure that those
conversions are done without errors there is a test module separatetly from the application. The tests simply convert a set of data to binary and
back to check for unintended differences.  
`SampleGroup.py` and `SampleCollector.py` are classes to collect fragments of measurements to compile them into a complete set. The
`SampleCollector` class holds `SampleGroup` instances for every group of samples the network module encounters. The `SampleCollector` passes
fragments to the right `SampleGroup` and whenever a group is complete it commits the measurements into the `modelcontroller` for application
processing.  
`Network.py` is handles the UDP socket, receiption of board beacons, is the interface to set a trigger on the board and passes sample fragments
to the `SampleCollector`.

### Module `modelcontroller`

This module handles storage and events processing of beacons and complete measurement sets. Both event classes, `BoardEvents` and `PlotEvents`
accomplish this task in an identical manner. These classes are event busses where the listeners have to be derived from the event bus class.
When a child class (eg. `Network`) calls the super constructor of the event bus class it is registered and from that point on all event calls
by the event bus class will be forwarded to the child class (eg `network`).  
Because of this, any View component is only to react to highly refined and specific events (eg. this board was newly detected. Add it to
available boards).  
Timeouts are also handled here.

### Module `view`

In here the UI is handled in an object oriented way. Each UI component, like the Trigger Command Unit, is grouped in a file and finally all
parts are combined to a window in `MainWindow.py`
