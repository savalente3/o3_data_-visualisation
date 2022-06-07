# Data visualisation of O3 levels in Europe

The visualisation of O3 levels in Europe was achieved by extracting large amounts of data and plot it in a simple and effective manner. The software uses python in conjunction with matplotlib, cartopy and some other modules to plot the data in a map and create the images requested. A label to better understand the relation between the representation and the data values was solicited.

With this, twenty-four images were created, where each demonstrates the O3 levels analysed using different models, eight in total. A centralized map in Europe was implemented using the extracted coordinates of Europe from the data file, along with a side-by side-disposition of the graphs for a better visual comparison. In addition, a colorbar as a visual label was displayed at the bottom of each image. The software creates a default directory named O3_images where it saves all twenty-four images named with their respective time and png extension. This directory is created in the same directory the program is executed.

# Instructions

The execution of the code requires the installation of anaconda, there are mac and windows versins.
it includs the graphical installer and the terminal installer. However, i recomend the terminal 
installer, which can be download from:
https://www.anaconda.com/distribution/

After the installation of anaconda, the requirements.txt will install the remaining required packages
<conda install --file requirements.txt>

To run the code:
python3 bigData.py

To run the test:
python3 -m pytest tes_bigData.py
