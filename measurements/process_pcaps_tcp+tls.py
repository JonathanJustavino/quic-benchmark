import pandas as pd
from pathlib import Path
import statistics as st


def dataloader(import_path):
    # get all measurement folders
    all_folders = sorted(import_path.glob('*'))

    # collect csvs with 14 packets in one list
    csvs_14 = []
    for folder in all_folders:
        curr_csv = pd.read_csv(import_path / folder / 'timestamps.csv', header=None, delimiter='\t', index_col=False)

        # drop csv folders with 14 packets
        if len(curr_csv) == 14:
            csvs_14.append(curr_csv)

    return csvs_14


def list_unwrap(wrapped_list):
    newlist = []
    for el in wrapped_list:
        newlist.append(el[0])
    return newlist


if __name__ == '__main__':
    global_path = Path(
        '/home/amelie/Uni/RNP_Komplexpraktikum/quic-benchmark/measurements/samples_threshold5_dev2_delay0/tcp/remote/')

    csvs = dataloader(global_path)

    avg_list = []
    # iterate over each row==time of 1st packet, 2nd packet etc.
    for row in range(0, 14):
        tmp_avg_list = []

        # extract row of each csv + append to tmp_avg_list
        for one_csv in csvs:
            one_csv = one_csv.values.tolist()  # convert panda DataFrame to List
            one_csv = list_unwrap(one_csv)  # unwrap list of list
            tmp_avg_list.append(one_csv[row])

        avg_list.append(st.mean(tmp_avg_list))

    print(avg_list)

