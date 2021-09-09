# -*- coding: utf-8 -*-



##Basefile:F:Work:/Correlation Regression/latlong\Chilika Latlong
#%matplotlib inline
from shapely.geometry import Point
#import descartes ####
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
#import shapefile
from osgeo import gdal

#####Reading Lat and long of fields from Excel
df = pd.read_excel(r'D:\1Desktop\3PSD_copy of labpc\PSD Data_Black pendrive--April4_2020\PSD_FC3Data\PSD April Lockdown\4.CHK_D50_FF_GT_Latlong.xlsx',sheet_name='Sheet1')
Crs={'init':'epsg:4326'} 
gdf= gpd.GeoDataFrame(df, crs=Crs,geometry=gpd.points_from_xy(df['Long'], df['Lat']))
#####Coordinate system 
gdf.head() 
gdf.plot(figsize=(5,5))
gdf.to_file('FC3Data.shp', driver='ESRI Shapefile') ####Saving as  point shape file
## Saved here:F:\Work\CorrelationsAndRegression\Lat_Long............But no driver with name: ESRI Shapefile
#####Reading Sentinel-2 Data Processed in arcmap
fig,ax=plt.subplots(1,figsize=(5,5))
Chk=gpd.read_file("F:\Work\Arcgis2020\ArcMap_Oct2020_DataFeb7_2019\db665tiftopolygon.shp")
crs={'init':'epsg:4326'} 
print(Chk.head(5))
print(Chk.crs)
Chk.plot(ax=ax)
#plt.show()
############################################## This works for Chk+sample points
# ####Both stations and Chilika
fig,ax=plt.subplots(1,figsize=(10,8))
Chk.plot(ax=ax,color='blue')
projected_gdf=gdf.to_crs(epsg=32645) 
projected_gdf.plot(ax=ax,color='darkred', marker="*", markersize=10)

# ####Both stations and Chilika
# fig,ax=plt.subplots(1,figsize=(5,5))
# Basemap=Chk.plot(ax=ax,color="blue") 
# projected_gdf=gdf.to_crs(epsg=32644) 
# projected_gdf.plot(ax=Basemap, color='darkred', marker="*", markersize=10)
# plt.legend()
# ax.set_title("FC3 Data Collected in Chilika", fontsize=25)
# #plt.savefig('FC3 Data Collected in Chilika.png',bbox_inches='tight');

#############For remaining code check Chk_lat_long.py in F:/Work/correlation and regression/lAT LONG/Chk_latlong


import gdal
import matplotlib.pyplot as plt
filepath = r"F:\Work\Arcgis2020\ArcMap_Oct2020_DataFeb7_2019\Chk_Rrs560.tif"
Rrs560 = gdal.Open(filepath).ReadAsArray()
Rrs560tif = gdal.Open(filepath)
print(Rrs560tif.GetMetadata())
type(Rrs560)
plt.imshow(Rrs560)
Rrs560.plot()

