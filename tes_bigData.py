import bigData as data
import pytest
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr
import time as tm
import matplotlib.ticker as mticker
import concurrent.futures
import datetime
from matplotlib.widgets import Button
import os
from unittest import mock



rootgrp  = xr.open_dataset('bigData.nc') 
long = np.array(rootgrp.variables['lon'])
lat = np.array(rootgrp.variables['lat'])


models = [                                                                          #extract data from models: convertin models into numpy arrays
    np.array(rootgrp.variables['emep_ozone']),
    np.array(rootgrp.variables['chimere_ozone']),
    np.array(rootgrp.variables['ensemble_ozone']),              
    np.array(rootgrp.variables['eurad_ozone']),
    np.array(rootgrp.variables['lotoseuros_ozone']),
    np.array(rootgrp.variables['match_ozone']),
    np.array(rootgrp.variables['mocage_ozone']),
    np.array(rootgrp.variables['silam_ozone']),
]


@mock.patch("%s.data.plt" % __name__, side_effect=['viridis', 'yes'])
def test_module(mock_plt):

    data.make_graph(1)
    projection = ccrs.PlateCarree()
    ax1 = mock_plt.subplot()

    assert mock_plt.title.called
    assert mock_plt.figure.called
    assert mock_plt.subplot.called
    assert mock_plt.subplot.call_args_list[0][0][0] == 5
    assert mock_plt.subplot.call_args_list[0][0][1] == 2

    assert ax1.coastlines.called
    assert ax1.set_title.called

    assert mock_plt.contour.called
    assert (len(mock_plt.contour.call_args_list[0][0][0]) == len(long))
    assert (set(mock_plt.contour.call_args_list[0][0][0]) == set(long))
    
    assert (len(mock_plt.contour.call_args_list[0][0][1]) == len(lat))
    assert (set(mock_plt.contour.call_args_list[0][0][1]) == set(lat))
 
    
    assert mock_plt.suptitle.called
    assert ax1.inset_axes.call_args_list[0][0][0] == [-3.4, -1, 5, 0.3]
    assert mock_plt.savefig.called


# def test_open_file():
