import DatabaseCompiler as DatComp
import StatisticsPlots as StatPlt
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import Mapping

parameter_file = "../1_Raw-Data/compilation_parameters.txt"
parameters = DatComp.read_parameters(parameter_file)
events, station_events = DatComp.compiler(parameters)
station_data = DatComp.StationData()

# Mapping.data_map_wide(events, station_data, parameters['filename'])
Mapping.data_map_hengill(events, station_data, parameters['filename'])
# StatPlt.TimeHist(events, parameters['filename'])
# StatPlt.MagHist(events, parameters['filename'])

