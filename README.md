# FlexiNetz

The FlexiNetz scripts aim to perform a soft-coupling of the energy system models [**rivus**](https://github.com/tum-ens/rivus)
and the QGIS-Plugin [**FlexiGIS**](https://github.com/FlexiGIS/FlexiGIS-plugin) is performed. 

**rivus** is a [mixed integer linear programming](https://en.wikipedia.org/wiki/Integer_programming) optimisation model 
for capacity planning of energy infrastructure networks. Its name, latin for stream or canal, stems from its origin as a 
companion model for [urbs](https://github.com/tum-ens/urbs), an optimisation model for urban energy systems. The model 
has been first published in the dissertation of [Johannes Dorfner](https://github.com/ojdo) ["Open Source Modelling 
and Optimisation of Energy Infrastructure at Urban Scale"](http://nbn-resolving.de/urn/resolver.pl?urn:nbn:de:bvb:91-diss-20161206-1285570-1-6).

**FlexiGIS-plugin** is a graphical user interface (GUI) of the FlexiGIS-model including FlexiGIS-light. It extracts the 
geo-datasets of the urban energy infrastructure and simulates the electricity consumption in the respective case study. 
This plugin can be directly installed from the QGIS Plugin Manager within the QGIS Desktop.

## Features (TODO: Adjust text to fit FlexiNetz)

  * rivus is a mixed integer linear programming model for multi-commodity energy infrastructure networks systems with a 
    focus on high spatial resolution.
  * It finds the minimum cost energy infrastructure networks to satisfy a given energy distribution for possibly multiple 
    commodities (e.g. electricity, heating, cooling, ...).
  * Time is represented by a (small) set of weighted time steps that represent peak or typical loads  
  * Spatial data can be provided in form of shapefiles, while technical parameters can be edited in a spreadsheet.
  * The model itself is written using [Pyomo](https://software.sandia.gov/trac/coopr/wiki/Pyomo) and includes reporting 
    and plotting functionality.

## Installation

### Mac

1. Install [**miniforge3**](https://github.com/conda-forge/miniforge/releases). Choose the 64-bit installer if possible.

2. Clone [**TODO LINK: FlexiNetz**]() repository to your working directory
   
    ```
    (base)$ git clone <link_to_repo>
    ```

3. Create **conda** environment from environment.yml file via terminal
    
    i) Navigate to your working directory
   
    ```
    (base)$ cd path/to/working_directory
    ```

    ii) Install **conda** virtual environment from file
    
    ```
    (base)$ conda env create -f environment.yml
    ```
   
    iii) Activate environment

    ```
    (base)$ conda activate flexinetz
    ```

4. Install [**Skeletron package**](https://github.com/ojdo/Skeletron.git) into **flexinetz** environment using **pip**
    
    i) Clone repository and navigate into directory

    ```
    (flexinetz)$ git clone https://github.com/ojdo/Skeletron.git
    ```      

    ii) Navigate into directory and install package using pip
    
    ```
    (flexinetz)$ pip install -e .
    ```


## Documentation / Tutorials

  * [Official documentation](http://rivus.readthedocs.io/en/latest/)
  * List of helpful IPython notebooks on handling geographic input data:
    + [join data from building.shp and edge.shp](https://nbviewer.jupyter.org/gist/lnksz/6edcd0a877997e9365e808146e9b51fe)
    + [OSM street data to vertex.shp and edge.shp](https://nbviewer.jupyter.org/gist/lnksz/7977c4cff9c529ca137b67b6774c60d7)
    + [Square grid to vertex.shp and edge.shp](https://nbviewer.jupyter.org/gist/lnksz/bd8ce0a79e499479b61ea7b45d5c661d)
  * See repository-wiki for archive of interesting conversations, tips, and troubleshooting.
