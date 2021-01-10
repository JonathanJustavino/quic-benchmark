import json
from pathlib import Path
import os
import matplotlib.pyplot as plt

# Client events:
# ready, writeToServer, error
# zB {"ready":"2021-01-09T20:23:21.786Z","writeToServer":"2021-01-09T20:23:21.793Z","error":""}

# Server events:
# listening, session, keylog, secure, data, streamEnd, streamClose, socketClose / handshakeDurationInNs
# zB {"listening":"2021-01-09T20:23:17.230Z","session":"2021-01-09T20:23:21.787Z",
# "keylog":"2021-01-09T20:23:21.791Z","secure":"2021-01-09T20:23:21.794Z","data":"2021-01-09T20:23:21.796Z","streamEnd":"2021-01-09T20:23:21.798Z","streamClose":"2021-01-09T20:23:31.805Z","socketClose":"2021-01-09T20:23:31.810Z"}{"handshakeDurationInNs":"6427581"}

# Path to folder "measurements"
abs_path = Path('/home/amelie/Uni/RNP_Komplexpraktikum/quic-benchmark/measurements/')

curr_dict_tuple = 0
events = 0
events_timeline = 0

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
def dataloader(filename):
    with open(abs_path / filename, 'r') as quicclient_file:
        data = quicclient_file.read()

    # have to dump server-logfile because contains 2 top-level json-objects
    if 'client' in filename:
        eventsdict = json.loads(data)
        # delete empty error message
        del eventsdict['error']
        handshakedur = -1
    else:
        pydict = json.loads(data)
        eventsdict = pydict['events']
        handshakedur = pydict['durations']['handshakeDurationInNs']

    # returns eventsdict, handshakeduration (== 0 bei client)
    # so that it can be accessed via "dict['keyword'] == value"
    return eventsdict, float(handshakedur)


if __name__ == '__main__':

    # get all logfiles of directory
    logfiles = os.listdir(abs_path)

    # init figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # possible colors for graphs/axis in figure
    colorlist_plot = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    for n, file in enumerate(logfiles):
        curr_dict_tuple = dataloader(file)

        # zB "ready":"2021-01-09T20:23:21.786Z","writeToServer":"2021-01-09T20:23:21.793Z"
        events = curr_dict_tuple[0]

        # time of events unformatted
        events_timeline = list(events.values())
        # -> get eventtime in seconds
        events_timeline = [split_timestamp(j)[1][2] for j in events_timeline]

        plt_x_axis = []
        for time in events_timeline:
            time = time - events_timeline[0]
            time = round(time, 5)
            plt_x_axis.append(time)

        # eventnames
        plt_y_axis = list(events.keys())

        ax.plot(plt_x_axis, plt_y_axis, c=colorlist_plot[(n % len(colorlist_plot))], ls='-', fillstyle='none', label=str(file))

    plt.grid(1)
    plt.legend(loc=2)
    plt.show()

