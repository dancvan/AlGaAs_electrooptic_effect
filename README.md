#AlGaAs_electro-optic_effect
This repository is intended to hold all related notes/work related to the measurement of the electro-optic effects (both the pockels and the piezoelectric effects) at the SU gravitational wave physics lab

Navigating this repository:

<<<<<<< HEAD
code:
- notebooks -> a high number of jupyter notebooks primarily used for quick computations and plotting. For instance, one notebook in lab_tools called beam_scans provides an easy routine to do a least squares fit from an .xlsx file.  
- fea_electrodes -> directory contains all files related to the simulation of the electrode system to produce a reasonable electric field estimate within the AlGaAs coating (both disk and split electrode systems)
- py_packages -> contains consistently used computations and operations (for instance, importing a model dataset from ltspice or the calibration of the meaasured error signal voltage spectra within the PDH loop to a displacement spectra
- finesse -> currently not utilized very much but might possibly be updated with tabletop simulations

documents:
- contains various books, datasheets, internal notes, and related publications that I found relevant to the project
=======
code: 
- notebooks -> a high number of jupyter notebooks primarily used for quick computations and plotting. For instance, one notebook in lab_tools called beam_scans provides an easy routine to do a least squares fit from an .xlsx file.  
- fea_electrodes -> directory contains all files related to the simulation of the electrode system to produce a reasonable electric field estimate within the AlGaAs coating (both disk and split electrode systems)
- py_packages -> contains consistently used computations and operations (for instance, importing a model dataset from ltspice or the calibration of the meaasured error signal voltage spectra within the PDH loop to a displacement spectra
- finesse -> currently not utilized very much but might possibly be updated with tabletop simulations 

documents:
- contains various books, datasheets, internal notes, and related publications that I found relevant to the project

measurements: 
- all measured data. Categorized by measurement type and is stored within a directory that labels the date of the measurement taken. 

results:
- contains a lot of .h5 files that can be traced back reading through the code/py_packages/pockels_cal.py calibration package. It also contains figures depicting experimental concept sketches and .stl files as well as group meeting updates that organize the results into something a little more comprehensive.  
>>>>>>> e60011e48ce0b8cf5ad2c824ebe11d5f90db972d

measurements:
- all measured data. Categorized by measurement type and is stored within a directory that labels the date of the measurement taken.

results:
- contains a lot of .hdf5 files that can be traced back reading through the code/py_packages/pockels_cal.py calibration package. It also contains figures depicting experimental concept sketches and .stl files as well as group meeting updates that organize the results into something a little more comprehensive.  
