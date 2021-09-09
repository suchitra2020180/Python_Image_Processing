# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:42:31 2020

@author: Suchitra
"""
import geopandas as gpd    ####matplotlibrary is also a part of geopandas
help(gpd)   #####Gives more info abt geopandas
########################################1.Reading ESRI Shape files

district=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm2.shp')
state=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm1.shp')
India=gpd.read_file(r'D:\1Desktop\3PSD_copy of labpc\2PSD_Sentinel2\Downloaded_DivaGIS\IND_adm\IND_adm0.shp')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,8))
state.plot(ax=ax,edgecolor='black')
district.plot(ax=ax,color='None',edgecolor='red')



##############################################Adding Legend    ##preferred method
