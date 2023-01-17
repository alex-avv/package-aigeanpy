.. Aigeanpy documentation master file, created by
   sphinx-quickstart on Mon Jan 16 13:05:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Aigeanpy's documentation!
====================================

Overview
********

The Aigean satallite is an Earth observation satallite used to monitor the region around Lough Ree.

There are 4 primary instruments onboard the Aigean satellite:

*  Lir imager: Has the largest field-of-view (FOV) of the three imagers, but the smallest resolution (20 m per pixel).

*  Manannan imager: Intermediate FOV with an imporved resolution (10 m per pixel).

*  Fand imager: Smallest FOV of the three imagers, but high provides a high resolution (1 m per pixel).

*  Ecne radar: Provides three measurements (turbulence, salinity and algal density) for the 300 deepest areas of the region. 

Aigeanpy is a Python library that allows the user to query, download, open, process and visualise Aigean satellite data from 
the `Irish Space Agency webservice archive <https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/>`_. 



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   content/installation
   content/tutorial
   content/modules
   content/developer_guide
