# letzter Stand, 17.05.21 12:53
'''
Konvertiert Datei highway_lines.csv aus FlexiGIS in ein Format, das von
geopandas gelesen werden kann
'''

import os
import geopandas as gpd

# Konstanten
#WORKDIR = os.path.join('/Users/haukebents/Documents/Studium/Praktika/DLR ESY Oldb/FlexiGIS Netz Arbeit/rivus-wechloy') # Hauke Mac
WORKDIR = os.path.normpath('/') # DLR Linux
INPUT_DIR = os.path.join('data/flexigis-input/fg-wechloy-raw')
RES_DIR = os.path.join('data/flexigis-input/output')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)

shp_reader = gpd.read_file
def csv_reader(filename, crs_code='epsg:3857', to_gdf=False):
    from shapely import wkt
    import pandas as pd
    import geopandas as gpd

    df = pd.read_csv(filename)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    if to_gdf:
        gdf = gpd.GeoDataFrame(df, crs=crs_code)
        return gdf
    else:
        return df

# Input
in_filename = os.path.join(INPUT_DIR, 'highway_lines.csv')

# Output
out_filename = os.path.join(RES_DIR, 'streets.shp')

# DO
streets = csv_reader(in_filename, to_gdf=True)
streets.to_file(out_filename)
