Tab Reference energy system
---------------------------
For the description of the reference energy system tabs first the standard
example of a business park and neighbouring ciy will be used. In the end of
this page a small guide for filling out this tab from scratch will be given.

To get an overview of a reference energy system tab the following picture shows
a full zoom on the entire tab for the business park in the standard example.

.. image:: img_gui_tutorial/RES.png
    :width: 100%
    :align: center

The tab is structured into a header line and the main field where the RES is
represented. In the header line new entities to be added can be chosen. A more
detailed description of this will be given after the extensive discussion of
the model entities themselves.

Reference energy system
^^^^^^^^^^^^^^^^^^^^^^^
The reference energy system consist of three main types of model entities:

* **Commodities** respresenting the different energy carriers are represented
  by vertical lines (buses)
* **Processes** respresenting energy conversion units are represented by
  rectangles. The commodities connected to the conversion processes are
  indicated by arrows
* **Storages** representing commodity storage possiblities are represented by
  rectangles with rounded edges

For each of these three types of model entities there exist several subtypes
which require different parameters to be set by the user.

Commodities
~~~~~~~~~~~
Commidities are typically, but not exclusively, energy carriers. They are
represented by vertical lines in the RES. There aer 7 different commodity types
which play different roles within the energy system model and require different
inputs.

**Intermittend supply commodities** (SupIm) are not directly energy carriers.
They force all processes that interact with them to operate with a percentage
of their total capacity specified by a time series associated with the SupIm
commodity. A typical example for SupIm commodities is the capacity factor of
renewable energy generation units. The paramter input window that opens when
double clicking on the name or line of an existing SupIm commodity or the
clicking leftmost symbol in the RES header for a new SupIm commodity looks like
this:

.. image:: img_gui_tutorial/RES_Com_SupIm.png
    :width: 100%
    :align: center

The window denoted 'Time series' on the right hand side opens when double
clicking on the three dots next to a modeled year in the the lower part of the
main window denoted 'Commodity data'. Here you can paste the capacity factor
time series data from a spreadsheet for each modeled year individually. You
then have to close the subwindow by clicking the 'Ok' button to confirm the
values set. In the main window you can set the display color on the upper right
hand side by clicking on the button. The checkboxes in the columns 'Plot' and
'Report' specify if the commodity will be plotted in the standard output graphs
and reported in the output excel spredsheet. In the standard example the
commodity 'Solar (West/East)' is of type SupIm and represents the capacity
factors for solar photovoltaic units with an alternating west/east inclination
of 10°. 

**Buy commodities** can be bought by an external market at a user defined
price. This price can vary with time and correspondingly price time series have
to be specified. The paramter input window that opens when double clicking on
the name or line of an existing buy commodity or clicking the second symbol on
the left in the RES header for a new buy commodity looks like this:

.. image:: img_gui_tutorial/RES_Com_Buy.png
    :width: 90%
    :align: center

The window denoted 'Time series' on the right hand side opens when clicking on
the three dots next to a modeled year in the the lower part of the main window
denoted 'Commodity data'. Here you can paste the price time series data from a
spreadsheet for each modeled year individually. You then have to close the
subwindow by clicking the 'Ok' button to confirm the values set. In the main
window you can set the display color on the upper right hand side by clicking
on the button. There are three further paramters to be set in the main window.
In the column labeled 'Price factor' (Default 1) you can set a constant
multiplier for the price time series. This paramter simplifies scenario
definitions for price variations but is typically set to 1. The columns
'Maximum commodity use' and 'Maximum commodity use per step' restrict the total
annual and hourly amount of the commodity the system is allowed to use,
respectively. The checkboxes in the columns 'Plot' and 'Report' specify if the
commodity will be plotted in the standard output graphs and reported in the
output excel spredsheet. In the standard example the only buy commodity is
called 'Grid electricity' and represents the possibility to buy electricity
from the higher level grid.

**SupIm** and **Buy** commodities are grouped in the leftmost part of the RES
since they are typically inputs of processes rather then outputs. They are
separated by a vertical dashed line from the other commodities.

**Stock commodities** can also be bought at an external market albeit at a
fixed price as opposed to buy commodities. The paramter input window that opens
when double clicking on the name or line of an existing Stock commodity or the
clicking leftmost symbol in the RES header for a new Stock commodity looks like
this:

.. image:: img_gui_tutorial/RES_Com_Stock.png
    :width: 90%
    :align: center

You can set the display color on the upper right hand side by clicking on the
button. There are three paramters to be set for Stock commodities. In the
column labeled 'Commodity price (€/MWh)' you can set a constant price at which
the stock commodity can be bought from an external source. The columns
'Maximum commodity use' and 'Maximum commodity use per step' restrict the total
annual and hourly amount of the commodity the system is allowed to use,
respectively. The checkboxes in the columns 'Plot' and 'Report' specify if the
commodity will be plotted in the standard output graphs and reported in the
output excel spredsheet. Stock commodities can also be used to specify
intermediate helper commodities that expand the modeling possibilities
strongly. Since these cannot be bought externally the corresponding values
restricting the commodity buy capacity from an external market per year and per
hour are set to zero in this case. Next to the commodity 'Gas', which can be
bought externally for a given price, the commodities 'Intermediate' and
'Intermediate low temperature' are Stock commodities. The latter two serve to
make the model behavior more realistic. The commodity 'Intermediate'
tracks the operational state of a combined heat and power plant (CHP). This
then allows for a realistic linear operation of the power plant between
electricity and heat driven modes. This will be explained in more detail in the
Process section. The commodity 'Intermediate low temperature' has the sole
purpose of preventing the process 'Ambient air cooling' from loading the
cooling storage which would be unrealistic.

**Stock commodities** are located in the middle part of the RES since they can
be both, process inputs and outputs. They are spearated with dashed lines
against the other commodity types. 