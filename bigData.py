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

color_names = {
            1: 'viridis', 
            2: 'plasma', 
            3: 'inferno', 
            4: 'magma', 
            5: 'cividis',
}

print('Colorsets: \n', '\n '.join("{}: {}".format(k, v) for k, v in color_names.items()))
color_input = int(input('Chose a colorset for the graphs: '))
print('\n                        STATUS')


#making graphs of O3 per hour
def make_graph(hours):
    map_proj = ccrs.PlateCarree()
    fig = plt.figure(f'O3 in {hours}h')

    for m in range(len(models)):
        print('\n ..............','Hours: ', hours,' Models: ', (m + 1), '.............. \n')
        
        ax1 = plt.subplot(4, 2, (m + 1), projection = map_proj)
        ax1.coastlines(zorder = 3)
        plt.subplots_adjust(hspace = 0.4)
        ax1.set_title(f'{modelsNames[m]}', fontsize = 9)        

        if color_input not in color_names:
            img = plt.contour(long, lat, models[m][hours, :, :], 1000, transform = map_proj)            
        else:
            img = plt.contour(long, lat, models[m][hours, :, :], 1000, cmap = color_names[color_input], transform = map_proj)

    set_axis(ax1, hours, fig, img)
    quit_button(img)
    plt.savefig(f'{hours}.png')


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

def quit_button(img):

    def handler(*args, **kwargs):
        print('Bye!')
        plt.close('all')

    ax_color_button = plt.axes([0.825, 0.04, 0.14, 0.05])
    color_button = Button(ax_color_button ,'Quit all')
    color_button.on_clicked(handler)
       

def parallel_processing():
    with concurrent.futures.ProcessPoolExecutor(max_workers = 24) as executer: 
        hours = [i for i in range(1,25)]
        executer.map(make_graph, hours)
  

if __name__ == '__main__':
    parallel_processing()
    

#timer of process
finish = tm.perf_counter()
tot_time = round(finish-start,0)
time = datetime.timedelta(seconds = tot_time)
print(f'Finished in {time} hours')

