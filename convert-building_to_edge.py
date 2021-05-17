# letzter Stand, 17.05.21 12:53
import geopandas
import pandas as pd
import rivus
from rivus.utils import pandashp as pdshp
import shutil
import os

# Consts
WORKDIR = os.path.join('/Users/haukebents/Documents/Studium/Praktika/DLR ESY Oldb/FlexiGIS Netz Arbeit/rivus-wechloy') # Hauke Mac
#WORKDIR = os.path.join('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/rivus-wechloy') # DLR Linux
RES_DIR = os.path.join(WORKDIR, 'data')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)
EPSG_XY = 3857

# IN
buildings_apath = os.path.join(WORKDIR, 'data/flexigis-input/output', 'building.shp')
edge_apath = os.path.join(WORKDIR, 'results', 'edge.shp')

# OUT
to_edge_apath = os.path.join(RES_DIR, 'to_edge.shp')
buildings_mapped_apath = os.path.join(RES_DIR, 'building_w_nearest.shp')

# DO
# read
buildings = geopandas.read_file(buildings_apath)
edge = geopandas.read_file(edge_apath)

buildings = buildings.to_crs(epsg=EPSG_XY)
edge = edge.to_crs(epsg=EPSG_XY)

# find closest edge
to_edge = pdshp.find_closest_edge(buildings, edge, to_attr='Edge')
to_edge = geopandas.GeoDataFrame(to_edge)
to_edge.crs = edge.crs.copy()

# reproject back to geographic WGS 84 (EPSG:4326)
buildings = buildings.to_crs(epsg=4326)
edge = edge.to_crs(epsg=4326)
to_edge = to_edge.to_crs(epsg=4326)

# write to file
to_edge.to_file(to_edge_apath)
buildings.to_file(buildings_mapped_apath)