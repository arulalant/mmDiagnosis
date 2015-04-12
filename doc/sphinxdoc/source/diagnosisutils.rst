.. _diagnosisutils:


Documentation of **diagnosisutils** source code
***********************************************

The diagnosisutils package contains the `Data Access Utils`_, `Time Axis Utils`_, and `Plot Utils`_ modules.


Data Access Utils
=================

This data access utils uses the `Time Axis Utils`_ and `Days Utils`_ .

The `xml_data_access`_ module help us to access the all the grib files through single object.

Basically all the grib files are pointed into xml dom by cdscan command.

Then we can the xml files through uv-cdat.

Right now we are generating 8 xml files to access analysis grib files and 7 forecasts grib files.

In the `xml_data_access`_ module, we are finding which xml needs to access depends upon the user inputs (Type, hour) in the functions of this module.

And once one xml object has initiated then through out that program execute session, it will remains exists and use when ever user needs it.


.. _xml_data_access:

xml_data_access
---------------

.. automodule:: xml_data_access
   :members:
   


Time Axis Utils
===============

This `timeutils`_ module helps us to generate our own time axis, correct existing time axis bounds and generate bounds.

Here we used inbuilt methods of cdtime and cdutil module of uv-cdat.


timeutils
---------

.. automodule:: timeutils
   :members:
   


Plot Utils
==========

The `plot`_ module has the properties to plot the vcs vector with some default template look out.

User can control the reference point, scale of arrow marks of the vector plot.

plot
----

.. automodule:: plot
   :members:


More
====

More utilities will be added and optimized in near future.

