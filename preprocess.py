import glob
import pandas as pd
import sys
import math

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def preprocess(user=None):
    press_files = glob.glob(f"logs/{user}/press/*.txt")
    press_rows = []

    release_files = glob.glob(f"logs/{user}/release/*.txt")
    release_rows = []

    for press_file in press_files:
        with open(press_file) as fp:
            line = fp.readline()
            while line:
                if line == "\n":
                    line = fp.readline()
                    continue
                timestamp = datetime.strptime(
                    line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1].lower()
                press_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    for release_file in release_files:
        with open(release_file) as fp:
            line = fp.readline()
            while line:
                if line == "\n":
                    line = fp.readline()
                    continue
                timestamp = datetime.strptime(
                    line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1].lower()
                release_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    press_df = pd.DataFrame(press_rows)
    release_df = pd.DataFrame(release_rows)

    press_df.to_csv("press_df.csv", date_format="%Y-%m-%d %H:%M:%S %f")
    release_df.to_csv("release_df.csv", date_format="%Y-%m-%d %H:%M:%S %f")

    # Map release -> press and build dataset
    dataset_rows = []
    for _, row in release_df.drop_duplicates(subset=['key']).iterrows():
        sub_df = release_df[release_df["key"] == row['key']]
        lower_bound = None
        for sub_id, sub_row in sub_df.reset_index().iterrows():
            try:
                higher_bound = sub_row["timestamp"]
                if sub_id == 0:
                    press_time = press_df[(press_df["key"] == sub_row["key"]) & (
                        press_df["timestamp"] < higher_bound)].iloc[0]["timestamp"]
                else:
                    press_time = press_df[(press_df["key"] == sub_row["key"]) & (press_df["timestamp"] < higher_bound) & (press_df["timestamp"] > lower_bound)].iloc[0]["timestamp"]
                lower_bound = higher_bound
                dataset_rows.append({
                    "key": sub_row["key"],
                    "pressed": press_time,
                    "released": sub_row["timestamp"],
                    "user": user
                })
            except:
                continue

    dataset = pd.DataFrame(dataset_rows).sort_values(['pressed'])
    dataset.to_csv("tmp_dataset.csv", date_format="%Y-%m-%d %H:%M:%S %f")

    dataset["hold_time"] = (dataset["released"] -
                            dataset["pressed"]) / pd.Timedelta(microseconds=1)
    press_press_time = []
    press_release_time = []
    release_release_time = []

    for index, row in dataset.reset_index().iterrows():
        press_press_delta = (dataset.iloc[index+1]["pressed"] -
                             dataset.iloc[index]["pressed"]) / pd.Timedelta(microseconds=1)
        press_press_time.append(press_press_delta)
        release_release_delta = (
            dataset.iloc[index+1]["released"] - dataset.iloc[index]["released"]) / pd.Timedelta(microseconds=1)
        release_release_time.append(release_release_delta)
        press_release_delta = (
            dataset.iloc[index+1]["pressed"] - dataset.iloc[index]["released"]) / pd.Timedelta(microseconds=1)
        press_release_time.append(press_release_delta)

        if index == len(dataset) - 2:
            press_press_time.append(0)
            press_release_time.append(0)
            release_release_time.append(0)
            break

    dataset["press_press_time"] = press_press_time
    dataset["press_release_time"] = press_release_time
    dataset["release_release_time"] = release_release_time

    # Analyse statistique
    average_hold_time = dataset["hold_time"].mean()
    average_press_press_time = dataset.iloc[:len(
        dataset)-1]["press_press_time"].mean()
    average_press_release_time = dataset.iloc[:len(
        dataset)-1]["press_release_time"].mean()
    average_release_release_time = dataset.iloc[:len(
        dataset)-1]["release_release_time"].mean()
    apm = len(dataset) * 60 * math.pow(10, 6) / ((dataset.iloc[len(
        dataset)-1]["pressed"] - dataset.iloc[0]["pressed"]) / pd.Timedelta(microseconds=1))

    print("average_hold_time", average_hold_time)
    print("average_press_press_time", average_press_press_time)
    print("average_press_release_time", average_press_release_time)
    print("average_release_release_time", average_release_release_time)
    print("apm", apm)

    dataset[:-1].to_csv("dataset.csv", index=False)

    return dataset


if __name__ == "__main__":
    dataframe = preprocess(sys.argv[1])
