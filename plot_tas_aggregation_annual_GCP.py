# this scripte aggregates the surrogate models and anomalies of tas over the world in impact regions with population weighting

import os
import csv
import sys
import numpy as np
import xarray as xr
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from scipy.interpolate import griddata
from scipy.ndimage import label
import pandas as pd


# read shapefile
print('reading shapefile ...')
fs = 'agglomerated-world-new'
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,\
            llcrnrlon=-180, urcrnrlon=180, resolution=None)
m.readshapefile(fs, 'shapes', drawbounds=False)
n_shp = len(m.shapes)
n_rgn = m.shapes_info[-1]['SHAPENUM']

var_name = 'tas'
var_units = 'Degree Celsius'
scenario = ['rcp85']
years = range(2080,2099)
years_hist = range(1986,2005)
ensemble = 'r1i1p1'
# set model
model = sys.argv[1]

# absolute path for large-size files for population-weighted aggregation
Dir='/global/scratch/groups/co_laika/gcp/climate/nasa_bcsd/hierid/popwt/daily/tas/rcp85'
Dirh='/global/scratch/groups/co_laika/gcp/climate/nasa_bcsd/hierid/popwt/daily/tas/historical'

print(model)
tas_list = []
tash_list = []
if model[:9] == 'surrogate':
    fn = '1.7.nc4'
else:
    fn = '1.6.nc4'
# compute baseline
for yr_h in years_hist:
    if (model[:9] == 'surrogate'):
        model_h = model[10:-3]
    else:
        model_h = model
    f_h = '{:}/{:}/{:}/1.6.nc4'.format(Dirh, model_h,yr_h)
    ds_h = xr.open_dataset(f_h)
    var_h = ds_h.tas.mean(dim='time')
    tash_list.append(var_h)
tash = xr.concat(tash_list, dim=pd.Index(years_hist, name='years'))
tas_bl = tash.mean(dim='years')
for yr in years:
    f = '{:}/{:}/{:}/{:}'.format(Dir, model,yr,fn)
    ds = xr.open_dataset(f)
    var = ds.tas.mean(dim='time')
    tas_anom = var-tas_bl
    tas_list.append(tas_anom)
tas = xr.concat(tas_list, dim=pd.Index(years, name='years'))
tasm = tas.mean(dim='years')

# ------ plot ------
# create polygon collection
print('creating polygon collection ...')
poly = []
color = np.zeros(n_shp)
for ii in range(n_shp):
    jj = m.shapes_info[ii]['hierid']
    color[ii] = tasm.sel(hierid=jj).values
    poly.append(Polygon(m.shapes[ii], closed=False))

# make a plot
fig = plt.figure(figsize=(5, 4))
ax = plt.subplot(111)
c = PatchCollection(poly, array=color, cmap=mpl.cm.Spectral_r,edgecolors='none')
c.set_clim([0, 10])     # set the range of colorbar here
ax.add_collection(c)
ax.set_xlim([-180, 180])
ax.set_ylim([-60, 90])
if model[:9] !='surrogate':
    mm = Basemap(llcrnrlon=-180,llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,projection='cyl')
    mm.drawcoastlines(linewidth=2, color='steelblue',zorder=0)
plt.axis('off')
plt.colorbar(c,orientation="horizontal")
f_p = 'figures/{:}_GCP_aggregated_rcp85_{:}_2080-2099.png'.format(var_name, model)
fig.savefig(f_p, dpi=300)
plt.close(fig)


