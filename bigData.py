from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
import cartopy.crs as ccrs
import multiprocessing as mp
import numpy as np
import xarray as xr
import time as tm


start = tm.perf_counter()
num_cores = mp.cpu_count()
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

modelsNames = [                                                                        #extract data from models: call each model models['emep_ozone']
    'emep_ozone',
    'chimere_ozone',
    'ensemble_ozone',
    'eurad_ozone',
    'lotoseuros_ozone',
    'match_ozone',
    'mocage_ozone',
    'silam_ozone',
]


#making graphs of O3 per hour
def make_graph():
    
    map_proj = ccrs.PlateCarree()
    time = 0

    for i in range(len(hour)):
        time += 1
        print('Hour', time)
        fig = plt.figure()

        for m in range(len(models)):

            print('..............', (m + 1), '..............')

            ax1 = plt.subplot(4, 2, (m + 1), projection = map_proj)
            ax1.coastlines(zorder = 3)
            img = plt.contour(long, lat, models[m][i, :, :], 1000, transform = ccrs.PlateCarree())
            plt.subplots_adjust(hspace = 0.4)
            ax1.set_title(f'{modelsNames[m]}', fontsize = 9)

        axins = inset_axes(ax1,
                    width = "7%",  
                    height = "500%",  
                    loc = 'lower left',
                    bbox_to_anchor = (1.2, 0., 1, 1),
                    bbox_transform = ax1.transAxes,
                   )

        plt.colorbar(img, cax = axins, orientation="vertical")
        finish = tm.perf_counter()
        print(f'Finished in {round(finish-start,2)} second(s)')
        fig.suptitle(f'O3 levels in {i} hour(s)')
        plt.show()

make_graph()

finish = tm.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')

