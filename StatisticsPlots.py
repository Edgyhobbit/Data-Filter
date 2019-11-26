def TimeHist(events, name):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import datetime as dt
    events_time = list()
    events_id = list(events.keys())
    for event in events_id:
        events_time.append(events[event][0])

    hist_data = mdates.date2num(events_time)
    binwidth = mdates.num2timedelta(7)                                                              # dates
    bins = mdates.drange(dt.datetime(2016,11,25,0,0,0,0),dt.datetime(2019,11,15,0,0,0,0),binwidth)
    color = 'lightblue'
    edgecolor = 'black'
    fig = plt.figure(figsize=(13,4))
    ax = plt.subplot(111)
    ax.tick_params(direction='in', labelbottom=True)
    ax.hist(hist_data, bins=bins, color=color, edgecolor=edgecolor)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    filename = name + "Time_histogram.png"
    plt.show(block=False)
    plt.pause(5)
    plt.savefig(filename)
    plt.close()


def MagHist(events, name):
    import numpy as np
    import matplotlib.pyplot as plt
    events_mag = list()
    events_id = list(events.keys())
    for event in events_id:
        events_mag.append(events[event][7])
    data = np.asarray(events_mag)
    color = 'green'
    edgecolor = 'black'
    fig2 = plt.figure(figsize=(13,7))
    ax2 = plt.subplot(111)
    binwidth = 0.125
    xlimpos= np.ceil(data.max())
    xlimneg= np.floor(data.min())
    xbins = np.arange(xlimneg, xlimpos + binwidth, binwidth)
    ax2.hist(data, bins=xbins, log=True,color=color,edgecolor=edgecolor)
    filename = name + "_Magnitude_histogram.png"
    plt.show(block=False)
    plt.pause(5)
    plt.savefig(filename)
    plt.close()

def MagHist2(events, name):
    import numpy as np
    import matplotlib.pyplot as plt
    events_mag = list()
    events_id = list(events.keys())
    for event in events_id:
        events_mag.append(events[event][4])
    data = np.asarray(events_mag)
    color = 'green'
    edgecolor = 'black'
    fig2 = plt.figure(figsize=(13,7))
    ax2 = plt.subplot(111)
    binwidth = 0.125
    xlimpos= np.ceil(data.max())
    xlimneg= np.floor(data.min())
    xbins = np.arange(xlimneg, xlimpos + binwidth, binwidth)
    ax2.hist(data, bins=xbins, log=True,color=color,edgecolor=edgecolor)
    filename = name + "_Magnitude_histogram.png"
    plt.show(block=False)
    plt.pause(5)
    plt.savefig(filename)
    plt.close()