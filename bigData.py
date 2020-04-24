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



def open_file():
    nc_file = [f for f in os.listdir('.') if f.endswith('.nc')]                    #finds .nc file in the same dir
    if len(nc_file) != 1:                                                          #checks if there is only one .nc file on dir
        raise ValueError('should be only one .nc file in the current directory')   #raises error if not

    print("The file updoaded is ", nc_file)                                        #prints name of file
    filename = nc_file[0]
    open_file.rootgrp  = xr.open_dataset(filename)                                 #opens the file

open_file()


#variables
rootgrp = open_file.rootgrp                                                         #reassigning var

lat = np.array(rootgrp.variables['lat'])                                            #extract/copy the data of lat
long = np.array(rootgrp.variables['lon'])                                           #extract/copy the data of lon
hour = np.array(rootgrp.variables['hour'])                                          #extract/copy the data of time

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

modelsNames = [                                                                      #list with models names
    'emep_ozone',
    'chimere_ozone',
    'ensemble_ozone',
    'eurad_ozone',
    'lotoseuros_ozone',
    'match_ozone',
    'mocage_ozone',
    'silam_ozone',
]

color_names = {                                                                      #dic of color names                       
                1: 'viridis', 
                2: 'jet', 
                3: 'inferno', 
                4: 'cubehelix', 
                5: 'cividis'
            }


def input_colour():    
    while True:
        print('Colorsets: \n', '\n '.join("{}: {}".format(k, v) for k, v in color_names.items()))       #print dic of color names
        color_input = input('Chose a colorset for the graphs: ')                                        #input for color names

        try:
            input_colour.val_color = int(color_input)                                                    #convert input color names to int
            if input_colour.val_color  in range(1,6):                                                                 #if input color names is between 1 and 5
                input_colour.view_graphs = input('Do you want to view the graphs? (yes/no): ')           #prints show graps
                
                if (input_colour.view_graphs == "yes") or (input_colour.view_graphs == "no"):
                    print(color_names[input_colour.val_color])                                           #if input of show graphs is yes or no
                    print('\n                        STATUS')                                            #print status
                    break                                                                                #leave the while loop 
                else:
                    print("\n \u001b[1m EROOR: insert yes or no \u001b[0m \n")                           #error if show graphs is not yes or no

            else:
                print("\n \u001b[1m ERROR: insert a valid colour number \u001b[0m \n")                   #error if input color name is not between 1 and 6
        except ValueError:
            print("\n \u001b[1m EROOR: please choose a number fom 1 to 5 \u001b[0m \n")                  #error if input color name is not int
    
start = tm.perf_counter()

#making graphs of O3 per hour
def make_graph(hours):
    map_proj = ccrs.PlateCarree()
    fig = plt.figure()
    plt.title(f'O3 in {hours}h')

    for m in range(len(models)):
        print('\n ..............','Hours: ', hours,' Models: ', (m + 1), '.............. \n')
        
        ax1 = plt.subplot(5, 2, (m + 1), projection = map_proj)                                         #plot graphs in 2 colums in 4 rows
        ax1.coastlines(zorder = 3)                                                                      #creates the cost lines
        plt.subplots_adjust(hspace = 0.5)                                                               #space between plots
        ax1.set_title(f'{modelsNames[m]}', fontsize = 9)        
        img = plt.contour(long, lat, models[m][hours, :, :], 1000, 
                cmap = color_names[input_colour.val_color], transform = map_proj)  
    
    cax = ax1.inset_axes([-3.4, -1, 5, 0.3])
    plt.colorbar(img, cax = cax, anchor = (3, 0.5), orientation = "horizontal")
    mticker.Locator.MAXTICKS = 2000                                                         #mesurments on the colorbar
    plt.suptitle(f'O3 levels in {hours} hour(s)')
    
    if not os.path.exists('O3_images'):                                                     #checks if folder exists
        os.makedirs('O3_images')                                                            #if not is created

    plt.savefig(f'O3_images/{hours}.png')                                                   #saves img in forger with hour as name
    
    #interface quit button -- quits all graphs at once
    def handler(*args, **kwargs):
        print('Bye!')
        plt.close('all')                                                                    #closes all windows

    ax_color_button = plt.axes([0.425, 0.04, 0.14, 0.05])                                   #button's dimentions
    color_button = Button(ax_color_button ,'Quit all')                                      #€button's messagen when clicked
    color_button.on_clicked(handler)                                                                        #incorporates the quit button
    
    if input_colour.view_graphs == "yes":                                                                #if input show graphs is yes
        plt.show()                                                                          #show graphs


#makes de parallel process
def parallel_processing():
    with concurrent.futures.ProcessPoolExecutor(max_workers = 24) as executer:              #set num of parallel processes
        hours = [i for i in range(1,25)]                                                    #each process gets an hiur
        executer.map(make_graph, hours)                                                     #executs the processess


if __name__ == '__main__':
    input_colour()   
    parallel_processing()
    

#timer of process
finish = tm.perf_counter()
tot_time = round(finish-start,0)
time = datetime.timedelta(seconds = tot_time)
print(f'Finished in {time} hours')

