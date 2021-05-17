#letzter Stand: 29.04.2021, 14:54
import os
import geopandas
import pandas
from rivus.utils import pandashp as pdshp

# Consts
#WORKDIR = os.path.join('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/FlexiNetz')
INPUT_DIR = os.path.join('data/wechloy')
RES_DIR = os.path.join('data/wechloy')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)
EPSG_CODE = 'epsg:3857'

# IN
edge_filename = 'edge.shp'
edge_filename_abs = os.path.join(INPUT_DIR, 'edge.shp')

building_filename = 'building_w_nearest.shp'
building_filename_abs = os.path.join(INPUT_DIR, 'building_w_nearest.shp')

# OUT
edge_w_demands_path = os.path.join(RES_DIR, 'edge_w_demands.shp')

# DO
# Create edge graph with grouped building demands.

# load buildings and sum by type and nearest edge ID
# 1. read shapefile to DataFrame (with special geometry column)
# 2. group DataFrame by columns 'nearest' (ID of nearest edge) and 'type'
#    (residential, commercial, industrial, other)
# 3. sum by group and unstack, i.e. convert secondary index 'type' to columns

buildings = pdshp.read_shp(building_filename_abs)
building_type_mapping = {
    'church': 'other',
    'farm': 'other',
    'hospital': 'residential',
    'hotel': 'commercial',
    'house': 'residential',
    'office': 'commercial',
    'retail': 'commercial',
    'school': 'commercial',
    'yes': 'other'}
buildings.replace(to_replace={'type': building_type_mapping}, inplace=True)
buildings_grouped = buildings.groupby(['nearest', 'type'])
total_area = buildings_grouped.sum()['area'].unstack()

# load edges (streets) and join with summed areas
# 1. read shapefile to DataFrame (with geometry column)
# 2. join DataFrame total_area on index (=ID)
# 3. fill missing values with 0
edge = pdshp.read_shp(edge_filename_abs)
edge = edge.set_index('Edge')
edge = edge.join(total_area)
edge = edge.fillna(0)

# write edge with aggregated demands
edge_gdf = geopandas.GeoDataFrame(edge, crs=EPSG_CODE)
edge_gdf.to_file(edge_w_demands_path)