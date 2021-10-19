import glob
import pandas as pd
import sys

from datetime import datetime

if __name__ == "__main__":

    press_files = glob.glob("press/*.txt")
    press_rows = []

    release_files = glob.glob("release/*.txt")
    release_rows = []

    for press_file in press_files:
        with open(press_file) as fp:
            line = fp.readline()
            while line:
                timestamp = datetime.strptime(line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1]
                press_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    for release_file in release_files:
        with open(release_file) as fp:
            line = fp.readline()
            while line:
                timestamp = datetime.strptime(line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1]
                release_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    press_df = pd.DataFrame(press_rows)
    release_df = pd.DataFrame(release_rows)

    print(press_df)
    print(release_df)

    # Map release -> press and build dataset
    dataset_rows = []
    for id, row in release_df.drop_duplicates(subset=['key']).iterrows():
        sub_df = release_df[release_df["key"] == row['key']]
        print(sub_df)
        lower_bound = None       
        for sub_id, sub_row in sub_df.reset_index().iterrows():
            higher_bound = sub_row["timestamp"]
            if sub_id == 0:
                press_time = press_df[(press_df["key"] == sub_row["key"]) & (press_df["timestamp"] < higher_bound)].iloc[0]["timestamp"]
            else:
                press_time = press_df[(press_df["key"] == sub_row["key"]) & (press_df["timestamp"] < higher_bound) & (press_df["timestamp"] > lower_bound)].iloc[0]["timestamp"]
            lower_bound = higher_bound
            dataset_rows.append({
                "key": sub_row["key"],
                "pressed": press_time,
                "released": sub_row["timestamp"],
                "user": sys.argv[1]
            })

    dataset = pd.DataFrame(dataset_rows)
    print(dataset)
    dataset.sort_values(['pressed']).to_csv("dataset.csv", index=False, date_format='%Y-%m-%d %H:%M:%S %f')
