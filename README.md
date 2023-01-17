# aigeanpy-Working-Group-15

Overview
********

The Aigean satallite is an Earth observation satallite used to monitor the region around Lough Ree.

There are 4 primary instruments onboard the Aigean satellite:

*  Lir imager: Has the largest field-of-view (FOV) of the three imagers, but the smallest resolution (20 m per pixel).

*  Manannan imager: Intermediate FOV with an imporved resolution (10 m per pixel).

*  Fand imager: Smallest FOV of the three imagers, but high provides a high resolution (1 m per pixel).

*  Ecne radar: Provides three measurements (turbulence, salinity and algal density) for the 300 deepest areas of the region. 

Aigeanpy is a Python library that allows the user to query, download, open, process and visualise Aigean satellite data from 
the Irish Space Agency webservice archive (https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/).

Installation Guide
==================

Aigeanpy is written in Python and supports python version 3.9. This section provides a brief overview on how to install the Aigeanpy library.

1. Download Aigeanpy from the Github repository (https://github.com/UCL-COMP0233-22-23/aigeanpy-Working-Group-15)

2. Unzip the package

3. Navigate to the directory containing the Aigeanpy package and run:
  
   pip install .
   
Tutorials
=========

How to query images for a particular date:
******************************************

The query_isa function passes in three parameters. The first, start_date, representing from what date you want to get isa-archive results.
The second, stop_date, represents the final date you want to recieve isa-archive results. 
The final parameter, instrument, specifies which instrument you want to query the isa-archive by.
All three parameters are optional but they must be a string type.

Both the start_date and the stop_date must be in a YYYY-MM-DD format.
The stop_date must be after the start_date and no more than three days later.

An example query_isa use case would be the following:

    query_isa("2023-01-16", "2023-01-19", "Lir")

This query will retrieve all Lir imagery data from the isa-archive between the dates of the 16th of January 2023 and 19th of January 2023.

How to download images for a particular date:
*********************************************

The download_isa function takes in two parameters.
The first, file_name, is required and must be a string. 
This parameter specifies the name of the file to be downloaded from the ISA and will also represent the filename of the locally downloaded file. 
The second, save_dir, is an optional parameter (but must be a string) that specifies which directory the file should be saved in. 

An example download_isa use case would be the following:

    download_isa("aigean_lir_20230104_145310.asdf", "C:/{foldertosaveto}/")

Where queriedfile represents the name of the file in the database, the instrumentext represents the instrument type to be parsed (asdf, hdf5, zip),
and the foldertosaveto represents the path to the locally saved file.

Developer Guide
===============

This page is a guide for those developers who want to contribute to the Aigeanpy library.

1.  Create a personal fork of the project from the Github repository (https://github.com/UCL-COMP0233-22-23/aigeanpy-Working-Group-15).

2.  Clone the fork onto your local machine.

    *   If your fork is out-dated pull the up-to-date version to your local repository:

            git pull

3.  Create a new branch and begin implementing your code following the PEP 8 style guide (https://peps.python.org/pep-0008/)

        git checkout -b <new-branch-name>
    
4.  Fully document your code using docstrings following the numpy format (https://numpydoc.readthedocs.io/en/latest/format.html).

5.  Move into the aigeanpy directory and run pytest in the terminal.

    .. code-block:: Python

        pytest

6.  Push your branch to your fork on Github. When creating commit messages please follow the style guide (https://medium.com/swlh/writing-better-commit-messages-9b0b6ff60c67).

7.  Create a new pull request targeting the master branch of the aigeanpy library.

    *   Please link issues, use relevant tags and use an appropriate title that summarises your changes concisely.
