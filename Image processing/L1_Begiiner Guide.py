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
state    ###To check the state and its geometry
print(state.columns) ###Gives column names in the shapefile
print(state.head())
state['geometry']
Odisha.columns
Odisha['geometry']
state[['NAME_0','NAME_1']]  ###Column names are taken from state.columns
type(state)   ###Tells the type which is geodataframe
##Geometry is the geometrical data which tells the spatial data##Never delete it 
state.plot()   ##### Displays the shape files##plot can used as it is a part of geopandas dataframe
###Default color of plot is blue
state.plot(color='green')    ###If we want to change the color of plot
state.plot(color= 'green', edgecolor = 'black')  ### Gives color to boundaries of shapefile
####If we want different colors for each state in India
state.plot(cmap='jet',edgecolor= 'black', column='NAME_1') ##Depending on NAME_1 the colors are assigned..if two rows has same value or name then same color would be assigned

###############################################    2.Plotting maps from different resources: side by side #############
import matplotlib.pyplot as plt  ####As all properties of matplotlib cannot be used through geopandas
fig,(ax1,ax2)=plt.subplots(ncols =2)
state.plot(ax=ax1)
Odisha.plot(ax=ax2)
####It we need to add different colors and looks good each plot
fig,(ax1,ax2)=plt.subplots(ncols =2,figsize=(10,8))   ##instaed of nrows ,we can also nrows
state.plot(ax=ax1,cmap='hsv',edgecolor='black',column='NAME_1')
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
state.crs  ###crs: Coordinate ref system : Here o/p: {'init': 'epsg:4326'}
#####epsg: 4326 is WGS_1984:4326 is just the EPSG identifier of WGS84.  From Google
Odisha.crs    ###O/P:4326
###Here the data is plotted in GCS_WGS..But if we want to calculate area(km2) usinhg WGS_1984 output of area is in decimaldegrees ,which is of no use
###so we need to project the image in different coordinate system..So converting data from one crs to others using geopandas
########################################              Not from geodelta    5. Way to find ESPG COde
import pyproj
crs = pyproj.CRS("+proj=laea +lat_0=45 +lon_0=-100 +x_0=0 +y_0=0 +a=6370997 +b=6370997 +units=m +no_defs")
crs.to_epsg()
help(pyproj)
type(pyproj)
Odisha.plot()
####
from pyproj import Proj
Proj('+init=epsg:32645'.preserve_flags=True)
Proj({'init':'epsg:32645','no_defs':True},preserve_flags=True)


############## ################################### 4a.  REPROJECTING GEOPANDAS GEODATFRAMES(Need to work)

projected_Odisha= Odisha.to_crs(epsg=32645) ###check for mine
projected_Odisha.plot()    ###Appearance of projected and original image will be different ###units: metrs
projected_state=state.to_crs(epsg=32645)
projected_state.plot()
##############################################Plotting projected images
fig,ax=plt.subplot(figsize=(10,8))
projected_Odisha= Odisha.to_crs(epsg=32645) ###check for mine
projected_Odisha.plot(ax=ax,color= 'none',edgecolor='white')    ###Appearance of projected and original image will be different ###units: metrs
projected_state=state.to_crs(epsg=32645)
projected_state.plot(ax=ax,cmap='hsv',edgecolor='black',column='NAME_1')
###############                https://epsg.io/?q=India%20kind%3APROJCRS        check it for espg values
{'init': 'epsg:32645'} ####Output from satellit data
##Tried:
Odisha.to_crs(crs={'init': 'epsg:4326'},epsg=32645,inplace = False)
d=Odisha.to_crs(epsg =32645)
Odisha.to_crs({'init': 'epsg:32644'})  ##not working
Odisha.to_crs("EPSG:32644") ##not working
Odisha.crs = 'epsg:32644'   ##not working
Odisha.crs={'init': 'epsg:4326'}
gdf = Odisha.to_crs({'init': 'epsg:32644'})

geom = df.geometry.to_crs(crs=crs, epsg=epsg)
######################################################################## 6.Intersection of layers   ##can be used as mask for ndvi
AOI=gpd.overlay(projected_state,projected_Odisha, how='intersection')
AOI.plot(edgecolor='red')
AOI  ####To check attributes
##############################################################  6. Calculate Areas of AOI
###Creats a column with name AREA in AOI attribute table
AOI['Area']=AOI.area #######As we r working UTM==>units of  area is m2
AOI['Area']=AOI.area/1000000 ##units is km2

#########################################################  7 .Exporting Geopandas Geodataframe into an ESRI shape file
AOI.to_file('AOI.shp',driver='F:\Online courses\Geodeltalabs')
####This file is now saved in my folder abd we can open this file in QGIS just by dragging the file from folder  to QGIS interface and also check for attribute table init.U can aslo find area column also

"""
Created on Wed Nov 18 13:24:59 2020

@author: Suchitra
"""
# -*- coding: utf-8 -*-
##reset
##cls
import geopandas as gpd    ####matplotlibrary is also a part of geopandas
help(gpd)   #####Gives more info abt geopandas
########################################1.Reading ESRI Shape files
district=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm2.shp')
state=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm1.shp')
India=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm0.shp')
Odisha=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\ArcGis_Lockdown\India_ODISHA.shp')
### Once shapefile is imported into python..it becomes a geopandas dataframe...now it is not a shapefile
state    ###To check the state and its geometry
state.columns ###Gives column names in the shapefile
state.head()
print(state['geometry'])
Odisha.columns
Odisha['geometry']
state[['NAME_0','NAME_1']]  ##