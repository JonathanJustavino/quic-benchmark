import pandas as pd
from pathlib import Path
import statistics as st
import matplotlib.pyplot as plt
import numpy as np


def dataloader(directory_list):
    # collect quic csvs
    quic_csvs = []
    for folder in directory_list:
        curr_csv = pd.read_csv(folder / 'quic_timestamps.csv', header=None, delimiter='\t', index_col=False)
        quic_csvs.append(curr_csv)

    tcp_csvs = []
    for folder in directory_list:
        curr_csv = pd.read_csv(folder / 'tcp_timestamps.csv', header=None, delimiter='\t', index_col=False)
        tcp_csvs.append(curr_csv)

    return quic_csvs, tcp_csvs


def list_unwrap(wrapped_list):
    newlist = []
    for el in wrapped_list:
        newlist.append(el[0])
    return newlist


# calculate average values of QUIC packages
def quic_average(quic_csvs):
    avg_list = []
    std_list = []

    # iterate over each row==time of 1st packet, 2nd packet etc.
    for row in range(0, 20):
        tmp_list = []

        # extract row of each csv + append to tmp_list
        for one_csv in quic_csvs:
            one_csv = one_csv.values.tolist()  # convert panda DataFrame to List
            one_csv = list_unwrap(one_csv)  # unwrap list of list
            tmp_list.append(one_csv[row])

        avg_list.append(st.mean(tmp_list))
        std_list.append(st.stdev(tmp_list))

    return avg_list, std_list


def plot_quic_graph(quic_avg_std_tuple):
    # static colors for graphs -> quic == blue, tcp == red
    quic_serv_col = 'b'
    col_tcp_serv = 'r'

    # init figure
    fig = plt.figure()
    fig.suptitle('nginx-QUIC: average+std', fontsize=15)
    ax = fig.add_subplot(111)

    # set x-axis elements
    x_axis = quic_avg_std_tuple[0]

    # set y-axis to [1..20] for the 20 packets
    y_axis_ticks = list(range(1, 21))
    ax.set_yticks(y_axis_ticks)

    # standard deviation
    error = quic_avg_std_tuple[1]
    print(error)

    ax.plot(x_axis, y_axis_ticks, c=quic_serv_col, marker='o', ls='', label="quic server")
    ax.errorbar(x_axis, y_axis_ticks, xerr=error, fmt="o")

    plt.grid(1)
    plt.ylabel("Packets")
    plt.xlabel("Timeline in seconds")
    plt.show()


if __name__ == '__main__':
    global_path = Path.cwd()
    # get directories: 1st run, 2nd run etc.
    directories = [x for x in global_path.iterdir() if x.is_dir()]

    # get list of quic and tcp csv's
    csv_tuple = dataloader(directories)

    quic_avg_std_values = quic_average(csv_tuple[0])

    plot_quic_graph(quic_avg_std_values)
