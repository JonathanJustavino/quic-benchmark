import json
from pathlib import Path
import os
import matplotlib.pyplot as plt
import re

# Client events:
# ready, writeToServer, error
# zB {"ready":"2021-01-09T20:23:21.786Z","writeToServer":"2021-01-09T20:23:21.793Z","error":""}

# Server events:
# listening, session, keylog, secure, data, streamEnd, streamClose, socketClose / handshakeDurationInNs
# zB {"listening":"2021-01-09T20:23:17.230Z","session":"2021-01-09T20:23:21.787Z",
# "keylog":"2021-01-09T20:23:21.791Z","secure":"2021-01-09T20:23:21.794Z","data":"2021-01-09T20:23:21.796Z","streamEnd":"2021-01-09T20:23:21.798Z","streamClose":"2021-01-09T20:23:31.805Z","socketClose":"2021-01-09T20:23:31.810Z"}{"handshakeDurationInNs":"6427581"}

# OLD Path to folder "measurements"
# abs_path = Path('../tcp/measurements/tcp-local/')

# Path-dict
all_pathes = [Path('../tcp/measurements/tcp-local/timestamps/'),
              Path('../tcp/measurements/tcp-same-network/timestamps/'),
              Path('../quic/measurements/quic-local/timestamps/'),
              Path('../quic/measurements/quic-same-network/timestamps/')]

curr_dict_tuple = 0
events = 0
events_timeline_seconds = 0

# get all numbers [0-9]
# \d: Matches any decimal digit; this is equivalent to the class [0-9].
regex = re.compile(r'\d+')


# split 2021-01-09T20:23:17.230Z -> [2021,01,09] [20, 23, 17.23]
# expects string -> returns (list[int], list[float])
def split_timestamp(timestamp):
    lists = timestamp.split('T')

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
    participant = ''
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
        participant = 'client'
    # --- Participant: Server ---
    else:
        # split json dict -> events, handshakeDurationInNs
        pydict = json.loads(data)
        eventsdict = pydict['events']
        handshakedur_ns = pydict['durations']['handshakeDurationInNs']
        participant = 'server'

    # --- QUIC - protocol ---
    if 'quic' in filename:
        protocol = 'quic'
    # --- TCP/TLS - protocol ---
    else:
        protocol = 'tcp'

    # --- get test-round: ----
    # -> aus filname auslesen mit regex
    testrun_num = [int(nr_string) for nr_string in regex.findall(filename)]
    # Liste entfernen TODO: was ist wenn testrun-anzahl > 9 also 2stellig? regex checkt bisher nur 1 element
    testrun_num = testrun_num[0]

    # --- returns: ---
    # testrun_nr: which testrun (1,2, ..)
    # protocol: 'quic' or 'tcp'
    # participant: 'server' or 'client'
    # location: local (on localhost) or network
    # events: eventsdict, so that events can be accessed zB via "eventsdict['session'] == timestamp"
    # handshakeduration in ns: (== -1 bei client)
    return {'testrun_nr': testrun_num, 'protocol': protocol, 'participant': participant, 'location': location,
            'events': eventsdict, 'handshakeduration_ns': handshakedur_ns}


def merge_min_sec(minute, sec):
    sec += minute * 60
    return sec


def split_sec_in_min(sec):
    minute = sec // 60
    sec = sec % 60
    return minute, sec


# get only elements out of list that are from the same "run" (== curr_run)
def filter_list(data_dict, curr_run):
    if data_dict['testrun_nr'] == curr_run:
        return data_dict


if __name__ == '__main__':

    # list that contains all dicts from all testruns + participants
    # of the form: {'testrun_nr': testrun_num, 'protocol': protocol, 'participant': participant,
    #             'events': eventsdict, 'handshakeduration_ns': handshakedur_ns}
    data_all_runs = []

    for path in all_pathes:
        # get all json filenames at given path
        all_filenames = os.listdir(path)
        # get infos for each file,
        # append infos to list "data_all_runs"
        for file in all_filenames:
            # get dict with testrun_nr, participant (server/client) etc from dataloader
            file_info = dataloader(str(path / file))
            data_all_runs.append(file_info)

    # static colors for graphs -> quic == blue, tcp == red
    quic_serv_col = 'b'
    quic_client_col = 'c'
    col_tcp_serv = 'r'
    col_tcp_client = 'm'

    runs_in_total = int(len(data_all_runs) / 4)
    print("runs in total (network + local): ", runs_in_total)

    # TODO: Separate local and network runs
    network_runs = []
    local_runs = []

    for element in data_all_runs:
        if element['location'] == 'local':
            local_runs.append(element)
        else:
            network_runs.append(element)
    print('elemente in local runs: ', local_runs)
    print('# elemente in local runs: ', len(local_runs))
    print('elemente in nw runs: ', network_runs)
    print('# elemente in nw runs: ', len(network_runs))
    quit()

    # TODO: sort all runs into run1, run2, etc.

    # init figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # über jeden file iterieren -> man weiß nicht welcher
    for n, file in enumerate(logfiles):
        curr_dict_tuple = dataloader(file)

        # zB "ready":"2021-01-09T20:23:21.786Z","writeToServer":"2021-01-09T20:23:21.793Z"
        events = curr_dict_tuple[0]

        # time of events unformatted
        events_timeline = list(events.values())
        # -> get eventtime in seconds
        # j = zB ([2021, 01, 09], [20, 23, 21.786] -> 21,786 (seconds))
        events_timeline_seconds = [split_timestamp(j)[1][2] for j in events_timeline]
        # j = zB ([2021, 01, 09], [20, 23, 21.786] -> 23 (min))
        events_timeline_minutes = [split_timestamp(j)[1][1] for j in events_timeline]

        # normalize the x-axis / timestamps so they all start with zero
        # (just substract the first timestamp from each timestamp -> removes offset
        plt_x_axis = []
        for time in events_timeline_seconds:
            print('time: ', time, " - 1st timestamp", events_timeline_seconds[0])
            # substract 1st timestamp from each other timestamp
            time = time - events_timeline_seconds[0]
            # round to 5 decimal places (Nachkommastellen)
            time = round(time, 5)
            plt_x_axis.append(time)

        # eventnames
        plt_y_axis = list(events.keys())

        # current color for current graph
        # curr_color = colorlist_plot[(n % len(colorlist_plot))]
        ax.plot(plt_x_axis, plt_y_axis, c=curr_color, marker='o', ls='', fillstyle='none', label=str(file))

        # annotate each point on each graph
        for (x, y) in zip(plt_x_axis, plt_y_axis):
            if 'quic' in file:
                ax.annotate(x, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', color=curr_color)
            else:
                ax.annotate(x, (x, y), textcoords="offset points", xytext=(0, -15), ha='center', color=curr_color)

    plt.grid(1)
    # ToDo: position von text korrigieren -> am besten neben legende
    # plt.text(1, -1, "RTT:", fontsize=10)
    plt.legend(bbox_to_anchor=(0, 0), loc="upper left")
    plt.show()
