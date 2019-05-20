import pandas as pd
import folium

from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime

from datetime import date


#change file name here
filename='consolidated_csv/fragments_ds1000_dt1200.csv'
df = pd.read_csv(filename)
df.info()

# df.Max_time_UserA = pd.to_datetime(df.Max_time_UserA).
# df.Max_time_UserA=pd.to_datetime(df['Max_time_UserA'],).apply(lambda x: x.date())
# df['date']=pd.to_datetime(df['Max_time_UserA'],unit='s').date()

df['Tile_key ']= df['Tile_key '].astype(str)
#creating a column for just date from the Tile_key
df['date_from_key']=df['Tile_key '].apply(lambda x: x.split('_')[2])
df.date_from_key = df.date_from_key.astype(float)
df['date_from_key']=pd.to_datetime(df['date_from_key'],unit='s')




df['just_date']=pd.to_datetime(df['date_from_key'],unit='s').dt.date

#other useful columns for future use
df['Max_time_UserA']=pd.to_datetime(df['Max_time_UserA'],unit='s')
#UserA
df['month'] = df.Max_time_UserA.apply(lambda x: x.month)
df['week'] = df.Max_time_UserA.apply(lambda x: x.week)
df['day'] = df.Max_time_UserA.apply(lambda x: x.day)
df['hour'] = df.Max_time_UserA.apply(lambda x: x.hour)

# df['just_date'] = (df['Max_time_UserA'].dt.date)

# df.just_date = df.just_date.astype(str)
# print(df['date_from_key'])
# print(df['month'])
# print(df['day'])
# print(df['week'])
# print(df['hour'])
print(df['just_date'])

df.info()

print("here")
print(df['date_from_key'])


df['Avg_Lat'] = df[['LatA', 'LatB']].mean(axis=1)
df['Avg_Lng'] = df[['LngA', 'LngB']].mean(axis=1)


print(df[['LatA','LatB','Avg_Lat','LngA','LngB','Avg_Lng','Distance_apart(m)']])
def generateBaseMap(default_location=[39.913818, 116.363625], default_zoom_start=12):
    # base_map = folium.Map(location=default_location, tiles='http://{s}.tiles.mapbox.com/v3/{{ API_key }}/{z}/{x}/{y}.png',
    #                       API_key='xxx.xxx.xxx',
    #                       control_scale=True,
    #                       attr='XXX Mapbox Attribution',
    #                       zoom_start=default_zoom_start)

    # base_map=folium.Map(location=[45.5236, -122.6750],
    #            tiles='Mapbox',
    #            API_key='pk.eyJ1Ijoic2FudG9zaGdvbGkiLCJhIjoiY2p2MnRma20yMjh4cDQ0bWYxejc2ejVlcSJ9.ZuPPlyxSXQ511rvFCHl5mw')
    # return base_map

    map_mapbox_custo = folium.Map(
        location=default_location,
        zoom_start=default_zoom_start,
        tiles='https://api.mapbox.com/v4/mapbox.run-bike-hike/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2FudG9zaGdvbGkiLCJhIjoiY2p2MnRma20yMjh4cDQ0bWYxejc2ejVlcSJ9.ZuPPlyxSXQ511rvFCHl5mw',attr='helloo')
    return map_mapbox_custo

# basemap=generateBaseMap()

# basemap.save('foli1.html')

# df_copy = df[df.Max_time_UserA=='2009-06-14'].copy()

# curr_date=pd.Timestamp(date(2009,4,13)).date()
# print(df.just_date['2009-04-11'])

def create_visual(curr_date):
    print("Creating visualixation for  "+str(curr_date))
    y,m,d=curr_date
    str_date=str(y)+'-'+str(m)+'-'+str(d)
    df_copy=df[df['date_from_key'].dt.date == pd.Timestamp(date(y,m,d)).date()].copy() #y-m-d
    df_copy['count'] = 1

    base_map_general = generateBaseMap(default_zoom_start=11)
    HeatMap(data=df_copy[['Avg_Lat', 'Avg_Lng', 'count']].groupby(['Avg_Lat', 'Avg_Lng']).sum().reset_index().values.tolist(), radius=12, max_zoom=11,min_opacity=0.5).add_to(base_map_general)
    # base_map_general.save('heatmapsbydate/foli1_heat_general_'+filename+'.html')

    print(df_copy.info())
    df_hour_list = []
    for hour in df_copy.hour.sort_values().unique():
        df_hour_list.append(df_copy.loc[df_copy.hour == hour, ['Avg_Lat', 'Avg_Lng', 'count']].groupby(['Avg_Lat', 'Avg_Lng']).sum().reset_index().values.tolist())
    # print(df_hour_list)
    base_map = generateBaseMap(default_zoom_start=11)
    HeatMapWithTime(df_hour_list, radius=5, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)
    base_map.save('heatmapsbydate/foli1_heat_time_'+str_date+'_'+str(filename.split('/')[1])+'.html')



def create_general_visual(filename):
    df_copy = df.copy()  # y-m-d
    df_copy['count'] = 1

    base_map_general = generateBaseMap(default_zoom_start=11)
    HeatMap(data=df_copy[['Avg_Lat', 'Avg_Lng', 'count']].groupby(
        ['Avg_Lat', 'Avg_Lng']).sum().reset_index().values.tolist(), radius=10, max_zoom=11, min_opacity=0.3).add_to(base_map_general)
    base_map_general.save('heatmapsbydate/foli1_heat_general_'+str(filename.split('/')[1])+'.html')


#call required dates and generate hourly heatmaps
curr_dates_list=[(2009,4,11),(2009,4,12),(2009,4,13),(2009,4,19)]

for cd in curr_dates_list:
        create_visual(cd)

#create a general heatmap for the file
create_general_visual(filename)