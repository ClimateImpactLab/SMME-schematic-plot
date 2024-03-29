# SMME-schematic-plot
This repository provide code for generating figures to compose the SMME schematic plot (Fig. 1B in mortality paper):

1. plot_GMT_pdf.py is the python code for generating PDF of global mean surface temperature anomaly.

2. plot_tas_aggregation_annual_GCP.py is the python code for generating world maps of surface temperature anomaly in impact regions.

3. figures: a folder stores figures produced by the code 1 and 2. Limited by the space of the repository, the figures used to produce the schematic plot are stored on Zenodo (http://doi.org/10.5281/zenodo.3595174). Users can download the figures from the Zenodo and save them in the folder.

4. shapefile: this folder stores the shape file for impact regions

Finally, the schematic plot is generated by manually putting the tas maps in lines based on the GMT of the corresponding model and superimposing on the GMT PDF plot as follows:

According to the PDF of GMT, 7 bins (with bin edges 1.5, 2.5, 3.5, 4.5, 5.5, 6..5, 7.5,8.5) are used. The GCMs and surrogates are arranged in these GMT bins based on the averaged GMT values over the period 2080-2099 in RCP8.5. The averaged GMT values of the 33 models are listed in the excel file "GMST_2080-2099mean_SMMEmodels.xlsx". For a particular bins, the tas maps of selected models are sorted from cool to warm by eyeballing. 
