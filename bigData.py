import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs


rootgrp = xr.open_dataset("bigData.nc")                                           #opening the .nc file

lat = np.array(rootgrp.variables['lat'])                                          #extract/copy the data of lat
long = np.array(rootgrp.variables['lon'])                                         #extract/copy the data of lon
hour = np.array(rootgrp.variables['hour'])                                        #extract/copy the data of time


models = [                                                                        #extract data from models: call each model models['emep_ozone']
    np.array(rootgrp.variables['emep_ozone']),
    np.array(rootgrp.variables['chimere_ozone']),
    np.array(rootgrp.variables['ensemble_ozone']),              
    np.array(rootgrp.variables['eurad_ozone']),
    np.array(rootgrp.variables['lotoseuros_ozone']),
    np.array(rootgrp.variables['match_ozone']),
    np.array(rootgrp.variables['mocage_ozone']),
    np.array(rootgrp.variables['silam_ozone']),
]


#making graphs of O3 per hour
def make_graph():
    
    map_proj = ccrs.PlateCarree()
    time = 0

    for i in range(len(hour)):
        time += 1
        for m in range(len(models)):

            print('..............', m, '..............')

            ax1 = plt.subplot(3, 3, (m + 1), projection = map_proj)
            ax1.coastlines(zorder=3)
            plt.contour(long, lat, models[m][(i+1), 1:, 1:], 1000, transform = ccrs.PlateCarree())
            ax1.set_title(f'O3 levels in Europe in hour {i}')

    print(time)
    plt.show()

make_graph()