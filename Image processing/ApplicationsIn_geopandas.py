# -*- coding: utf-8 -*-

import geopandas as gpd
import matplotlib.pyplot as plt
SA1=gpd.read_file(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\Study_Area_1.shp')
SA2=gpd.read_file(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\Study_Area_2.shp')
river=gpd.read_file(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\river.shp')
fig,ax=plt.subplots(figsize=(8,6))
SA1.plot(ax=ax,color='red',edgecolor='black')
SA2.plot(ax=ax,color='none',edgecolor='black')
river.plot(ax=ax,color='blue')
### Tip:There are some common places ...so see that use color=none for second plot to know the extent
#####As second plot overlaps the first
#############   1. Intersection of polygon
Intersection=gpd.overlay(SA1,SA2,how='intersection')
Intersection.plot()

################## 2. Union of polygons
Union=gpd.overlay(SA1,SA2,how='union')
Union.plot()
###In union attribute table we have 3 attributes==>1. SA1,2.SA2,3.intersection of SA1,SA2

############## 3.Symmetrical differences ####(A union B)-(A intersection B)
Sym_dif=gpd.overlay(SA1,SA2,how='symmetric_difference')
Sym_dif.plot()

############# 4. Polygon difference    ### A- B
dif=gpd.overlay(SA1,SA2,how='difference')
dif.plot() ####O/p: SA1 - SA2

#### To get SA2 instead of SA1
dif1=gpd.overlay(SA2,SA1,how='difference')
dif1.plot() ####O/p: SA1 - SA2

##########5. Dissolve
union=gpd.overlay(SA1,SA2,how='union')
###Dissolve will give only 1 attribute of union which actually have 3 attributes ###Needs a common value
###SO common col is created
union['common_col']=1
dissolved_area=union.dissolve(by='common_col')
dissolved_area.plot() ###Single continous ploygon

################      6. Creating Buffer around river upto 500m
#Steps: Need to check river coordinate system
##Buffer can be done only on geoseries
#Geoseries is one of the column in geodataframe like geometry
###Buffer can be applied to poinys ,lines and polygons
print(river.crs)
proj_river = river.to_crs(epsg=24547) ##EPSG of Malayasia
print(proj_river.crs)
print(type(proj_river))   ### O/P; <class 'geopandas.geodataframe.GeoDataFrame'>
print(type(proj_river['geometry']))   ###O/p: <class 'geopandas.geoseries.GeoSeries'>
###Applying buffer
buffer_500m=proj_river['geometry'].buffer(distance = 500)
buffer_500m.plot(figsize=(7,7))

########################## 7. Centroid of polygons
##Centroid also works on geoseries
##Needs union which consists of 3 attributes==> 3 columns
union1=gpd.overlay(SA1,SA2, how='union')
union1.plot(cmap='hsv',edgecolor= 'black')
centroid=union['geometry'].centroid
centroid.plot()
###To get both union and centroid in one plot
fig,ax=plt.subplots(figsize=(10,8))
union1.plot(ax=ax,color='blue',edgecolor='black')
centroid.plot(ax=ax,color='black')
####Output is 3 centroids for 3 areas

###############################  8.  Point geometries
##Finding where are the airports
import pandas as pd
from shapely.geometry import Point
airports=pd.read_csv(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\us_airports.csv')
print(airports.head())
print(airports.columns)
####Use lat and long column to create geometry column
geometry =[Point(xy) for xy in zip(airports['LONGITUDE'],airports['LATITUDE'])]
#######Preferrred is using points_ from_xy(x,y) method
geometry1=gpd.points_from_xy(airports['LONGITUDE'], airports['LATITUDE'])

##### Converting csv data to geodataframe with crs of USstate shapefile or we can given directly crs as Crs={'init':'epsg:4326'}  andcrs=Crs
us_state=gpd.read_file(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\us_states.shp')
airports_us = gpd.GeoDataFrame(airports, crs= us_state.crs, geometry=geometry1)
airports_us.plot(color='red',markersize= 15,marker='*')

#########################           9.Attribute Join ##Joining two files   ##using csv files
#Files: airports,      and check common attributes in both files ##then find common states with  corresponding airports
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
us_state_names=pd.read_csv(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\state names and codes.csv') 
airports=pd.read_csv(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\us_airports.csv')
print(us_state_names.columns) ###state_name,state_code
print(airports.columns) ####ndex(['IATA', 'AIRPORT', 'CITY', 'STATE', 'COUNTRY', 'LATITUDE', 'LONGITUDE'], dtype='object')
### As the columns are different we need a common column #### airports['STATE']  is same as us_state_names['state_name']
###So need to rename STATE in airport as state_code (As state_name is there is us_state_names)
airports.rename(columns={'STATE':'state_code'},inplace=True) #####Syntax:df.rename(columns={"A": "a", "B": "c"})
##Now when we check airports.columns we can find state_name
###Now for joining do merge
airports_us=airports.merge(us_state_names, on='state_code')

#############################               10. Spatial Join using geopandas  ###using shapefiles
#####Displaying airports in us_state map   ###Shape file+csv file
##Spatial joins are completly dependent on spatial locations
us_state=gpd.read_file(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\us_states.shp')
us_state.plot()

airports=pd.read_csv(r'F:\Online courses\Geodeltalabs\10 Applications of GeoPandas\us_airports.csv')
airports_us = gpd.GeoDataFrame(airports,crs=us_state.crs,geometry=gpd.points_from_xy(airports['LONGITUDE'], airports['LATITUDE']))
airports_us.plot(color='red',markersize= 15,marker='*')

import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,8))
us_state.plot(ax=ax,edgecolor='black')
airports_us.plot(ax=ax,color='red',markersize= 15,marker='*')

###Now we want to extract the state of each airport from image
S_airports_us=gpd.sjoin(airports_us,us_state,how='inner',op='intersects')
#left: indicates airport_us ==> gives index i.e., geometry of left dataframe
S_airports_us.columns