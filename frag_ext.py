import math as m
import itertools

import json
# with open(mydatafile, 'w') as f:
#     json.dump(a, f)

import operator
import itertools
import datetime
from datetime import timedelta
from math import sin, cos, sqrt, atan2,radians
# import matplotlib.pyplot as plt

# import networkx as nx
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

datetimeFormat = '%Y-%m-%d %H:%M:%S'

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


p={}
# p['latitude']=39.984094
# p['longitude']=116.319236
p['latitude']=40.002991
p['longitude']=116.321491
print("Current Point(lat,lng) in degrees \n"+str(p.values()))
relativeNullPoint={}
relativeNullPoint['latitude']=39.75872
relativeNullPoint['longitude']=116.04142
print("Converted Lat and lng to meters for current point: ")
print(getXYpos(relativeNullPoint,p))

ds=500
dt=600
print("Distance threshold: ")
print(ds)
ptLatConv,ptLngConv=getXYpos(relativeNullPoint,p)

tileLatConv=int(ptLatConv/ds)*ds
tileLngConv=int(ptLngConv/ds)*ds

print("Tile lat,lng in meters with current point:")
print((tileLatConv,tileLngConv))

def getLatLng(relativeNullPoint,x,y):
    latitudeCircumference = 40075160 * m.cos(asRadians(relativeNullPoint['latitude']))
    deltaLatitude=y *360/40008000
    deltaLongitude=x * 360/latitudeCircumference

    resultLat=deltaLatitude+relativeNullPoint['latitude']
    resultLng=deltaLongitude +relativeNullPoint['longitude']

    return resultLat,resultLng

print("Tile lat,lng in degrees with current point:")
print(getLatLng(relativeNullPoint,tileLatConv,tileLngConv))



def createFragments(key,values,fc):
    # print(fragment_dict)
    for usr in range(2):
        curr_usr='%03d' % usr
        print("current user")
        frag_count = 1
        print(curr_usr)
        print("fragmenting tile no :")
        print(fc)
        # print(list(range(0,len(values)-1)))
        for pt_i in range(0,len(values)-1):
            if(values[pt_i][0]==curr_usr):
                    # print(pt_i)
                if abs(values[pt_i][5] - values[pt_i + 1][5]) == 1:
                        # fragment_dict[key]={curr_usr:{frag_count:values[pt_i]}}
                        fragment_dict[(key,curr_usr,str(frag_count))]=[values[pt_i]]
                        # print(fragment_dict)
                        # print("values")
                        # print(type(values[pt_i]))
                        # fragment_dict[key][curr_usr][str(frag_count)]=values[pt_i]
                        if(pt_i==max(range(len(values)-1))):
                            fragment_dict[(key, curr_usr, str(frag_count))] = [values[pt_i+1]]
                            # print(fragment_dict)
                            # fragment_dict[key][curr_usr][str(frag_count)] = values[pt_i+1]
                            # fragment_dict[key] = {curr_usr: {frag_count: values[pt_i+1]}}



                else:
                    print("else")
                    print(pt_i)
                    print(pt_i+1)
                    fragment_dict[(key, curr_usr, str(frag_count))] = [values[pt_i]]
                    # fragment_dict[key][curr_usr][str(frag_count)] = values[pt_i]
                    # fragment_dict[key] = {curr_usr: {frag_count: values[pt_i]}}

                    print("before")
                    # print(fragment_dict[key,curr_usr,str(frag_count)])
                        # fragment_dict[key]={curr_usr:{frag_count:values[pt_i+1]}}
                        # fragment_dict[(key,curr_usr,str(frag_count))]=values[pt_i]
                        # print(fragment_dict)
                    frag_count=frag_count+1
                    print("Incrementing fragment")
                    continue
                    # createFragments(key,values[pt_i+1:],fc)
    return fragment_dict





def mapp():
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
                # print(hash_str)
                # if(hash_str in d ):
                #     if(user_str not in d[hash_str][0]):
                #         d[hash_str]=[user_str,date1,time1]
                # else:

                # ls.extend()
                d[hash_str]=[(user_str,lat1,lng1,date1,time1,pid,ttotal)]
                     # d[hash_str]=user_str
    print("Tiles generated")
    # print(d.keys())
    print("No of tiles are :"+str(len(d.keys())))
    # count=1
    finalList=[]
    with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt", 'w') as f:
        json.dump(d, f)
    # with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt") as f:
    #     load_dict = json.load(f)
    load_dict=d
    #################################

    print("Creating Fragments")
    for key, values in load_dict.items():
                frag_count = 1
                for pt_i in range(0, len(values) - 1):
                        curr_usr= values[pt_i][0]
                        # print(pt_i)
                        if abs(values[pt_i][5] - values[pt_i + 1][5]) == 1:
                            # fragment_dict[key]={curr_usr:{frag_count:values[pt_i]}}
                            # fragment_dict[(key, curr_usr, str(frag_count))] = [values[pt_i]]
                            fragment_dict[key+"&"+curr_usr+"&"+str(frag_count)]=[values[pt_i]]
                            # print(fragment_dict)
                            # print("values")
                            # print(type(values[pt_i]))
                            # fragment_dict[key][curr_usr][str(frag_count)]=values[pt_i]
                            if (pt_i == max(range(len(values) - 1))):
                                # fragment_dict[(key, curr_usr, str(frag_count))] = [values[pt_i + 1]]
                                # print(fragment_dict)
                                # fragment_dict[key][curr_usr][str(frag_count)] = values[pt_i+1]
                                # fragment_dict[key] = {curr_usr: {frag_count: values[pt_i+1]}}
                                fragment_dict[key + "&" + curr_usr +"&" + str(frag_count)] = [values[pt_i+1]]




                        else:
                            # print("else")
                            # print(pt_i)
                            # print(pt_i + 1)
                            # fragment_dict[(key, curr_usr, str(frag_count))] = [values[pt_i]]
                            # fragment_dict[key][curr_usr][str(frag_count)] = values[pt_i]
                            # fragment_dict[key] = {curr_usr: {frag_count: values[pt_i]}}
                            # print("before")
                            fragment_dict[key + "&" + curr_usr +"&" + str(frag_count)] = [values[pt_i]]

                            # print(fragment_dict[key,curr_usr,str(frag_count)])
                            # fragment_dict[key]={curr_usr:{frag_count:values[pt_i+1]}}
                            # fragment_dict[(key,curr_usr,str(frag_count))]=values[pt_i]
                            # print(fragment_dict)
                            frag_count = frag_count + 1
                            # print("Incrementing fragment")
                            continue

                            # createFragments(key,values[pt_i+1:],fc)
            # print("inner")
            # print(len(fragment_dict))

    # print(len(fragment_dict))
    fg=fragment_dict
    ##########
    # for k ,v in fg.items():
    #     if(len(v)>1):
    #         # print(k)
            # print(len(v))
            # print(values)
            # with open("frag.txt",'a+') as j :
            #     j.write(k+"\n")
            #     j.write(str(v)+"\n")

    # createFragments(d)

    # for key,values in d.items():
    #     with open("user_points.txt",'a+') as up:
    #         up.write(key+"\n")
    #         up.write(str(values)+'\n')
    fc=0
    # for key,values in d.items():
    #     fc=fc+1
    #     fg=createFragments(key,values,fc)
    #     print(len(fg.keys()))
    # print(len(fg.keys()))
    # print(fg.keys())
    final_frag=DictList()
    for k1,v1 in fg.items():
            if(len(v1)>0):
                # print("key")
                # print(k1)
                # print(v1)
                # print(len(v1))
                lat_avg=sum([float(pair[1]) for pair in v1])/len(v1)
                lng_avg=sum([float(pair[2]) for pair in v1])/len(v1)
                max_time=max([float(pair[6]) for pair in v1])
                min_time=min([float(pair[6]) for pair in v1])

                # print(lat_avg,lng_avg,max_time)
                final_frag[k1.split('&')[0]]=[(k1.split('&')[1],lat_avg,lng_avg,min_time,max_time)]
    # print(final_frag)
    print("Writing CSV")
    with open("consolidated_csv/fragments_ds" + str(ds) + "_dt" + str(dt) + ".csv", 'a+') as wr:
        wr.write("UserA,LatA,LngA,Min_time_UserA,Max_time_UserA,UserB,LatB,LngB,Min_time_UserB,Max_time_UserB,Distance_apart(m),Interaction_time(ms),Tile_key\n")
    interaction_time=0

    for ft,vt in final_frag.items():
        # print(ft)
        if(len(vt)>1):
            # print(len(vt))
            # print(vt)
            for x,y in itertools.combinations(vt,2):
                    u1,la1,lo1,t1_min,t1_max=x
                    # df_1 = d1 + " " + t1

                    u2,la2,lo2,t2_min,t2_max=y

                    # df_2 = d2 + " " + t2
                    if (u1 != u2):
                        print("EUREKA")
                        # print(ft)
                        # print(vt)
                        if t1_max > t2_max and t2_min > t1_min:
                            interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                        elif t1_max < t2_max and t2_min < t1_min:
                            interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                        elif t1_max > t2_max and t1_min > t2_min:
                            interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                        elif t2_max > t1_max and t2_min > t2_min:
                            interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                        # print("u1" + str((t1_min, t1_max)))
                        # print("u2" + str((t2_min, t2_max)))
                        # print((u1, u2, interaction_time))
                        # print(ft)
                        # print(vt)
                        check=checkForOutliers(ft,x, y)

                        if check is not -1:

                            with open("consolidated_csv/fragments_ds"+str(ds)+"_dt"+str(dt)+".csv",'a+') as fn:
                                fn.write(u1+","+str(la1)+","+str(lo1)+","+str(t1_min)+","+str(t1_max)+","+u2+","+str(la2)+","+str(lo2)+","+str(t2_min)+","+str(t2_max)+","
                                         + str(checkForOutliers(ft,x,y))+","+str(interaction_time)+","+ft+"\n")





    # for key,values in fg.items():
    #     print(key)
    #     print(values)
    #     with open("frah.txt") as frg:
    #         frg.write()
    # # for key in d:
    #     print(fg[key,_,_])
    # fragment_dict=DictList()
    # for key,values in d.items():
    #     # for pt in values:
    #         # print(str(pt[5]))
    #     # print(len(values))
    #     for pt_i in range(len(values)-1):
    #         # print(i)
    #         if abs(values[pt_i][5]-values[pt_i+1][5])==1 :
    #             print(key)
    #             break_point=pt_i
    #             fragment_dict[key][str(values[0])]=[values]
    #             print(str(values[pt_i]))
    #             print(str(values[pt_i+1]))
    #             for fr_i in range()
    #
    # fragment_dict = DictList()
    # for usr in range(2):
    #     curr_usr='%03d' % usr
    #     frag_count=1
    #     for key,values in d.items():
    #         print(list(range(0,len(values)-1)))
    #         for pt_i in range(0,len(values)-1):
    #             if(values[pt_i][0]==curr_usr):
    #                 # print(pt_i)
    #
    #                 if  abs(values[pt_i][5] - values[pt_i + 1][5]) == 1:
    #                     # fragment_dict[key]={curr_usr:{frag_count:values[pt_i]}}
    #                     fragment_dict[(key,curr_usr,str(frag_count))]=values[pt_i]
    #                     # print(fragment_dict)
    #                     if(pt_i==max(range(len(values)-1))):
    #                         fragment_dict[(key, curr_usr, str(frag_count))] = values[pt_i+1]
    #                         # print(fragment_dict)
    #
    #                 else:
    #                     print(pt_i)
    #                     print("else")
    #                     # fragment_dict[key]={curr_usr:{frag_count:values[pt_i+1]}}
    #                     # fragment_dict[(key,curr_usr,str(frag_count))]=values[pt_i]
    #                     # print(fragment_dict)
    #                     frag_count=frag_count+1

    # print(fragment_dict[])


    # print(any(abs(values[i][5]-values[i + 1][5])==1 for i in range(len(values) - 1)))
            # if(any(abs(values[i+1][5]-values[i][5])==1 for i in range(len(values) - 1)) is False):
            #     print(str(values[i]))
            #     print(str(values[i+1]))


    # for key,values in d.items():
    #     print(key, values)
    #     print("Processing tile "+str(count))
    #     # print(type(d[key]))
    #     # print(d[key])
    #     # print(values)
    #     # for m,n in enumerate(d[key]):
    #     #     for user_id in n:
    #     #         print(user_id)
    #     # print(key,values)
    #     ls=set()
    #     # for x,y in itertools.combinations(values,2):
    #     #     u1,la1,lo1,d1,t1=x
    #     #     df_1 = d1 + " " + t1
    #     #
    #     #     u2,la2,lo2,d2,t2=y
    #     #
    #     #     df_2 = d2 + " " + t2
    #     #     timedelta = datetime.datetime.strptime(df_2, datetimeFormat) - datetime.datetime.strptime(df_1,datetimeFormat)
    #     #
    #     # #     if(u1!=u2 and d1==d2 and abs(timedelta.total_seconds())<=600):
    #     # #         # print("Contact Established between :")
    #     # #         # print(x)
    #     # #         # print(y)
    #     # #         ls.add((u1,u2))
    #     # # print("Tile with key "+key+" with tile num: "+str(count)+" has the following contacts")
    #     # # print(ls)
    #     # # count=count+1
    #     #
    #     # # print(d[key])
    #     # # for ele in d[key]:
    #     # #     u,d,t=ele
    #     # #     print(u)
    #     # #     print(d)
    #     # #     print(t)
    #     for ele in values:
    #             ls.add(ele[0])
    #     if(len(ls)>1):
    #         print("Tile with key " + key + " with tile num: " + str(count) + " has the following contacts")
    #         print(ls)
    #         finalList.append(ls)
    #     count=count+1
    # print("Final List of contacts")
    # print(finalList)
    # G = nx.Graph()
    user_loc = DictList()

    # count=0
    # finalList=[]
    # for key, values in d.items():
    #     # print(values)
    #     count = count + 1
    #     print(count)
    #     ls=set()
    #
    #     for x ,y in itertools.combinations(values,2):
    #         us1,lt1,ln1,dt1,tm1=x
    #         us2,lt2,ln2,dt2,tm2=y
    #         if(us1!=us2):
    #             con1,con2,dist=checkForOutliers(key,x,y)
    #             # ls.add((a,b))
    #             ltlist=[]
    #
    #             a, x1, y1, d1, t1 = con1
    #             b, x2, y2, d2, t2 = con2

                # with open('contacts_full_ds'+str(ds)+'_dt'+str(dt)+'.csv','a+') as fl:
                #     fl.write(a+","+x1+','+y1+','+d1+','+t1+","+b+","+x2+','+y2+','+d2+','+t2+','+str(dist)+','+str(dt)+','+key+"\n")

    #             user_loc[a]=[(x1,y1)]
    #             user_loc[b]= [(x2,y2)]
    #             if G.has_edge(a, b):
    #                 # we added this one before, just increase the weight by one
    #                 G[a][b]['weight'] += 1
    #             else:
    #                 # new edge. add with weight=1
    #                 G.add_edge(a, b, weight=1)
    #
    # pos = nx.circular_layout(G)
    # # nx.draw(G,with_labels=True, arrows=True, node_size=700)
    # nx.draw(G, pos, with_labels=True, arrows=True, node_size=700)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos,  with_labels=True, arrows=True, node_size=700,edge_labels=labels)
    # plt.show()
    #
    # #     if (len(ls) > 0):
    # #         print("Tile with key " + key + " with tile num: " + str(count) + " has the following contacts")
    # #         print(ls)
    # #         finalList.append(ls)
    # # print("Final list of possible contacts")
    # # print(finalList)
    # #
    # # with open("final_list_new2.txt",'a+') as d:
    # #     d.write(str(finalList))
    # latitude_list = []
    # longitude_list = []
    #
    # for key,values in user_loc.items():
    #     print(key)
    #     useravgloc={}
    #
    #     total=[sum(float(i) for i, j in values)/len(values),sum(float(j) for i, j in values)/len(values)]
    #     useravgloc[key]=total
    #     print(useravgloc)
    #     latitude_list.append(sum(float(i) for i, j in values) / len(values))
    #     longitude_list.append(sum(float(j) for i, j in values) / len(values))
    #
    # gmap2 = gmplot.GoogleMapPlotter.from_geocode("Beijing, China")
    #
    # gmap2.scatter(latitude_list, longitude_list, '# FF0000',
    #                   size=40, marker=False)
    #
    #     # Plot method Draw a line in
    #     # between given coordinates
    # gmap2.plot(latitude_list, longitude_list,
    #                'cornflowerblue', edge_width=2.5)
    #
    # gmap2.draw("C:\\Users\\user\\Desktop\\map13.html")


datetimeFormat = '%Y-%m-%d %H:%M:%S'
from datetime import timedelta


def distance(p1,p2):
    """Euclidean distance between two points."""
    # approximate radius of earth in km
    R = 6373.0
    x1,y1,d1,t1 = p1
    x2,y2,d2,t2 = p2
    #print(x1)
    # return hypot(x2 - x1, y2 - y1)
    lat1 = radians(float(x1))
    lon1 = radians(float(y1))
    lat2 = radians(float(x2))
    lon2 = radians(float(y2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c *1000
    return distance

outliers=[]
import datetime

def checkForOutliers(key,p1,p2):
    R = 6373.0
    u1,x1, y1, tmin1, tmax1 = p1
    u2,x2, y2, tmin2, tmax2 = p2
    # print(x1)
    # return hypot(x2 - x1, y2 - y1)
    lat1 = radians(float(x1))
    lon1 = radians(float(y1))
    lat2 = radians(float(x2))
    lon2 = radians(float(y2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000
    # return distance
    # print(distance)
    # ls=set()

    # df1 = d1 + " " + t1
    # df2 = d2 + " " + t2
    # timedelta = datetime.datetime.strptime(df2, datetimeFormat) - datetime.datetime.strptime(df1, datetimeFormat)

    if (u1 != u2 ):
        if(distance<=ds):
            # with open("outliers/outliers.txt _ "+str(key)+".txt",'a+') as o:
                # print("outlier found")
                # o.write(str(p1)+"---"+str(p2)+"-"+str(distance)+"---"+str(timedelta)+"\n")
            # ls.add((u1,u2))
            # return u1,u2
            return distance
        else:
            with open("exclusions/out_of_threshold_"+str(ds)+"_"+str(dt)+".txt",'a+') as ob:
                ob.write(str((key,p1,p2,distance))+"\n")

            print("out of bound")
            return -1









mapp()

