# letzter Stand, 29.04.21 13:09
'''
Konvertiert Datei highway_lines.csv aus FlexiGIS in ein Format, das von
geopandas gelesen werden kann
'''

import os
import geopandas as gpd

# Konstanten
WORKDIR = os.path.normpath('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/rivus-wechloy')
INPUT_DIR = os.path.join(WORKDIR, 'data/flexigis-data/fg-wechloy-raw')
RES_DIR = os.path.join(WORKDIR, 'data/flexigis-data/output')


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
