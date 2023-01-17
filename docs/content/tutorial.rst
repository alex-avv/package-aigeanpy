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

.. code-block:: Python

    query_isa("2023-01-13", "2023-01-15", "Lir")

This query will retrieve all Lir imagery data from the isa-archive between the dates of the 13th of January 2023 and 15th of January 2023.

How to download images for a particular date:
*********************************************

The download_isa function takes in two parameters.
The first, file_name, is required and must be a string. 
This parameter specifies the name of the file to be downloaded from the ISA and will also represent the filename of the locally downloaded file. 
The second, save_dir, is an optional parameter (but must be a string) that specifies which directory the file should be saved in. 

An example download_isa use case would be the following:

.. code-block:: Python

    download_isa("aigean_lir_20230104_145310.asdf", "C:/{foldertosaveto}/")

Metadata update when combining images:
**************************************
When you add or substract two images, 'archive', 'instrument', 'observatory', 'resolution', and 'obs_time' in meta will only hold the value of the first satmap. Just the 'xcoords' and 'ycoords' are updated.

When using the mosaic method to add two images, 'archive', 'instrument', 'observatory', and 'obs_time' will only hold the value in the first satmap. Just the 'Resolution', 'xcoords' and 'ycoords' are updated. 
If creating the mosaic with padding = False, it will return the data cover maximum portion without blanks on the image.
