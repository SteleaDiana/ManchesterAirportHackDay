#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:13:53 2020

@author: vladgriguta
"""
latMcr, lonMcr = 53.3588, -2.2727
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def get_planes(url = 'https://opensky-network.org/api/states/all'):
    
    import requests
    
    data = requests.get(url).json()
    
    cols = ['icao24','callsign','origin_country','time_position','last_contact'
            ,'longitude','latitude','geo_altitude','on_ground','velocity','heading'
            ,'vertical_rate','sensors','baro_altitude','squawk','spi','position_source']
    
    df = pd.DataFrame(data['states'],columns=cols)

    return df


def withinRadius(df, lat = 53.3588, lon = -2.2727, max_distance = 50, max_altitude = 5):
    earth_radius = 6373.0
    
    diff_coords = pd.DataFrame(index=df.index, columns=['lat','lon'],
        data=np.stack([np.deg2rad(df.latitude.values-lat),
                       np.deg2rad(df.longitude.values-lon)]).transpose())
    
    """
    # "Square of half the chord length between the points":
    var_a = (math.pow(math.sin(d_lat / 2), 2) + math.cos(lat_a) * math.cos(lat_b)
             * math.pow(math.sin(d_lon / 2), 2))
    # "Angular distance in radians":
    var_c = 2 * math.atan2(math.sqrt(var_a), math.sqrt(1 - var_a))
    """
    temp_a = np.sin(diff_coords.lat/2)**2 + (np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(df.latitude)) * 
                                           np.sin(diff_coords.lon/2)**2)
    
    temp_c = 2 * np.arctan2(np.sqrt(temp_a),np.sqrt(1-temp_a))
    
    diff_coords['dist'] = earth_radius * temp_c
    
    return df[diff_coords.dist<max_distance]





def plotData(dfMcr):
    fig, ax = plt.subplots(figsize=(10,10))
    m = Basemap(llcrnrlon=lonMcr-2,llcrnrlat=latMcr-3,
                urcrnrlon=lonMcr+2,urcrnrlat=latMcr+3,
                #width=1e5,height=1e5,
                resolution='i', # Set using letters, e.g. c is a crude drawing, f is a full detailed drawing
                projection='tmerc', # The projection style is what gives us a 2D view of the world for this
                lon_0=lonMcr,lat_0=latMcr, # Setting the central point of the image
                epsg=27700) # Setting the coordinate system we're using
    
    m.drawmapboundary(fill_color='#46bcec') # Make your map into any style you like
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec') # Make your map into any style you like
    m.drawcoastlines()
    m.drawrivers() # Default colour is black but it can be customised
    m.drawcountries()
    
    
    x, y = m(lonMcr, latMcr)
    plt.plot(x, y, 'ok', markersize=10)
    plt.text(x, y, ' Manchester', fontsize=20)
    
    for _,elem in dfMcr.iterrows():
        x,y = m(elem.longitude, elem.latitude)
        m.plot(x, y, marker = 'o', c='r', markersize=15, alpha=1, latlon=False)
    
    plt.show()



def main():
    df = get_planes()
    dfMcr = withinRadius(df)
    plotData(dfMcr)




