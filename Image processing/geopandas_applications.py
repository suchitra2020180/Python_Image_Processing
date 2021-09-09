import geopandas as gpd 
import matplotlib.pyplot as plt 
import pandas as pd
from shapely.geometry import Point

# Importing the states ESRI Shapefile of the USA 
us_states = gpd.read_file('us_states.shp')
us_states.plot()

airports_data = pd.read_csv('us_airports.csv')
geometry = [Point(xy) for xy in zip(airports_data['LONGITUDE'],airports_data['LATITUDE'])]
airports_us = gpd.GeoDataFrame(airports_data, geometry = geometry, crs = us_states.crs)

airports_us = airports_us[['AIRPORT', 'geometry']]


fig, ax = plt.subplots(figsize = (8,8))
us_states.plot(ax = ax, color = 'blue', edgecolor = 'black')
airports_us.plot(ax=ax, markersize = 2, color = 'green')

# Spatial Join

airports_us = gpd.sjoin(airports_us, us_states, how  = 'inner', op = 'intersects')

