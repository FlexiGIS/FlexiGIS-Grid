#letzter Stand: 30.04.2021, 15:32
import os
import geopandas as gpd
import pandas as pd
import numpy as np

# Consts
WORKDIR = os.path.join('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/rivus-wechloy')
INPUT_DIR = os.path.join(WORKDIR, 'data/wechloy')
RES_DIR = os.path.join(WORKDIR, 'data/wechloy')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)
shp_reader = gpd.read_file
csv_reader = pd.read_csv

# IN
vertex_filename_abs = os.path.join(INPUT_DIR, 'vertex.shp')
sources_filename_abs = os.path.join(INPUT_DIR, 'sources.csv')

# OUT
vertex_w_source_filename_abs = os.path.join(INPUT_DIR, 'vertex_w_source.shp')

# DO
# read
vertex = shp_reader(vertex_filename_abs) # GeoDataFrame
sources = csv_reader(sources_filename_abs) # DataFrame

for commodity in ['Elec', 'Gas', 'Heat']:
# add generation of commodity
    try:
        commodity_generation = np.zeros(( len(vertex) ,)) # Initializing array of zeros
        commodity_generation[sources['Vertex']] = sources[ commodity ] # replacing zeros by generation at certain vertices

        vertex[ commodity ] = commodity_generation # adding column to GeoDataFrame
    except: # commodity is not available as column in input file
        pass

vertex
# write
vertex.sort_index()
vertex.to_file(vertex_w_source_filename_abs)