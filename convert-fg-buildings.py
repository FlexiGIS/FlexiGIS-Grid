# letzter Stand 29.04.21, 13:08
'''
# Kombiniere die shapefiles, die FlexiGIS zur Verfügung stellt. Der Name der Shapefiles
# gibt den Typen der Gebäude wieder.


# So habe ich ich die Teilfunktionen erarbeitet

res = pd.DataFrame(data={
    'osmid' : np.array([1, 2, 3, 4]),
    'building' : np.array(list('xyxz')),
    'geometry' : np.array(['g1', 'g2' , 'g3', 'g4']),
    'area' : np.array([24, 12, 9, 49])
})

agri = pd.DataFrame(data={
    'osmid' : np.array([9, 8, 7, 6]),
    'building' : np.array(list('hlkr')),
    'geometry' : np.array(['g9', 'g8' , 'g7', 'g6']),
    'area' : np.array([121, 380, 70, 1218])
})

# Dieser Schritt ist für die echten Shapefiles nicht notwendig, 
# die Spalte 'category' enthält bereits den 'type'
agri['type'] = np.full((len(agri),), 'agricultural')
res['type'] = np.full((len(res),), 'residential')

combined = pd.concat([res, agri], ignore_index=True)
print(combined.head(8))
'''

import os
import geopandas as gpd
import pandas as pd

# Konstanten
WORKDIR = os.path.normpath('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/rivus-wechloy')
INPUT_DIR = os.path.join(WORKDIR, 'data/flexigis-data/fg-wechloy-raw')
RES_DIR = os.path.join(WORKDIR, 'data/flexigis-data/output')


shp_reader = gpd.read_file
def csv_reader(filename, crs_code='epsg:3857', to_gdf=False):
    from shapely import wkt
    import pandas as pd

    df = pd.read_csv(filename)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    if to_gdf:
        gdf = gpd.GeoDataFrame(df, crs=crs_code)
        return gdf
    else:
        return df

# Input
types = ['agricultural', 'commercial', 'educational', 'industrial', 'residential'] # Gebäudetypen

# Output
out_filename = os.path.join(RES_DIR, 'building.shp') # Dateiname für rivus. building enthält kombinierte Gebäudetypen

# DO

buildings_df = pd.DataFrame() # Initialisierung des DataFrames
for type in types:
    input_name = os.path.join(INPUT_DIR, type + '.csv')
    building_type = csv_reader( input_name, to_gdf=False )
    building_type = building_type.rename(columns = {'category' : 'type'}) # 'category' enthält die Typebeschreibung
    buildings_df = pd.concat([buildings_df, building_type], ignore_index=True) # ähnlich wie np.append(array, other)

buildings_gdf = gpd.GeoDataFrame(buildings_df, crs='epsg:3857') # Konvertieren in GeoDataFrame

buildings_gdf.to_file(out_filename) # Speichern
