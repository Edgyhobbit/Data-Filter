import DatabaseCompiler as DatComp
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt
import os


parameter_file = "../1_Raw-Data/compilation_parameters.txt"
parameters = DatComp.read_parameters(parameter_file)
events, station_events = DatComp.compiler(parameters)
station_data = DatComp.StationData()

stations_names = list(station_events.keys())
# Histogram parameters
binwidth = mdates.num2timedelta(7)
bins = mdates.drange(dt.datetime(2016,11,25,0,0,0,0),dt.datetime(2019,11,15,0,0,0,0),binwidth)
color = 'lightblue'
edgecolor = 'black'

for station in stations_names:
    title1=station
    data1=list()
    for event in station_events[station]:
        data1.append(mdates.date2num(event[0]))
    fig = plt.figure(figsize=(10,4))
    ax = plt.subplot(111)
    ax.set_title(station)
    ax.tick_params(direction='in', labelbottom=True)
    ax.hist(data1, bins=bins, color=color, edgecolor=edgecolor)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    strFile="../1_Raw-Data/stations/"+station+".png"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)
    plt.close()