############################################################
# this program plots the PDF of the global mean temperature
############################################################
from netCDF4 import Dataset, date2index
import numpy as np
import netCDF4 as nc
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm,gaussian_kde

# read gmt from SCM
file = '../MAGICC_CMIP/IPCCAR5climsens_rcp85_DAT_SURFACE_TEMP_BO_15Nov2013_185227.OUT'
data = np.loadtxt(file, skiprows=24)
year0 = data[:,0]
gmt = data[(year0>=2080)&(year0<=2099),1:]
gmt_ref = data[(year0>=1986)&(year0<=2005),1:]
gmt_refm = np.mean(gmt_ref,0).reshape(1,600)
gmt_m = np.tile(gmt_refm,(20,1))
gmt_scm = gmt-gmt_m
gmtm = np.mean(gmt_scm,0)

# plot probability density function
pdf = norm.pdf(gmtm)
kde = gaussian_kde(gmtm,bw_method=0.45)
t_range = np.linspace(0,10,101)
fig = plt.figure(figsize=[8, 7])
plt.plot(t_range,kde(t_range), linewidth=3, color='steelblue')
plt.ylabel('Probability Density',fontsize=15)
plt.xlabel('2080-2099 Global Mean Temperature Anomaly ($^\circ$C)',fontsize=15)
plt.ylim(0, 0.45)
plt.xlim(0,10)
fig_name = 'figures/PDF_golobal_mean_temp_2080-2099.pdf'
fig.savefig(fig_name, dpi=300)
plt.close(fig)
