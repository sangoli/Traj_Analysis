import json

from math import sin, cos, sqrt, atan2,radians

import itertools

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

def checkForOutliers(key,p1,p2):
    R = 6373.0
    u1,x1, y1, tmin1, tmax1 = p1
    u2,x2, y2, tmin2, tmax2 = p2
    lat1 = radians(float(x1))
    lon1 = radians(float(y1))
    lat2 = radians(float(x2))
    lon2 = radians(float(y2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000
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

def create_fragments(load_dict,ds,dt):
    fragment_dict = DictList()

    print("Creating Fragments")
    for key, values in load_dict.items():
        frag_count = 1
        for pt_i in range(0, len(values) - 1):
            curr_usr = values[pt_i][0]
            # print(pt_i)
            if abs(values[pt_i][5] - values[pt_i + 1][5]) == 1:
                fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i]]
                if (pt_i == max(range(len(values) - 1))):
                    fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i + 1]]
            else:

                fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i]]
                frag_count = frag_count + 1
                # print("Incrementing fragment")
                continue

    #
    fg = fragment_dict #make a copy
    final_frag = DictList()
    for k1, v1 in fg.items():
        if (len(v1) > 0):
            # print("key")
            # print(k1)
            # print(v1)
            # print(len(v1))
            lat_avg = sum([float(pair[1]) for pair in v1]) / len(v1)
            lng_avg = sum([float(pair[2]) for pair in v1]) / len(v1)
            max_time = max([float(pair[6]) for pair in v1])
            min_time = min([float(pair[6]) for pair in v1])

            # print(lat_avg,lng_avg,max_time)
            final_frag[k1.split('&')[0]] = [(k1.split('&')[1], lat_avg, lng_avg, min_time, max_time)]
    # print(final_frag)
    print("Writing CSV")
    with open("consolidated_csv/fragments_ds" + str(ds) + "_dt" + str(dt) + ".csv", 'a+') as wr: #creating column names for csv
        wr.write(
            "UserA,LatA,LngA,Min_time_UserA,Max_time_UserA,UserB,LatB,LngB,Min_time_UserB,Max_time_UserB,Distance_apart(m),Interaction_time(ms),Tile_key\n")
    interaction_time = 0

    for ft, vt in final_frag.items():
        if (len(vt) > 1):

            for x, y in itertools.combinations(vt, 2):
                u1, la1, lo1, t1_min, t1_max = x

                u2, la2, lo2, t2_min, t2_max = y

                if (u1 != u2):
                    print("EUREKA")
                    if t1_max > t2_max and t2_min > t1_min:
                        interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                    elif t1_max < t2_max and t2_min < t1_min:
                        interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                    elif t1_max > t2_max and t1_min > t2_min:
                        interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                    elif t2_max > t1_max and t2_min > t2_min:
                        interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                    check = checkForOutliers(ft, x, y) #making one final check for distance threshold satisfaction
                    if check is not -1:
                        with open("consolidated_csv/fragments_ds" + str(ds) + "_dt" + str(dt) + ".csv", 'a+') as fn: # appending to csv
                            fn.write(u1 + "," + str(la1) + "," + str(lo1) + "," + str(t1_min) + "," + str(
                                t1_max) + "," + u2 + "," + str(la2) + "," + str(lo2) + "," + str(t2_min) + "," + str(
                                t2_max) + ","
                                     + str(checkForOutliers(ft, x, y)) + "," + str(interaction_time) + "," + ft + "\n")






#set ds and dt fot creating fragments
ds=100
dt=300
with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt") as f:
        load_dict = json.load(f)
create_fragments(load_dict,ds,dt)
