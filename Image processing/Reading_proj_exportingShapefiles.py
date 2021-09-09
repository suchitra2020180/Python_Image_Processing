# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:24:59 2020

@author: Suchitra
"""
# -*- coding: utf-8 -*-
##reset
##cls
###Use print to dispaly command outputs
import geopandas as gpd    ####matplotlibrary is also a part of geopandas
help(gpd)   #####Gives more info abt geopandas
########################################1.Reading ESRI Shape files
district=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm2.shp')
state=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm1.shp')
India=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm0.shp')
Odisha=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\ArcGis_Lockdown\India_ODISHA.shp')
### Once shapefile is imported into python..it becomes a geopandas dataframe...now it is not a shapefile
print(state)   ###To check the state and its geometry
print(state.columns) ###Gives column names in the shapefile
print(state.head())
state['geometry'] ##%%for selecting geometry col in state data
state[['NAME_0','NAME_1']]  ###Column names are taken from state.columns

Odisha.columns
Odisha['geometry']
type(state)   ###Tells the type which is geodataframe
##Geometry is the geometrical data which tells the spatial data##Never delete it 
state.plot()   ##### Displays the shape files##plot can used as it is a part of geopandas dataframe
###Default color of plot is blue
state.plot(color='green')    ###If we want to change the color of plot
state.plot(color= 'green', edgecolor = 'black')  ### Gives color to boundaries of shapefile
####If we want different colors for each state in India
state.plot(cmap='jet',edgecolor= 'black', column='NAME_1') ##Depending on NAME_1 the colors are assigned..if two rows has same value or name then same color would be assigned
#####Basic commands
state=state[['NAME_1','geometry']]  #####If we need only columns of the data
Ass_removedstate=state[state['NAME_1'] !='Assam'] ######Removing Assam state
Ass_removedstate.plot()
state.plot()
Assam=state[state['NAME_1']=='Assam']  #####Displaying only Assam state
Assam.plot()
print(Assam.crs)
Proj_Assam=Assam.to_crs(epsg=3857)####Check these epsg code for india
Proj_Assam.plot()
Proj_state=state.to_crs(epsg=3857)
Proj_state.plot(cmap='jet',edgecolor='red',column='NAME_1')
state['Area in DD']=state.area
Proj_state['Area in m2']=Proj_state.area
Proj_state['Area in km2']=Proj_state.area/1000000

##############################################Adding Legend    ##preferred method
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize = (10,8))
Proj_state.plot(ax=ax,cmap='jet',column='Area in km2', legend=True,legend_kwds={'label':"Area of state(Sq.km)"})

#####Another method for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable
fig,ax=plt.subplots(figsize=(10,8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right",size='7%',pad = 0.1)
Proj_state.plot(column='Area in km2',cmap='hsv',legend=True,legend_kwds ={'label':"Area of states(Sq.km)"},ax=ax,cax=cax)

###############################################    2.Plotting maps from different resources: side by side #############
import matplotlib.pyplot as plt  ####As all properties of matplotlib cannot be used through geopandas
fig,(ax1,ax2)=plt.subplots(ncols =2)
state.plot(ax=ax1)
Odisha.plot(ax=ax2)
####It we need to add different colors and looks good each plot
fig,(ax1,ax2)=plt.subplots(ncols =2,figsize=(10,8))   ##instaed of nrows ,we can also nrows
state.plot(ax=ax1,cmap='hsv',edgecolor='black',column='NAME_1') ##Coloring based on state names
Odisha.plot(ax=ax2, color= 'blue')
###################################    3.Plotting multiple layers ############################
fig,ax=plt.subplots(figsize = (10,8))
state.plot(ax=ax,cmap='hsv',edgecolor='black',column='NAME_1')
Odisha.plot(ax=ax, color= 'none',edgecolor='white') ##### units: decimal degrees
ax.set_title('GCS_WGS_1984')
###Similarly we can add atm locations in these area as points in image
##atm.plot(ax=ax, color='black',markersize=6)  ###This is a shapefile
#####So TO ADD LOCATIONS IN CHILIKA I NEED POINT SHAPEFILE TO PLOT IN PYTHON
###################################################      4. Working on Projections #############################
####Here we are acuurately plotting data in spatial domain as it contaons coordinates
###Its Geographic coordinate system  here it was WGS_1984
print(state.crs)  ###crs: Coordinate ref system : Here o/p: {'init': 'epsg:4326'}
print('states')
#####epsg: 4326 is WGS_1984:4326 is just the EPSG identifier of WGS84.  From Google
print(Odisha.crs)    ###O/P:4326
print('Odisha')
#Odisha.crs.name ###For point shape files 
#Odisha.crs.datum
###Here the data is plotted in GCS_WGS..But if we want to calculate area(km2) usinhg WGS_1984 output of area is in decimaldegrees ,which is of no use
###so we need to project the image in different coordinate system..So converting data from one crs to others using geopandas



############## ################################### 4a.  REPROJECTING GEOPANDAS GEODATFRAMES(Need to work)
##gOdisha=gpd.GeoDataFrame(Odisha,crs=Crs,geometry=Odisha['geometry'])
#gOdisha.to_crs(crs={'init': 'epsg:32645'})
#Projected_Odisha=Odisha.to_crs(epsg=32644)
##gOdisha.plot()
#Projected_Odisha.plot()

##
# projected_Odisha= Odisha.to_crs(epsg=32644) ###check for mine
# projected_Odisha.plot()    ###Appearance of projected and original image will be different ###units: metrs
# print(projected_Odisha.crs)
# print("Odisha")
# projected_state=state.to_crs(epsg=32644)
# projected_state.plot()
# print(projected_state.crs)
# print('states')
##############################################Plotting projected images
###Tip: Plot Bigger image first then smaller images else it will overlqap smalller image ans is not visible
fig,ax=plt.subplots(figsize=(10,8))
#fig,ax=plt.subplot()
projected_state=state.to_crs(epsg=32644)
projected_state.plot(ax=ax,cmap='hsv',edgecolor='black',column='NAME_1')
projected_Odisha= Odisha.to_crs(epsg=32644) ###check for mine
projected_Odisha.plot(ax=ax,color= 'green',edgecolor='white')    ###Appearance of projected and original image will be different ###units: metrs
ax.set_title("Projected India Map")
print("Executed upto here")
###############                https://epsg.io/?q=India%20kind%3APROJCRS        check it for espg values
######################################################################## 6.Intersection of layers   ##can be used as mask for ndvi
AOI=gpd.overlay(projected_state,projected_Odisha, how='intersection')
AOI.plot(color='blue',edgecolor='red')
print(AOI) ####To check attributes
print(AOI.columns)
##############################################################  6. Calculate Areas of AOI
###Creats a column with name AREA in AOI attribute table
AOI['Area']=AOI.area #######As we r working in UTM==>units of  area is m2
AOI['Area']=AOI.area/1000000 ##units is km2
print(AOI.columns)
#########################################################  7 .Exporting Geopandas Geodataframe into an ESRI shape file
AOI.to_file('AOI.shp',driver='ESRI Shapefile')  ##Driver is always esri shapefile
####This file is now saved in my folder abd we can open this file in QGIS just by dragging the file from folder  to QGIS interface and also check for attribute table init.U can aslo find area column also

########################################              Not from geodelta    5. Way to find ESPG COde
#import pyproj
#crs = pyproj.CRS("+proj=laea +lat_0=45 +lon_0=-100 +x_0=0 +y_0=0 +a=6370997 +b=6370997 +units=m +no_defs")
#crs.to_epsg()
#help(pyproj)
#type(pyproj)
