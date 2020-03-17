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

start = tm.perf_counter()
rootgrp = xr.open_dataset("bigData.nc")                                           #opening the .nc file
# color_input = 

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
def make_graph(hours):
    map_proj = ccrs.PlateCarree()
    fig = plt.figure()

    for m in range(len(models)):
        print('..............','Hours: ', hours,' Models: ', (m + 1), '.............. \n')
        
        ax1 = plt.subplot(4, 2, (m + 1), projection = map_proj)
        ax1.coastlines(zorder = 3)
        img = plt.contour(long, lat, models[1][hours, :, :], 1000, transform = map_proj)            #magma 
        plt.subplots_adjust(hspace = 0.4)
        ax1.set_title(f'{modelsNames[m]}', fontsize = 9)

    set_axis(ax1, hours, fig, img)
    # plt.contour(img, cmap = 'cividis')           
    plt.show()


def set_axis(ax1, hours, fig, img):
    axins = inset_axes( ax1,
            width = "7%",  
            height = "500%",  
            loc = 'lower left',
            bbox_to_anchor = (1.2, 0., 1, 1),
            bbox_transform = ax1.transAxes,
            )

    plt.colorbar(img, cax = axins, orientation = "vertical")
    mticker.Locator.MAXTICKS = 2000
    fig.suptitle(f'O3 levels in {hours} hour(s)')
    # plt.savefig(f'{hours}.png')



# def parallel_processing():
#     with concurrent.futures.ProcessPoolExecutor(max_workers = 25) as executer: 
#         hours = [i for i in range(25)]
#         executer.map(make_graph, hours)

# if __name__ == '__main__':
#     parallel_processing()

#calling functions
make_graph(1)

#timer of process
finish = tm.perf_counter()
tot_time = round(finish-start,0)
time = datetime.timedelta(seconds = tot_time)
print(f'Finished in {time} hours')


