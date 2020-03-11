import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs



rootgrp = xr.open_dataset("bigData.nc")                                              #opening the .nc file

lat = np.array(rootgrp.variables['lat'])                                          #extract/copy the data of lat
long = np.array(rootgrp.variables['lon'])                                         #extract/copy the data of lon
hour = np.array(rootgrp.variables['hour'])                                       #extract/copy the data of time

# models = [
#     'emep_ozone',

# ]

emep_ozone = np.array(rootgrp.variables['emep_ozone'][:])



def avr():
    hours = 0
    values = 0
    emep_ozoneTwoD = []

    for i in range(len(hour)):
        emep_ozoneTwoD = emep_ozone[i, :, :]
        hours += 1
        
        for j in range(len(lat)):
            for k in range(len(long)):
                values += 1
                print(emep_ozoneTwoD[j,k])
                    
    
    print('Hours: ', hours)
    print(emep_ozone.size)
    print(values)

avr()

#making graphs per hour
def graph(array):

    for i in range(len(hour)):
        emep_ozoneTwoD = emep_ozone[i, :, :]  #slices array converting it into 2D array for each hour
        plt.figure()
        ax = plt.axes(projection=ccrs.PlateCarree())
        plt.contour(long, lat, emep_ozoneTwoD, 1000, transform=ccrs.PlateCarree())
        ax.coastlines(zorder=3)
        ax.set_title(f'{i}h')

    plt.show()
