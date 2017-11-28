import pandas as pd
from datetime import datetime
import numpy as np
import os.path
import math
import numpy as np

def getRideData():
    ridefile = "dataset\\green_tripdata_2016-06.csv"
    return pd.read_csv(ridefile)

def countTaxiRides():
    data = getRideData()
    df = pd.DataFrame(data)
    df['Date'] = pd.DatetimeIndex(df['lpep_pickup_datetime']).date
    df = df.groupby(['Date']).size().reset_index().rename(columns={0:'Number_of_rides'})
    df.to_csv('dataset\\day_count.csv', index = False)
    print df.tail()
    
def countDayDiff():
    data = getRideData()
    df = pd.DataFrame(data)
    pickupDate = pd.DatetimeIndex(df['lpep_pickup_datetime']).date
    dropoffDate = pd.DatetimeIndex(df['Lpep_dropoff_datetime']).date    
    df['Number_of_days'] = dropoffDate - pickupDate
    df['Number_of_days'] = df['Number_of_days']/np.timedelta64(1, 'D') + 1
    df = df[['lpep_pickup_datetime', 'Lpep_dropoff_datetime', 'Number_of_days']]
    df.to_csv('dataset\\day_diff.csv', index = False)
    print df.tail()    
    
def countTaxiDrops():
    data = getRideData()
    df = pd.DataFrame(data)
    df['Date'] = pd.DatetimeIndex(df['Lpep_dropoff_datetime']).date
    df = df.groupby(['Date']).size().reset_index().rename(columns={0:'Number_of_drops'})
    df.to_csv('dataset\\drop_hour_count.csv', index = False)
    print df.tail()    
    
def calculateRideDuration():
    data = getRideData()
    df = pd.DataFrame(data)
    a = pd.to_datetime(pd.Series(df['lpep_pickup_datetime']), format = '%Y-%m-%d %H:%M:%S')
    b = pd.to_datetime(pd.Series(df['Lpep_dropoff_datetime']), format = '%Y-%m-%d %H:%M:%S')
    hour = (((b - a)/np.timedelta64(1, 'h')) + 1).astype(int)
    beforehour = hour - 1
    hour = hour.apply(str)
    beforehour = beforehour.apply(str)
    df['Duration_in_hours'] = "(" + beforehour + " - " + hour + ")"
    df = df.groupby(['Duration_in_hours']).size().reset_index().rename(columns={0:'Number_of_rides'})
    df.sort_values(by=['Number_of_rides'], ascending=False, inplace=True)
    df.to_csv('dataset\\duration_hour_count.csv', index = False)
    print df.tail()
    
def countRidesByVendor():
    data = getRideData()
    df = pd.DataFrame(data)
    df = df.groupby(['VendorID']).size().reset_index().rename(columns={0:'Number_of_trips'})
    df.to_csv('dataset\\vendor_count.csv', index = False)
    print df.tail()
    
def distFromCoordinates(lat1, lon1, lat2, lon2):
  R = 6371

  d_lat = np.radians(lat2-lat1)
  d_lon = np.radians(lon2-lon1)

  r_lat1 = np.radians(lat1)
  r_lat2 = np.radians(lat2)

  a = np.sin(d_lat/2.) **2 + np.cos(r_lat1) * np.cos(r_lat2) * np.sin(d_lon/2.)**2
  haversine = 2 * R * np.arcsin(np.sqrt(a))
  return haversine

def calculateGpsDistance():
  df = getRideData()
  df = df[['Pickup_longitude', 'Pickup_latitude', 'Dropoff_longitude', 'Dropoff_latitude']]
  distance = []
  
  for index, row in df.iterrows():
      lat1 = row['Pickup_latitude']
      lon1 = row['Pickup_longitude']
      lat2 = row['Dropoff_latitude']
      lon2 = row['Dropoff_longitude'] 
      value = distFromCoordinates(lat1, lon1, lat2, lon2)
      distance.append(value)
      
  pdDistance = pd.Series([ float(x) for x in distance ])
  pdDistance = pdDistance.astype(int)
  pdDistance = pdDistance + 1      
  df['Distance_in_km'] = pdDistance
  beforedistance = pdDistance - 1
  pdDistance = pdDistance.apply(str)
  beforedistance = beforedistance.apply(str)
  df['Distance_in_km'] = "(" + beforedistance + " - " + pdDistance + ")"
  df = df.groupby(['Distance_in_km']).size().reset_index().rename(columns={0:'Number_of_rides'})
  df.sort_values(by=['Number_of_rides'], ascending=False, inplace=True)
  df.to_csv('dataset\\gps_distance.csv', index = False)
  print df.head()
  