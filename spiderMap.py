import pandas as pd
import geopandas as gpd
import os

os.chdir(r'c:\users\brenn\documents\projects\HopSkipJump')

gdf = gpd.read_file('Breweries/TorontoBreweries')
bike_mat = pd.read_csv('Breweries/toronto_bike.csv')
bike_mat.rename(columns = {'travel_time_p50' : 'bike'}, inplace = True)

walk_mat = pd.read_csv('Breweries/toronto_walk.csv')
walk_mat.rename(columns = {'travel_time_p50' : 'walk'}, inplace = True)

tran_mat = pd.read_csv('Breweries/toronto_transit.csv')
tran_mat.rename(columns = {'travel_time_p50' : 'transit'}, inplace = True)

for df in [bike_mat, walk_mat, tran_mat]:
    df.drop(columns = 'Unnamed: 0', inplace = True)

mat = walk_mat.merge(bike_mat, on = ['from_id', 'to_id'], how = 'outer').merge(tran_mat, on = ['from_id', 'to_id'], how = 'outer')

gdf.to_file('SpiderMap/brew.geojson', driver = 'GeoJSON')

mdf = gdf.merge(mat, left_on = 'id', right_on = 'to_id', how = 'right')
mdf.to_file('SpiderMap/matrix.geojson', driver = 'GeoJSON')

# number = False
# distance = 10
#
#
# mat.sort_values('travel_time_p50', ascending = True, inplace = True)
#
# if distance:
#     mat.query('travel_time_p50 <= @distance', inplace = True)
#
# if number:
#     mat.groupby('from_id').to_id.head(number)
#
# # func = lambda x: x.tolist()
# # lm = mat.groupby('from_id').agg({'to_id' : func}).reset_index()
#
# # gdf['popup'] = gdf.apply(lambda r: '<p>{name}</p>\n<p>{web}</p>'.format(name = r.name, web = r.web), axis = 1)
#
# content = ["var mat = {"]
# for idx, val in lm.iterrows():
#     fid = val['from_id']
#     tid = val['to_id']
#
#     s = f'"{fid}": {tid},\n'
#     content.append(s)
#
# content.append("}")
#
#
#
# with open('SpiderMap/matrix.js', 'w') as file:
#     file.writelines(content)