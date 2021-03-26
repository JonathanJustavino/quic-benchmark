import pandas as pd
from pathlib import Path


def dataloader(impport_path):
    # get all measurement folders
    all_folders = sorted(import_path.glob('*'))

    # collect pcaps with 10 packets in one list
    pcaps_10 = []
    for folder in all_folders:
        curr_csv = pd.read_csv(import_path / folder / 'timestamps.csv', header=None)

        # drop csv folders with 11 packets
        if len(curr_csv) == 10:
            pcaps_10.append(curr_csv)

    return pcaps_10

if __name__ == '__main__':

    import_path = Path(
        '/home/amelie/Uni/RNP_Komplexpraktikum/quic-benchmark/measurements/samples_threshold5_dev2_delay0/quic/remote/')

    pcaps = dataloader(import_path)
    print(len(pcaps))



#    df = pd.read_csv(import_path / '2021-03-08 08-21-15.964770' / 'timestamps.csv', header=None, sep='\t',
#                     index_col=False)
#    print(df)
#    print(len(df))
