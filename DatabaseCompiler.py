# Read the parrameters file for compilation
def read_parameters(filepath):
    # Loads the parameters and filters for the compilation into a dictionary
    print("#### Reading Parameters File ####")
    from numpy import genfromtxt
    select_par = genfromtxt(filepath, delimiter=':', dtype=str, comments='#')
    par_dic = {}
    for i in select_par:
        try:
            par_dic[i[0].strip()] = float(i[1])
        except ValueError:
            par_dic[i[0].strip()] = i[1].strip()
    print("#### Done! ####")
    return par_dic

# Compile the database into variables
def Primary_Select(par_dic):
    import os
    import datetime as dt
    min_lat = float(par_dic['min_lat'])
    max_lat = float(par_dic['max_lat'])
    min_lon = float(par_dic['min_lon'])
    max_lon = float(par_dic['max_lon'])
    max_dep = float(par_dic['max_depth'])
    max_gap = float(par_dic['max_GAP'])
    max_rms = float(par_dic['max_RMS'])
    min_mag = float(par_dic['min_mag'])
    primary_events = {}
    primary_events_ids = list()
    print("#### Selecting primary valid events ####")
    in_files = os.listdir("D:\Thesis\database")
    for file in in_files:
        with open("D:/Thesis/database/"+file) as event:
            lines = event.readlines()
        j = 0
        for line in lines:
            if "    Status" in line:
                status_line = j
                break
            j += 1
        if "rejected" in lines[status_line]:
            continue
        if " NOT SET" in lines[status_line]:
            continue
        if "not existing" in lines[2]:
            continue
        i = 0
        event_id = lines[1][27:41]                                                   #Read ID
        for line in lines:
            if "Date" in line:                                                       # Read Date and time
                time_string = line[27:37]+lines[i+1][27:39]
                time = dt.datetime.strptime(time_string, "%Y-%m-%d%H:%M:%S.%f")  # Save in 'datetime' variable
            if "Latitude   " in line:                                                # Read Latitude
                lat = float(line[27:37])
            if "Longitude   " in line:                                               # Read Longitude
                lon = float(line[27:37])
            if "Depth    " in line:                                                  # Read Depth
                depth = float(line[30:37])
            if "Agency    " in line:                                                 # Read Agency
                agency = line[27:31]
            if "Residual RMS     " in line:
                rms_res = float(line[29:35])                                         # Read RMS
            if "Azimuthal gap      " in line:
                gap = float(line[28:34])                                             # Read GAP
            if "Network magnitudes:" in line:
                magnitude_lines = [lines[i+1],lines[i+2],lines[i+3]]
                for mag_line in magnitude_lines:
                    if "preferred" in mag_line:
                        mag = float(mag_line[13:18])                                     # Read preferred Magnitude
                break                           # Stop reading file
            i += 1
    # Checking if the event is valid
        if min_lat < lat < max_lat:
            if min_lon < lon < max_lon:
                if depth < max_dep:
                    if gap < max_gap:
                        if rms_res < max_rms:
                            if mag > min_mag :
                                primary_events[event_id] = (time, lat, lon, depth, agency, rms_res, gap, mag)
                                primary_events_ids.append(event_id)
    print("#### " + str(len(primary_events)) + " primary events selected! ####")
    with open ("primary_events_id", 'w+') as list_file:
        list_file.write(str(len(primary_events))+"\t"+dt.datetime.strftime(dt.datetime.now(),"%d/%m/%Y %H:%M:%S")+"\n")
        for single_id in primary_events_ids:
            list_file.write(single_id+"\n")
    return primary_events, primary_events_ids

# Obtain the names and aka of stations
def StationInfo():
    print("#### Obtaining station info ####")
    station_list = list()
    blacklist = list()
    with open("station_blacklist.txt") as blacklist_file:
        blacklist_lines = blacklist_file.readlines()
        for line in blacklist_lines:
            blacklist.append(line.strip("\n"))
    with open("../Hengill.sta") as station_file:
        lines = station_file.readlines()
    for line in lines[1:]:
        if line[0:4] in blacklist:
            continue
        station_list.append(line[0:4])
    station_respell = {"GEI": "XGEI", "LHL": "XLHL", "ASM": "XASM", "BJA": "XBJA", "EDA": "XEDA", "HAU": "XHAU",
                "HEI": "XHEI", "KAS": "XKAS", "KRO": "XKRO", "SAN": "XSAN", "SAU": "XSAU", "SOL": "XSOL", "SHR": "XSHR",
                "VOS": "XVOS", "HUMLI": "UMLI", "HVH": "XHVH", "IND": "XIND", "INNST": "NNST", "LSKAR": "SKAR",
                "SKARM": "KARM", "SVIN": "SVIN", "KRIST": "RIST", "GRAFN": "RAFN", "KOLDU": "OLDU", "NESJV": "ESJV",
                "SKEGG": "KEGG", "ORUST": "RUST", "TROLL": "ROLL", "HURD": "HURD", "LAKA": "LAKA", "VOG": "XVOG",
                "LAULA": "AULA", "SKINN": "KINN", "HAMAR": "AMAR", "LYTI": "LYTI", "GUNN": "GUNN", "GRV": "XGRV",
                "NYL": "XNYL", "RNE": "XRNE", "SIG": "XSIG", "MEL": "XMEL", "KVO": "XKVO", "RAH": "XRAH", "SYRA": "SYRA",
                "SYRD": "SYRD", "SYRN": "SYRN", "LANG": "LANG", "STMN": "STMN", "ELDBG": "LDBG", "GRA": "XGRA",
                "HLA": "XHLA", "MID": "XMID", "GAESK": "AESK", "DALFJ": "ALFJ", "BEINI": "EINI", "SBS": "XSBS",
                "SHN": "XSHN", "GFJ": "XGFJ", "HVET5": "VET5", "HVA": "XHVA", "THEIG": "HEIG", "SPB": "XSPB",
                "THORF": "HORF", "GRT": "XGRT", "SUH": "XSUH", "HSPHO": "SPHO", "LAUF": "LAUF", "YVIK": "YVIK",
                "SKI": "XSKI", "OLF42": "LF42", "GAN02": "AN02", "FAL44":"AL44", "KAT03": "AT03", "LHA40": "HA40",
                "VAL41": "AL41", "GRH43": "RH43", "NUP27": "UP27", "THU04": "HU04", "BIT06": "IT06", "LAM08": "AM08",
                "LAK24": "AK24", "OLK26": "LK26", "URD20": "RD20", "JAK25": "AK25", "OHO23": "HO23", "SKA10": "KA10",
                "THJ07": "HJ07", "THF21": "HF21", "MEI05": "EI05", "KAP01":"AP01","REY09":"REY9", "BLK22": "BLK2",
                "STEKK": "STEK", "GA3": "XGA3", "GA1": "XGA1", "GA2":"XGA2", "GA4": "XGA4", "GA5": "XGA5", "GA6":"XGA6",
                "GA7": "XGA7", "BLIKA": "BLIK", "NIDUR": "NDUR", "SKOLI": "SKOL", "VIDEY": "VDEY", "GELDV": "GLDV",
                "GELDA": "GLDA", "R42": "XR42", "GOLF1":"GLF1", "GOLF2": "GLF2", "GOLF3": "GLF3"}
    print ("#### Done! ####")
    return station_list,station_respell


# Compile variables of the database into files
def compiler(par_dic):
    import os
    import datetime as dt
    from functions import query_yes_no

    filename = par_dic['filename']
    txt_FLAG = par_dic['txt_FLAG']
    cnv_FLAG = par_dic['cnv_FLAG']
    nordic_FLAG = par_dic['nordic_FLAG']
    station_min = int(par_dic['NUM_STA_MIN'])

    # Obtain list of events to compile
    if os.path.exists("primary_events_id"):
        with open("primary_events_id") as id_list:
            number_of_events, date_of_reading = id_list.readline().split("\t")
            question = (" Would you like to do another primary selection?\n "
                        "This would overwrite the last primary selection with "
                        + number_of_events + " events, with time: " + date_of_reading)
            input_flag = query_yes_no(question, default='no')
        if input_flag:
            events, events_ids = Primary_Select(par_dic)
        if not input_flag:
            events_ids = list()
            events = {}
            with open("primary_events_id") as id_list_file:
                next(id_list_file)
                for line in id_list_file:
                    events_ids.append(line.strip("\n"))
            for i_id in events_ids:
                with open("../database/"+i_id+".txt") as approved_event:
                    lines = approved_event.readlines()
                    i = 0
                    for line in lines:
                        if "Date" in line:                                                       # Read Date and time
                            time_string = line[27:37]+lines[i+1][27:39]
                            time = dt.datetime.strptime(time_string, "%Y-%m-%d%H:%M:%S.%f")  # Save in 'datetime' variable
                        if "Latitude   " in line:                                                # Read Latitude
                            lat = float(line[27:37])
                        if "Longitude   " in line:                                               # Read Longitude
                            lon = float(line[27:37])
                        if "Depth    " in line:                                                  # Read Depth
                            depth = float(line[30:37])
                        if "Agency    " in line:                                                 # Read Agency
                            agency = line[27:31]
                        if "Residual RMS     " in line:
                            rms_res = float(line[29:35])                                         # Read RMS
                        if "Azimuthal gap      " in line:
                            gap = float(line[28:34])                                             # Read GAP
                        if "Network magnitudes:" in line:
                            magnitude_lines = [lines[i+1],lines[i+2],lines[i+3]]
                            for mag_line in magnitude_lines:
                                if "preferred" in mag_line:
                                    mag = float(mag_line[13:18])                              # Read preferred Magnitude
                            break                           # Stop reading file
                        i += 1
                    events[i_id] = (time, lat, lon, depth, agency, rms_res, gap, mag)
    else:
        print("#### No primary selection file detected #####")
        events, events_ids = Primary_Select(par_dic)
    compiled_events= {}
    # Obtain stations Info
    station_list, station_respell = StationInfo()
    station_dict = {}
    for station in station_list:
        station_dict[station] = list()

    # strings are the files are written
    if nordic_FLAG:
        nordic_file = ""
    if cnv_FLAG:
        cnv_file = ""
    if txt_FLAG:
        txt_file = ""

    # Obtain phases information
    # e_ refers to event variable ph_ to a phase variable. They should change when the event or phase change
    Number_events_compiled = 0
    for i_id in events_ids:
        with open("../database/"+i_id+".txt") as event:
            lines2 = event.readlines()
        e_datetime = events[i_id][0]
        e_time_string = dt.datetime.strftime(events[i_id][0], "%Y %m %d %H:%M:%S.%f")
        e_time = dt.time.fromisoformat(e_time_string[11:])
        i = 0
        e_number_phases = 0
        for line2 in lines2:
            # Search for the line where the phases start to be listed
            i += 1
            if "Phase arrivals:" in line2:
                break
        # Number of phases in the file
        N_PH = int(lines2[i-1][0:2])
        # List to save phases
        if cnv_FLAG:
            cnv_e_phases = list()
        if nordic_FLAG:
            nordic_e_phases = list()
        # Counter to keep an eye on the number of Auto-picked events
        e_autophases = 0
        # List to save the stations that detected the event
        e_stationlist = list()
        # Error Values. Not all files reported these values
        E_Time_error = "      "
        E_Lat_error = "      "
        E_Lon_error = "      "
        E_Depth_error = "     "
        for line in lines2:
            if "Time          " in line:
                if "+/-" in line:
                    E_Time_ef = float(line[45:51])
                    E_Time_error = "{0:6.2f}".format(E_Time_ef)
            if "Latitude     " in line:
                if "+/-" in line:
                    E_Lat_ef = float(line[48:54])
                    E_Lat_error = "{0:6.1f}".format(E_Lat_ef)
            if "Longitude     " in line:
                if "+/-" in line:
                    E_Lon_ef = float(line[48:54])
                    E_Lon_error = "{0:6.1f}".format(E_Lon_ef)
            if "Depth      " in line:
                if "+/-" in line:
                    E_Depth_ef = float(line[48:54])
                    E_Depth_error = "{0:5.1f}".format(E_Depth_ef)

        # Read phases #################################################################################################
        for j in range(i+1, i+1+N_PH):

            # Station
            str_station = (lines2[j][4:9]).strip()         # Read the station name for the phase
            # use a station dictionary to respell 4 letters standard name
            if str_station in list(station_respell.keys()):
                xstation = station_respell[str_station]
            else:
                xstation = str_station
            if xstation in station_list:
                e_stationlist.append(xstation)
                station = xstation
            else:
                continue

            # Phase type (P or S)
            phase_type = lines2[j][32]

            # Time
            phase_time = dt.time.fromisoformat(lines2[j][39:51])   # The time of the phase is saved in a time variable
            if e_time > phase_time:
                continue
            phase_delta_time = dt.datetime.combine(dt.date.min, phase_time) - dt.datetime.combine(dt.date.min, e_time)

            # checking if the picking was automatic or manual
            if lines2[j][61] == "A":  # if the phase is automatically picked the counters registered
                e_autophases += 1
                ph_autophasePick = "A"
            else:
                ph_autophasePick = " "

            # Some extra info about the phase
            ph_azimut = int(round(float(lines2[j][25:30])))
            if "N/A" in lines2[j][54:60]:
                ph_time_residual = -99.999
            else:
                ph_time_residual = float(lines2[j][54:60])
            ph_station_distance = float(lines2[j][16:24]) * 111.1949  #station distance from degrees to km
            e_number_phases += 1
            # Writing phase string
            if cnv_FLAG:
                cnv_phase_string = "{0}{1}1{2:6.2f}".format(station, phase_type, phase_delta_time.total_seconds())
                cnv_e_phases.append(cnv_phase_string)
            if nordic_FLAG:
                phase_time_string = dt.time.strftime(phase_time, "%H %M %S.%f")
                ph_Hour = int(phase_time_string[0:2])
                ph_minute = int(phase_time_string[3:5])
                ph_second = float(phase_time_string[6:12])
                nordic_phase_string = " {0}     {1}   0{2}  {3:2}{4:2}{5:6.2f}                                   {6:5.2f} 0{7:5.1f} {8:3}4" \
                    .format(station, phase_type, ph_autophasePick, ph_Hour, ph_minute, ph_second, ph_time_residual, ph_station_distance, ph_azimut)
                nordic_e_phases.append(nordic_phase_string)
        # End reading phases ##########################################################################################

        if e_autophases > 3:
            continue
        if station_min > e_number_phases:
            continue
        for station in e_stationlist:
            station_dict[station].append(events[i_id])
        Number_events_compiled +=1
        compiled_events[i_id]=events[i_id]
        origin_Year = int(e_time_string[0:4])
        origin_Month = int(e_time_string[5:7])
        origin_Day = int(e_time_string[8:10])
        origin_Hour = int(e_time_string[11:13])
        origin_Minute = int(e_time_string[14:16])
        origin_Second = float(e_time_string[17:23])
        e_second = origin_Second
        e_minute = origin_Minute
        esecond = round(origin_Second, 1)
        if esecond >= 60.0:
            e_second = 00.0
            e_minute += 1
        if nordic_FLAG:
            # The Header of the event string is created
            nordic_event_string = """ {0:04} {1:02}{2:02} {3:02}{4:02} {5:4.1f} L {6:7.3f}{7:8.3f}{8:5.1f}S {9}{10:3}{11:4.1f}{12:4.1f}                    1""" \
                .format(origin_Year, origin_Month, origin_Day, origin_Hour, e_minute, e_second, events[i_id][1], events[i_id][2], events[i_id][3], events[i_id][4],
                        len(e_stationlist), events[i_id][5], events[i_id][7])
            nordic_event_string += "\n"
            nordic_event_error_string = """ GAP={0:3}      {1}    {2}  {3}{4}                                    E\n""" \
                .format(events[i_id][6], E_Time_error, E_Lat_error, E_Lon_error, E_Depth_error)
            nordic_event_string += nordic_event_error_string
            nordic_event_string += """ STAT SP IPHASW D HRMN SECON CODA AMPLIT PERI AZIMU VELO AIN AR TRES W  DIS CAZ7\n"""
            # the phases are added 1 by line
            for element in nordic_e_phases:
                nordic_event_string += element
                nordic_event_string += "\n"
            nordic_event_string += " "*80+"\n"
            nordic_file += nordic_event_string
        if cnv_FLAG:
            if events[i_id][1] > 0:
                rLAT = events[i_id][1]
                LM = "N"
            elif events[i_id][1] < 0:
                rLAT = events[i_id][1]*-1
                LM = "S"
            if events[i_id][2] > 0:
                rLON = events[i_id][2]
                LH = "E"
            elif events[i_id][2] < 0:
                rLON = events[i_id][2]*-1
                LH = "W"
            cnv_event_string = """{0}{1:02}{2:02} {3:02}{4:02} {5:05.2f} {6:7.4f}{7} {8:8.4f}{9}{10:7.2f}{11:7.2f} 0""" \
                .format(origin_Year, origin_Month, origin_Day, origin_Hour, e_minute, esecond, rLAT, LM, rLON, LH, events[i_id][3], events[i_id][7])
            i = 0
            cnv_event_string += "\n"
            # the phases strings are added by rows of 6 event per row
            for element in cnv_e_phases:
                if i == 6:
                    cnv_event_string += "\n"
                    i = 0
                cnv_event_string += element
                i += 1
            cnv_event_string += "\n"
            cnv_event_string += "\n"
            cnv_file += cnv_event_string
        if txt_FLAG:
            txt_event_string = "{0}\t{1}\t{2:9.6f}\t{3:10.6f}\t{4:6.3f}\t{5:5.2f}\n"\
                .format(i_id,events[i_id][0],events[i_id][1],events[i_id][2],events[i_id][3], events[i_id][7])
            txt_file += txt_event_string
    # Writing files
    if nordic_FLAG:
        with open(filename+".nord",'w+') as file:
            file.write(nordic_file)
    if cnv_FLAG:
        with open(filename+".cnv",'w+') as file:
            file.write(cnv_file)
    if txt_FLAG:
        with open(filename+".txt",'w+') as file:
            file.write(txt_file)
    print("#### " + str(Number_events_compiled) + " successfully compiled ####")
    return compiled_events, station_dict


# Compile variable and files from a given IDs list
def mini_compiler(events_id, par_dic):
    import datetime as dt
    min_lat = float(par_dic['min_lat'])
    max_lat = float(par_dic['max_lat'])
    min_lon = float(par_dic['min_lon'])
    max_lon = float(par_dic['max_lon'])
    max_dep = float(par_dic['max_depth'])
    max_gap = float(par_dic['max_GAP'])
    max_rms = float(par_dic['max_RMS'])
    min_mag = float(par_dic['min_mag'])
    filename = par_dic['filename']
    txt_FLAG = par_dic['txt_FLAG']
    cnv_FLAG = par_dic['cnv_FLAG']
    nordic_FLAG = par_dic['nordic_FLAG']
    station_min = int(par_dic['NUM_STA_MIN'])
    events = {}
    new_ids = list()
    for i_id in events_id:
        with open("../database/"+i_id+".txt") as approved_event:
            lines = approved_event.readlines()
            i = 0
            for line in lines:
                if "Date" in line:                                                       # Read Date and time
                    time_string = line[27:37]+lines[i+1][27:39]
                    time = dt.datetime.strptime(time_string, "%Y-%m-%d%H:%M:%S.%f")  # Save in 'datetime' variable
                if "Latitude   " in line:                                                # Read Latitude
                    lat = float(line[27:37])
                if "Longitude   " in line:                                               # Read Longitude
                    lon = float(line[27:37])
                if "Depth    " in line:                                                  # Read Depth
                    depth = float(line[30:37])
                if "Agency    " in line:                                                 # Read Agency
                    agency = line[27:31]
                if "Residual RMS     " in line:
                    rms_res = float(line[29:35])                                         # Read RMS
                if "Azimuthal gap      " in line:
                    gap = float(line[28:34])                                             # Read GAP
                if "Network magnitudes:" in line:
                    magnitude_lines = [lines[i+1],lines[i+2],lines[i+3]]
                    for mag_line in magnitude_lines:
                        if "preferred" in mag_line:
                            mag = float(mag_line[13:18])                              # Read preferred Magnitude
                    break                           # Stop reading file
                i += 1
            # Checking if the event is valid
            if min_lat < lat < max_lat:
                if min_lon < lon < max_lon:
                    if depth < max_dep:
                        if gap < max_gap:
                            if rms_res < max_rms:
                                if mag > min_mag :
                                    events[i_id] = (time, lat, lon, depth, agency, rms_res, gap, mag)
                                    new_ids.append(i_id)
    compiled_events= {}
    # Obtain stations Info
    station_list, station_respell = StationInfo()
    station_dict = {}
    for station in station_list:
        station_dict[station] = list()

    # strings are the files are written
    if nordic_FLAG:
        nordic_file = ""
    if cnv_FLAG:
        cnv_file = ""
    if txt_FLAG:
        txt_file = ""

    # Obtain phases information
    # e_ refers to Event variable, ph_ to a phase variable. They should change when the event or phase change
    Number_events_compiled = 0
    for i_id in new_ids:
        with open("../database/"+i_id+".txt") as event:
            lines2 = event.readlines()
        e_time_string = dt.datetime.strftime(events[i_id][0], "%Y %m %d %H:%M:%S.%f")
        e_time = dt.time.fromisoformat(e_time_string[11:])
        i = 0
        e_number_phases = 0
        for line2 in lines2:
            # Search for the line where the phases start to be listed
            i += 1
            if "Phase arrivals:" in line2:
                break
        # Number of phases in the file
        N_PH = int(lines2[i-1][0:2])
        # List to save phases
        if cnv_FLAG:
            cnv_e_phases = list()
        if nordic_FLAG:
            nordic_e_phases = list()
        # Counter of the number of Auto-picked events
        e_autophases = 0
        # List to save the stations that detected the event
        e_stationlist = list()
        # Error Values. Not all files reported these values
        E_Time_error = "      "
        E_Lat_error = "      "
        E_Lon_error = "      "
        E_Depth_error = "     "
        for line in lines2:
            if "Time          " in line:
                if "+/-" in line:
                    E_Time_ef = float(line[45:51])
                    E_Time_error = "{0:6.2f}".format(E_Time_ef)
            if "Latitude     " in line:
                if "+/-" in line:
                    E_Lat_ef = float(line[48:54])
                    E_Lat_error = "{0:6.1f}".format(E_Lat_ef)
            if "Longitude     " in line:
                if "+/-" in line:
                    E_Lon_ef = float(line[48:54])
                    E_Lon_error = "{0:6.1f}".format(E_Lon_ef)
            if "Depth      " in line:
                if "+/-" in line:
                    E_Depth_ef = float(line[48:54])
                    E_Depth_error = "{0:5.1f}".format(E_Depth_ef)

        # Read phases #################################################################################################
        for j in range(i+1, i+1+N_PH):

            # Station
            str_station = (lines2[j][4:9]).strip()         # Read the station name for the phase
            # use a station dictionary to respell 4 letters standard name
            if str_station in list(station_respell.keys()):
                xstation = station_respell[str_station]
            else:
                xstation = str_station
            if xstation in station_list:
                e_stationlist.append(xstation)
                station = xstation
            else:
                continue

            # Phase type (P or S)
            phase_type = lines2[j][32]

            # Time
            phase_time = dt.time.fromisoformat(lines2[j][39:51])   # The time of the phase is saved in a time variable
            if e_time > phase_time:
                continue
            phase_delta_time = dt.datetime.combine(dt.date.min, phase_time) - dt.datetime.combine(dt.date.min, e_time)

            # checking if the picking was automatic or manual
            if lines2[j][61] == "A":  # if the phase is automatically picked the counters registered
                e_autophases += 1
                ph_autophasePick = "A"
            else:
                ph_autophasePick = " "

            # Some extra info about the phase
            ph_azimut = int(round(float(lines2[j][25:30])))
            if "N/A" in lines2[j][54:60]:
                ph_time_residual = -99.999
            else:
                ph_time_residual = float(lines2[j][54:60])
            ph_station_distance = float(lines2[j][16:24]) * 111.1949  #station distance from degrees to km
            e_number_phases += 1
            # Writing phase string
            if cnv_FLAG:
                cnv_phase_string = "{0}{1}1{2:6.2f}".format(station, phase_type, phase_delta_time.total_seconds())
                cnv_e_phases.append(cnv_phase_string)
            if nordic_FLAG:
                phase_time_string = dt.time.strftime(phase_time, "%H %M %S.%f")
                ph_Hour = int(phase_time_string[0:2])
                ph_minute = int(phase_time_string[3:5])
                ph_second = float(phase_time_string[6:12])
                nordic_phase_string = " {0}     {1}   0{2}  {3:2}{4:2}{5:6.2f}                                   {6:5.2f} 0{7:5.1f} {8:3}4" \
                    .format(station, phase_type, ph_autophasePick, ph_Hour, ph_minute, ph_second, ph_time_residual, ph_station_distance, ph_azimut)
                nordic_e_phases.append(nordic_phase_string)
        # End reading phases ##########################################################################################

        if e_autophases > 3:
            continue
        if station_min > e_number_phases:
            continue
        for station in e_stationlist:
            station_dict[station].append(events[i_id])
        Number_events_compiled +=1
        compiled_events[i_id]=events[i_id]
        origin_Year = int(e_time_string[0:4])
        origin_Month = int(e_time_string[5:7])
        origin_Day = int(e_time_string[8:10])
        origin_Hour = int(e_time_string[11:13])
        origin_Minute = int(e_time_string[14:16])
        origin_Second = float(e_time_string[17:23])
        e_second = origin_Second
        e_minute = origin_Minute
        esecond = round(origin_Second, 1)
        if esecond >= 60.0:
            e_second = 00.0
            e_minute += 1
        if nordic_FLAG:
            # The Header of the event string is created
            nordic_event_string = """ {0:04} {1:02}{2:02} {3:02}{4:02} {5:4.1f} L {6:7.3f}{7:8.3f}{8:5.1f}S {9}{10:3}{11:4.1f}{12:4.1f}                    1""" \
                .format(origin_Year, origin_Month, origin_Day, origin_Hour, e_minute, e_second, events[i_id][1], events[i_id][2], events[i_id][3], events[i_id][4],
                        len(e_stationlist), events[i_id][5], events[i_id][7])
            nordic_event_string += "\n"
            nordic_event_error_string = """ GAP={0:3}      {1}    {2}  {3}{4}                                    E\n""" \
                .format(events[i_id][6], E_Time_error, E_Lat_error, E_Lon_error, E_Depth_error)
            nordic_event_string += nordic_event_error_string
            nordic_event_string += """ STAT SP IPHASW D HRMN SECON CODA AMPLIT PERI AZIMU VELO AIN AR TRES W  DIS CAZ7\n"""
            # the phases are added 1 by line
            for element in nordic_e_phases:
                nordic_event_string += element
                nordic_event_string += "\n"
            nordic_event_string += " "*80+"\n"
            nordic_file += nordic_event_string
        if cnv_FLAG:
            if events[i_id][1] > 0:
                rLAT = events[i_id][1]
                LM = "N"
            elif events[i_id][1] < 0:
                rLAT = events[i_id][1]*-1
                LM = "S"
            if events[i_id][2] > 0:
                rLON = events[i_id][2]
                LH = "E"
            elif events[i_id][2] < 0:
                rLON = events[i_id][2]*-1
                LH = "W"
            cnv_event_string = """{0}{1:02}{2:02} {3:02}{4:02} {5:05.2f} {6:7.4f}{7} {8:8.4f}{9}{10:7.2f}{11:7.2f} 0""" \
                .format(origin_Year, origin_Month, origin_Day, origin_Hour, e_minute, esecond, rLAT, LM, rLON, LH, events[i_id][3], events[i_id][7])
            i = 0
            cnv_event_string += "\n"
            # the phases strings are added by rows of 6 event per row
            for element in cnv_e_phases:
                if i == 6:
                    cnv_event_string += "\n"
                    i = 0
                cnv_event_string += element
                i += 1
            cnv_event_string += "\n"
            cnv_event_string += "\n"
            cnv_file += cnv_event_string
        if txt_FLAG:
            txt_event_string = "{0}\t{1}\t{2:9.6f}\t{3:10.6f}\t{4:6.3f}\t{5:5.2f}\n" \
                .format(i_id,events[i_id][0],events[i_id][1],events[i_id][2],events[i_id][3], events[i_id][7])
            txt_file += txt_event_string
    # Writing files
    if nordic_FLAG:
        with open("custom_"+filename+".nord",'w+') as file:
            file.write(nordic_file)
    if cnv_FLAG:
        with open("custom_"+filename+".cnv",'w+') as file:
            file.write(cnv_file)
    if txt_FLAG:
        with open("custom_"+filename+".txt",'w+') as file:
            file.write(txt_file)
    print("#### " + str(Number_events_compiled) + " successfully compiled ####")
    return compiled_events, station_dict


# Obtain the locations and elevation of stations
def StationData():
    station_data_dict = {}
    blacklist= list()
    with open("station_blacklist.txt") as blacklist_file:
        blacklist_lines = blacklist_file.readlines()
        for line in blacklist_lines:
            blacklist.append(line.strip("\n"))
    with open("../Hengill.sta") as station_file:
        station_data = station_file.readlines()[1:]
    for line in station_data:
        station_name_i = line[0:4]
        if station_name_i in blacklist:
            continue
        station_lat_i = float(line[4:11])
        station_lon_i = -1*float(line[14:21])
        station_elev_i = float(line[23:27])
        station_data_dict[station_name_i] = (station_lon_i, station_lat_i, station_elev_i)
    return station_data_dict



