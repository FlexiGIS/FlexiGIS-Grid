# letzter Stand: 29.04.2021, 13:08
import os
import geopandas
import shapely
import rivus
from rivus.utils import pandashp as pdshp
from rivus.utils import shapelytools
from rivus.utils import skeletrontools

# Consts

WORKDIR = os.path.join('/Users/haukebents/Documents/Studium/Praktika/DLR ESY Oldb/FlexiGIS Netz Arbeit/rivus-wechloy')
#WORKDIR = os.path.join('/home/bent_ha/Documents/FlexiGIS-Netz-Praktikum/rivus-wechloy')
INPUT_DIR = os.path.join(WORKDIR, 'data/flexigis-data/output') # FlexiGIS-Streets ist Vorlage für rivus-Edgefile
RES_DIR = os.path.join(WORKDIR, 'data/testing')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)
EPSG_XY = 3857

# IN
streets_filename = 'streets.shp'
streets_filename_abs = os.path.join(INPUT_DIR, 'streets.shp')

# OUT
edge_apath = os.path.join(RES_DIR, 'edge.shp')
vertex_apath = os.path.join(RES_DIR, 'vertex.shp')

# DO
# read
streets = geopandas.read_file(streets_filename_abs)
streets = streets.to_crs(epsg=EPSG_XY)

# filter away roads by type
road_types = ['motorway', 'motorway_link', 'primary', 'primary_link',
              'secondary', 'secondary_link', 'tertiary', 'tertiary_link',
              'residential', 'living_street', 'service', 'unclassified']
streets = streets.rename(columns = {'highway' : 'type'}) # FlexiGIS-'highway' enthält rivus-type-Info
streets = streets[streets['type'].isin(road_types)]

# create skeleton from street network
skeleton = skeletrontools.skeletonize(streets,
                                      buffer_length = 60,
                                      dissolve_length = 30,
                                      simplify_length = 30)

# adjust skeleton removing short endings (??) and short lines
skeleton = shapelytools.one_linestring_per_intersection(skeleton)
skeleton = shapelytools.snappy_endings(skeleton, max_distance=10)
skeleton = shapelytools.one_linestring_per_intersection(skeleton)
skeleton = shapelytools.prune_short_lines(skeleton, min_length=5)

# convert back to GeoPandas and reproject back to geographic WGS 84 (EPSG:4326)
edge = geopandas.GeoDataFrame(geometry=skeleton, crs=streets.crs)
edge = edge.to_crs(epsg=4326)  # World Geodetic System (WGS84)
edge['Edge'] = edge.index

# derive vertex points
vertices = shapelytools.endpoints_from_lines(edge.geometry)
vertex = geopandas.GeoDataFrame(geometry=vertices, crs=edge.crs)
vertex['Vertex'] = vertex.index

pdshp.match_vertices_and_edges(vertex, edge)

# drop loops
edge = edge[~(edge['Vertex1'] == edge['Vertex2'])]

# if there are >1 edges that connect the same vertex pair, drop one of them
edge = edge.drop_duplicates(subset=['Vertex1', 'Vertex2'])

# write to file
edge.to_file(edge_apath)
vertex.to_file(vertex_apath)