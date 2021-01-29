import json
from pathlib import Path
import os
import matplotlib.pyplot as plt
import re
import sys

# Client events:
# ready, writeToServer, error
# zB {"ready":"2021-01-09T20:23:21.786Z","writeToServer":"2021-01-09T20:23:21.793Z","error":""}

# Server events:
# listening, session, keylog, secure, data, streamEnd, streamClose, socketClose / handshakeDurationInNs
# zB {"listening":"2021-01-09T20:23:17.230Z","session":"2021-01-09T20:23:21.787Z",
# "keylog":"2021-01-09T20:23:21.791Z","secure":"2021-01-09T20:23:21.794Z","data":"2021-01-09T20:23:21.796Z","streamEnd":"2021-01-09T20:23:21.798Z","streamClose":"2021-01-09T20:23:31.805Z","socketClose":"2021-01-09T20:23:31.810Z"}{"handshakeDurationInNs":"6427581"}

# List with all paths
all_pathes = [Path('../tcp/measurements/tcp-local/timestamps/'),
              Path('../tcp/measurements/tcp-same-network/timestamps/'),
              Path('../quic/measurements/quic-local/timestamps/'),
              Path('../quic/measurements/quic-same-network/timestamps/')]

# get all numbers [0-9]
# \d: Matches any decimal digit; this is equivalent to the class [0-9].
regex = re.compile(r'\d+')


# split 2021-01-09T20:23:17.230Z -> [2021,01,09] [20, 23, 17.23]
# expects string -> returns (list[int], list[float])
def split_timestamp(timestamp_):
    lists = timestamp_.split('T')

    datelist = lists[0].split('-')
    # convert to int
    datelist = [int(i) for i in datelist]

    timelist = lists[1].split(':')
    # strip Z at the end
    timelist[2] = timelist[2].replace('Z', '')
    # convert to float
    timelist = [float(i) for i in timelist]

    return datelist, timelist  # zB ([2021, 01, 09], [20, 23, 21.786])


# loads json file and converts it to python dictionary
# Bekommt absoluten Pfad zu file
def dataloader(filename):
    testrun_num = 0
    protocol = ''
    participant_ = ''
    eventsdict = {}
    handshakedur_ns = 0
    location = ''

    with open(filename, 'r') as json_file:
        data = json_file.read()

    # --- Location of the testrun ---
    # LOCAL testrun (on localhost)
    if '-local' in filename:
        location = 'local'
    # NETWORK / LAN testrun
    else:
        location = 'network'

    # delete rest of the path from filename (if not, "quic" filter of filname string doesn't work)
    filename = os.path.basename(filename)

    # --- Participant: Client ---
    # have to dump server-logfile because contains 2 top-level json-objects
    if 'client' in filename:
        eventsdict = json.loads(data)
        # delete empty error message
        del eventsdict['error']
        handshakedur_ns = -1
        participant_ = 'client'
    # --- Participant: Server ---
    else:
        # split json dict -> events, handshakeDurationInNs
        pydict = json.loads(data)
        eventsdict = pydict['events']
        handshakedur_ns = pydict['durations']['handshakeDurationInNs']
        participant_ = 'server'

    # --- QUIC - protocol ---
    if 'quic' in filename:
        protocol = 'quic'
    # --- TCP/TLS - protocol ---
    else:
        protocol = 'tcp'

    # --- get test-round: ----
    # -> read test-run-nr from filname with regex
    testrun_num = [int(nr_string) for nr_string in regex.findall(filename)]
    # TODO: was ist wenn testrun-anzahl > 9 ? regex checkt bisher nur 1 element
    # delete list wrapping
    testrun_num = testrun_num[0]

    # --- returns: ---
    # testrun_nr: which testrun (1,2, ..)
    # protocol: 'quic' or 'tcp'
    # participant: 'server' or 'client'
    # location: local (on localhost) or network
    # events: eventsdict, so that events can be accessed zB via "eventsdict['session'] == timestamp"
    # handshakeduration in ns: (== -1 bei client)
    return {'testrun_nr': testrun_num, 'protocol': protocol, 'participant': participant_, 'location': location,
            'events': eventsdict, 'handshakeduration_ns': handshakedur_ns}


def sort_runs_by_number(unsorted_runs_list):
    runs_in_total = int(len(unsorted_runs_list) / 4)
    sorted_list = []

    for run_nr in range(1, runs_in_total+1):  # testrun_num begins at 1
        temp_list = []
        for run in unsorted_runs_list:
            if run['testrun_nr'] == run_nr:
                temp_list.append(run)
        sorted_list.append(temp_list)
    return sorted_list


def merge_min_sec(minute, sec):
    sec += minute * 60
    return sec


def split_sec_in_min(sec):
    minute = sec // 60
    sec = sec % 60
    return minute, sec


# get only elements out of list that are from the same "run" (== curr_run)
def filter_list(data_dict, current_run):
    if data_dict['testrun_nr'] == current_run:
        return data_dict


def parse_argv(nwruns_list, localruns_list):

    # default: localrun_list
    list_runs = localrun_list

    if sys.argv[1] == 'local' or 'network':
        # change to network only if said so in argv
        if sys.argv[1] == 'network':
            list_runs = nwruns_list
    else:
        print("Wrong argument for run location: Has to be 'local' or 'network'.")

    return list_runs


if __name__ == '__main__':

    # list that contains all dicts from all testruns + participants
    # of the form: {'testrun_nr': testrun_num, 'protocol': protocol, 'participant': participant,
    #             'events': eventsdict, 'handshakeduration_ns': handshakedur_ns}
    all_runs = []

    # Get all runs (local and network) into 2 unsorted lists:
    network_runs_unsorted = []
    local_runs_unsorted = []
    for path in all_pathes:
        # get all json filenames at given path
        all_filenames = os.listdir(path)
        # get infos for each file,
        # append infos to list "data_all_runs"
        for file in all_filenames:
            # get dict with testrun_nr, participant (server/client) etc from dataloader
            file_info = dataloader(str(path / file))

            # separate in local and network
            if file_info['location'] == 'local':
                local_runs_unsorted.append(file_info)
            else:
                network_runs_unsorted.append(file_info)

    # static colors for graphs -> quic == blue, tcp == red
    quic_serv_col = 'b'
    quic_client_col = 'c'
    col_tcp_serv = 'r'
    col_tcp_client = 'm'

    nwrun_list = sort_runs_by_number(network_runs_unsorted)
    localrun_list = sort_runs_by_number(local_runs_unsorted)

    # standard value list_all_runs:
    list_all_runs = nwrun_list

    if len(sys.argv) > 1:
        parse_argv(nwrun_list, localrun_list)

    # 1 graph per run
    for run_nr_index in range(0, len(list_all_runs)):

        # init figure
        fig = plt.figure()
        fig.suptitle("")
        ax = fig.add_subplot(111)

        all_participants = list_all_runs[run_nr_index]

        for n, participant in enumerate(all_participants):

            # time of events unformatted
            events_time = list(participant['events'].values())  # i.e. ['2021-01-17T23:14:45.560Z', '2021-01-17T23:14:59.390Z',.]

            # convert timestamps into seconds
            for index, timestamp in enumerate(events_time):
                global_sec = split_timestamp(timestamp)[1][2]  # return datelist=[year,..], timelist=[h, min, sec]
                global_min = split_timestamp(timestamp)[1][1]
                seconds = merge_min_sec(global_min, global_sec)
                events_time[index] = seconds  # seconds as absolute number

            # normalize timeline so it starts from zero + round time(float) to 5 decimal places
            events_time = [round((abs_time_sec - events_time[0]), 5) for abs_time_sec in events_time]

            # TODO: why doesnt removing minutes make a difference? lol -> maybe unnecessary
            # remove full minutes -> show only seconds
            events_time = [split_sec_in_min(seconds)[1] for seconds in events_time]

            # generating plot
            plt_x_axis = events_time
            plt_y_axis = list(participant['events'].keys())
            print("y- axis in round: ", n, plt_y_axis)
            color = ''
            # get plot color -> not the best, maybe move to dataloader and make color part of dict
            if participant['protocol'] == 'quic':
                if participant['participant'] == 'server':
                    color = quic_serv_col
                else:
                    color = quic_client_col
            else:
                if participant['participant'] == 'server':
                    color = col_tcp_serv
                else:
                    color = col_tcp_client

            ax.plot(plt_x_axis, plt_y_axis, c=color, marker='o', ls='', fillstyle='none',
                    label=str(participant['protocol'] + "_" + participant['participant']))

            print("Teilnehmer: ", n, "in aktuellem Durchlauf: ", run_nr_index)
            print('das wird an ax.plot hinzugefügt: x-achse: ', plt_x_axis)
            print('y-achse: ', plt_y_axis)

            # annotate each point on each graph
            for (x, y) in zip(plt_x_axis, plt_y_axis):
                if participant['protocol'] == 'quic':
                    ax.annotate(x, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', color=color)
                else:
                    ax.annotate(x, (x, y), textcoords="offset points", xytext=(0, -15), ha='center', color=color)

            # participant changes
        # run number changes
    # after all runs & participants

        plt.grid(1)
        # ToDo: position von text korrigieren -> am besten neben legende
        # plt.text(1, -1, "RTT:", fontsize=10)
        plt.legend(bbox_to_anchor=(0, 0), loc="upper left")  # No handles with labels found to put in legend.
        plt.show()