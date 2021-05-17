'''
This file is used to test the rivus-package and its virtual environment.
The script is mainly based on runmin.py from https://github.com/tum-ens/rivus

DO:
 1. Activate conda virtual environment '$ conda activate flexinetz'
 2. Execute program 'python test-runmin.py'

--------------
Input:
 - spatial data:
    building.shp, edge.shp and vertex.shp
 - non-spatial data:
    data.xlsx

Output:
 - report.xlsx containing optimized costs, transport and process capacities
 - maps displaying line peak capacities of electricity, heat and gas network
'''

import pyomo.environ
from pyomo.opt.base import SolverFactory

import matplotlib.pyplot as plt
import os
import pandas as pd
from rivus.utils import pandashp as pdshp
from rivus.main import rivus

# INPUT
base_directory = os.path.join('data', 'mnl')
building_shapefile = os.path.join(base_directory, 'building')
edge_shapefile = os.path.join(base_directory, 'edge')
vertex_shapefile = os.path.join(base_directory, 'vertex')
data_spreadsheet = os.path.join(base_directory, 'data.xlsx')

# OUTPUT
result_dir = os.path.join('data', 'mnl', 'results')
# create result directory if not existing already
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# DO

# load buildings and sum by type and nearest edge ID
# 1. read shapefile to DataFrame (with special geometry column)
# 2. group DataFrame by columns 'nearest' (ID of nearest edge) and 'type'
#    (residential, commercial, industrial, other)
# 3. sum by group and unstack, i.e. convert secondary index 'type' to columns
buildings = pdshp.read_shp(building_shapefile)
buildings_grouped = buildings.groupby(['nearest', 'type'])
total_area = buildings_grouped.sum()['total_area'].unstack()


# load edges (streets) and join with summed areas 
# 1. read shapefile to DataFrame (with geometry column)
# 2. join DataFrame total_area on index (=ID)
# 3. fill missing values with 0
edge = pdshp.read_shp(edge_shapefile)
edge = edge.set_index('Edge')
edge = edge.join(total_area)
edge = edge.fillna(0)
    
# load nodes
vertex = pdshp.read_shp(vertex_shapefile)

# load spreadsheet data
data = rivus.read_excel(data_spreadsheet)

# create and solve model
prob = rivus.create_model(data, vertex, edge)
solver = SolverFactory('cbc')

result = solver.solve(prob, tee=True)

# load results
costs, Pmax, Kappa_hub, Kappa_process = rivus.get_constants(prob)
source, flows, hub_io, proc_io, proc_tau = rivus.get_timeseries(prob)
    
rivus.save(prob, os.path.join(result_dir, 'prob.pgz'))
rivus.report(prob, os.path.join(result_dir, 'report.xlsx'))


# plot all caps (and demands if existing)
for com, plot_type in [('Elec', 'caps'), ('Heat', 'caps'), ('Gas', 'caps'),
                       ('Elec', 'peak'), ('Heat', 'peak')]:
    
    # create plot
    fig = rivus.plot(prob, com, mapscale=False, tick_labels=False,
                     plot_demand=(plot_type == 'peak'),
                     buildings=(building_shapefile, True))
    plt.title('')
    # save to file
    for ext in ['png', 'pdf']:
            
        # determine figure filename from plot type, commodity and extension
        fig_filename = os.path.join(
            result_dir, '{}-{}.{}').format(plot_type, com, ext)
        fig.savefig(fig_filename, dpi=300, bbox_inches='tight', 
                    transparent=(ext=='pdf'))