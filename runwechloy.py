import matplotlib.pyplot as plt
import os
import pandas as pd
from rivus.utils import pandashp as pdshp
from rivus.main import rivus
try:
    import pyomo.environ
    from pyomo.opt.base import SolverFactory
    PYOMO3 = False
except ImportError:
    import coopr.environ
    from coopr.opt.base import SolverFactory
    PYOMO3 = True


# IN
base_directory = os.path.join('data/wechloy')
building_shapefile = os.path.join(base_directory, 'building_w_nearest')
edge_shapefile = os.path.join(base_directory, 'edge_w_demands')
vertex_shapefile = os.path.join(base_directory, 'vertex_w_source')
data_spreadsheet = os.path.join(base_directory, 'data-flexigis.xlsx')

# OUT
result_dir = os.path.join(base_directory, 'results')
# create result directory if not existing already
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


# scenarios

def scenario_base(data, vertex, edge):
    """Base scenario: change nothing-"""
    return data, vertex, edge
    
def scenario_renovation(data, vertex, edge):
    """Renovation: reduce heat demand of residential/other by 50%"""
    area_demand = data['area_demand']
    area_demand.ix[('residential', 'Heat'), 'peak'] *= 0.5
    area_demand.ix[('other', 'Heat'), 'peak'] *= 0.5
    return data, vertex, edge

scenarios = [
    scenario_base]#,
    #scenario_renovation]

# solver

def setup_solver(optim):
    """Change solver options to custom values."""
    if optim.name == 'cbc':
        #optim.set_options('integerT=1e-06')
        #optim.set_options('dualT=1e-05')
        #optim.set_options('primalT=1e-07')
        #optim.set_options('zeroT=1e-25')
        #optim.set_options('preT=1e-07')
        optim.set_options('sec=1200')  # seconds
    else:
        print("Warning from setup_solver: no options set for solver "
            "'{}'!".format(optim.name))
    return optim

# helper functions
        
def run_scenario(scenario):
    # scenario name
    sce = scenario.__name__
    sce_nice_name = sce.replace('_', ' ').title()
    
    # prepare input data 
    data = rivus.read_excel(data_spreadsheet)
    vertex = pdshp.read_shp(vertex_shapefile)
    edge = pdshp.read_shp(edge_shapefile)
    
    # apply scenario function to input data
    data, vertex, edge = scenario(data, vertex, edge)
    
    # create & solve model
    prob = rivus.create_model(data, vertex, edge)
    if PYOMO3:
        prob = prob.create() # no longer needed in Pyomo 4+
    optim = SolverFactory('cbc')
    optim = setup_solver(optim)
    result = optim.solve(prob, tee=True)
    if PYOMO3:
        prob.load(result) # no longer needed in Pyomo 4+

    
    # report    
    rivus.report(prob, os.path.join(result_dir, 'report.xlsx'))
    
    # plots
    for com, plot_type in [('Elec', 'caps'), ('Heat', 'caps'), ('Gas', 'caps'),
                           ('Elec', 'peak'), ('Heat', 'peak')]:
        
        # two plot variants
        for plot_annotations in [False, True]:
            # create plot
            fig = rivus.plot(prob, com, mapscale=False, tick_labels=False, 
                             plot_demand=(plot_type == 'peak'),
                             annotations=plot_annotations)
            plt.title('')
            
            # save to file
            for ext, transp in [('png', True), ('png', False), ('pdf', True)]:
                transp_str = ('-transp' if transp and ext != 'pdf' else '')
                annote_str = ('-annote' if plot_annotations else '')
                
                # determine figure filename from scenario name, plot type, 
                # commodity, transparency, annotations and extension
                fig_filename = '{}-{}-{}{}{}.{}'.format(
                    sce, plot_type, com, transp_str, annote_str, ext) 
                fig_filename = os.path.join(result_dir, fig_filename)
                fig.savefig(fig_filename, dpi=300, bbox_inches='tight', 
                            transparent=transp)
                
    return prob

           
if __name__ == '__main__':
    for scenario in scenarios:
        prob = run_scenario(scenario)
