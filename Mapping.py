def world_map():
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    world_image_path = "D:/Cartopy/natural_earth_50/NE1_50M_SR_W/NE1_50M_SR_W.tif"
    world_image = plt.imread(world_image_path)
    fig = plt.figure(figsize=(10, 8))
    pc = ccrs.PlateCarree()
    img_extent = list(pc.x_limits) + list(pc.y_limits)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_global()
    ax.imshow(world_image, extent=img_extent, transform=pc, origin='upper')
    ax.coastlines(resolution = '50m')
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.gridlines(draw_labels=True,color='b', alpha=0.2,linestyle='--')
    plt.show(block=False)
    plt.pause(3)
    plt.savefig("world_map.png")
    plt.close()


def world_map2():
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    world_image_path = "D:/Cartopy/natural_earth_50/NE1_50M_SR_W/NE1_50M_SR_W.tif"
    fig = plt.figure(figsize=(10, 8))
    world_image = plt.imread(world_image_path)
    pc = ccrs.PlateCarree()
    img_extent = list(pc.x_limits) + list(pc.y_limits)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_global()
    ax.imshow(world_image, extent=img_extent, transform=pc, origin='upper')
    ax.coastlines(resolution = '50m')
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.gridlines(draw_labels=True,color='b', alpha=0.2,linestyle='--')
    ax.set_extent((-90, 50, -10, 75), crs=ccrs.PlateCarree())
    plt.show(block=False)
    plt.pause(3)
    plt.savefig("world_map2.png")
    plt.close()


def iceland_map():
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt
    stamen_terrain = cimgt.Stamen('terrain')
    fig = plt.figure(figsize=(13, 9))
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([-24.5, -13, 63, 67], crs=ccrs.Geodetic())
    ax.add_image(stamen_terrain, 7)
    ax.gridlines(draw_labels=True,color='b', alpha=0.2,linestyle='--')
    plt.show(block=False)
    plt.pause(5)
    plt.savefig("iceland.png")
    plt.close()


def data_map_wide(events, station_data, name_):
    from functions import query_yes_no
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt
    from matplotlib.transforms import offset_copy
    filename=name_+ "_wide_view"
    events_ids = events.keys()
    event_lon = list()
    event_lat = list()
    event_mag = list()
    event_depth = list()
    station_lon = list()
    station_lat = list()
    station_names = station_data.keys()
    for station in station_names:
        station_lon.append(station_data[station][0])
        station_lat.append(station_data[station][1])
    for i_id in events_ids:
        event_lon.append(events[i_id][2])
        event_lat.append(events[i_id][1])
        event_mag.append(events[i_id][7])
        event_depth.append(events[i_id][3])
    s = list()
    for mag in event_mag:
        s.append((mag + 3)**2)

    stamen_terrain = cimgt.Stamen('terrain')
    fig1 = plt.figure(figsize=(16, 8))
    ax = fig1.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([-21.9, -19.8, 63.8, 64.25], crs=ccrs.Geodetic())
    ax.add_image(stamen_terrain, 10)
    ax.gridlines(draw_labels=True,color='b', alpha=0.2,linestyle='--')
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    map1 = ax.scatter(event_lon, event_lat, s, c=event_depth, transform=ccrs.PlateCarree(),label= 'Events', edgecolor='black')
    fig1.colorbar(map1, fraction=0.046, pad=0.04)
    flag1 = query_yes_no("Wanna show the stations' names? (WIDE)", default='yes')
    if flag1:
        filename += "_w-StationNames"
        i = 0
        text_transform = offset_copy(geodetic_transform, units='dots', x=-12)
        x_space = 0.001
        y_space = 0.001
        for name in station_data.keys():
            ax.text(station_lon[i]+x_space, station_lat[i]+y_space, name, transform=text_transform, fontsize=10,
                    verticalalignment='center', horizontalalignment='right',
                    bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))
            i += 1

    ax.scatter(station_lon, station_lat, s=50, transform=ccrs.PlateCarree(),label= 'stations',marker="v", edgecolors='black',facecolor='black')
    ax.legend
    filename += ".png"
    plt.show(block=False)
    plt.pause(8)
    plt.savefig(filename)
    plt.close()


def data_map_hengill(events, station_data, name_):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt
    from functions import query_yes_no
    from matplotlib.transforms import offset_copy
    filename = name_ + "_hengill_view"
    events_ids = events.keys()
    event_lon = list()
    event_lat = list()
    event_mag = list()
    event_depth = list()
    station_lon = list()
    station_lat = list()
    station_names = station_data.keys()
    for station in station_names:
        station_lon.append(station_data[station][0])
        station_lat.append(station_data[station][1])
    for i_id in events_ids:
        event_lon.append(events[i_id][2])
        event_lat.append(events[i_id][1])
        event_mag.append(events[i_id][7])
        event_depth.append(events[i_id][3])
    s = list()
    for mag in event_mag:
        s.append((mag + 3)**2)

    stamen_terrain = cimgt.Stamen('terrain')
    fig1 = plt.figure(figsize=(16, 16))
    ax = fig1.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([-21.6, -21, 63.89, 64.15], crs=ccrs.Geodetic())
    ax.add_image(stamen_terrain, 12)
    ax.gridlines(draw_labels=True,color='b', alpha=0.2,linestyle='--')
    map1 = ax.scatter(event_lon, event_lat, s, c=event_depth, transform=ccrs.PlateCarree(),label= 'Events')
    fig1.colorbar(map1, fraction=0.046, pad=0.08)
    ax.scatter(station_lon, station_lat, s=50, transform=ccrs.PlateCarree(),label= 'stations',marker="v", edgecolors='black',facecolor='black')
    flag1 = query_yes_no("Wanna show the stations' names? (Hengill)", default='yes')
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    if flag1:
        filename += "_w-StationNames"
        i = 0
        text_transform = offset_copy(geodetic_transform, units='dots', x=-12)
        x_space = 0.001
        y_space = 0.001
        for name in station_data.keys():
            ax.text(station_lon[i]+x_space, station_lat[i]+y_space, name, transform=text_transform, fontsize=10,
                    verticalalignment='center', horizontalalignment='right',
                    bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))
            i += 1
    filename += ".png"
    ax.legend
    # plt.show(block=False)
    # plt.pause(8)
    # plt.savefig(filename)
    # plt.close()
    plt.show()