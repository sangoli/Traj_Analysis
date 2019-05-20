import math as m
import json
import itertools
import datetime
from datetime import timedelta
from math import sin, cos, sqrt, atan2,radians

#setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
relativeNullPoint={}
p={}
relativeNullPoint['latitude']=39.75872#for beijing
relativeNullPoint['longitude']=116.04142#for beijing

class DictList(dict):

    def __setitem__(self, key, value):
        try:
            # print("intry")
            # print(value)
            # print(self[key])
            # Assumes there is a list on the key
            self[key].extend(value)
            # print(self[key])
        except KeyError: # if fails because there is no key
            # print("key error")
            super(DictList, self).__setitem__(key, value)
            # print(self[key])
        except AttributeError: # if fails because it is not a list
        # print("attribute error")
            super(DictList, self).__setitem__(key, [self[key], value])


def asRadians(degrees):
    return degrees * m.pi / 180

def getXYpos(relativeNullPoint, p):
    """ Calculates X and Y distances in meters.
    """
    deltaLatitude = p['latitude']- relativeNullPoint['latitude']
    deltaLongitude = p['longitude'] - relativeNullPoint['longitude']
    latitudeCircumference = 40075160 * m.cos(asRadians(relativeNullPoint['latitude']))
    resultX = deltaLongitude * latitudeCircumference / 360
    resultY = deltaLatitude * 40008000 / 360
    return resultX, resultY

def getLatLng(relativeNullPoint,x,y):
    latitudeCircumference = 40075160 * m.cos(asRadians(relativeNullPoint['latitude']))
    deltaLatitude=y *360/40008000
    deltaLongitude=x * 360/latitudeCircumference

    resultLat=deltaLatitude+relativeNullPoint['latitude']
    resultLng=deltaLongitude +relativeNullPoint['longitude']

    return resultLat,resultLng


def mapp(ds,dt):
    d = DictList()
    fragment_dict = DictList()

    for i in range(4):
    # for i in range(182):

        user_str = '%03d' % i
        with open('parsed_data/output_'+user_str+'.txt') as f:
            print(user_str)
            pid=0
            for line in f:
                pid=pid+1
                lat1, lng1, date1, time1 = line.strip('\n').split(',')[0:5]
                p['latitude'] = float(lat1)
                p['longitude'] = float(lng1)
                ptLatConv, ptLngConv = getXYpos(relativeNullPoint, p)
                tileLatConv = int(ptLatConv / ds) * ds
                tileLngConv = int(ptLngConv / ds) * ds
                # print("Tile lat,lng in meters with current point:")
                # print((tileLatConv, tileLngConv))
                df1 = date1 + " " + time1
                t = datetime.datetime.strptime(df1, datetimeFormat)
                ttotal=t.timestamp()
                t=int(t.timestamp()/dt)*dt
                hash_lat,hash_lon=getLatLng(relativeNullPoint, tileLatConv, tileLngConv)
                # print((hash_lat,hash_lon))
                # hash_str=str(str(hash_lat)[:6])+'_'+str(str(hash_lon)[:6]+'_'+str(date1)+"_"+str(time1[:4]))
                hash_str = str(str(hash_lat)) + '_' + str(str(hash_lon) +'_'+str(t))
                d[hash_str]=[(user_str,lat1,lng1,date1,time1,pid,ttotal)]
    print("Tiles generated")
    # print(d.keys())
    print("No of tiles are :"+str(len(d.keys())))
    with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt", 'w') as f:
        json.dump(d, f)
    # with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt") as f:
    #     load_dict = json.load(f)

    #################################
ds=100
dt=300
mapp(ds,dt)# call based on ds and dt