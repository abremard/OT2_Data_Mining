import glob
import pandas as pd
import sys
import math

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def preprocess(user=None):
    """
        This script will pre-process the raw data collected by the keylogger.py script, the steps are as follows:
        1) parse each press and release .txt files by reading the events sequentially
        2) map each released event to its pressed event
        3) extract features such as "press_press_time", "press_release_time", "release_release_time"
        4) run some statistics that describe the behavior of the user
    """

    # Collect .txt keylogs paths
    press_files = glob.glob(f"logs/{user}/press/*.txt")
    release_files = glob.glob(f"logs/{user}/release/*.txt")
    # Initialize array to concatenate press and release events
    press_rows = []
    release_rows = []

    # Parse press keylogs
    for press_file in press_files:
        with open(press_file) as fp:
            line = fp.readline()
            while line:
                # Handle linebreak exception 
                if line == "\n":
                    line = fp.readline()
                    continue
                # extract event's timestamp and key
                timestamp = datetime.strptime(line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1].lower()
                press_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    # Parse release keylogs
    for release_file in release_files:
        with open(release_file) as fp:
            line = fp.readline()
            while line:
                # Handle linebreak exception 
                if line == "\n":
                    line = fp.readline()
                    continue
                # extract event's timestamp and key
                timestamp = datetime.strptime(line.strip().split(" - ")[0], '%Y-%m-%d %H:%M:%S %f')
                key = line.strip().split(" - ")[1].lower()
                release_rows.append({
                    "timestamp": timestamp,
                    "key": key
                })
                line = fp.readline()

    # Convert arrays to dataframes for easier manipulation
    press_df = pd.DataFrame(press_rows)
    release_df = pd.DataFrame(release_rows)

    # Optional : debug press/release dataframes
    press_df.to_csv("press_df.csv", date_format="%Y-%m-%d %H:%M:%S %f")
    release_df.to_csv("release_df.csv", date_format="%Y-%m-%d %H:%M:%S %f")

    # Map release events to their corresponding press event
    dataset_rows = []
    # The mapping will be done key by key.
    # For example we will map all "[SPACE]" keys together before mapping "e" keys
    for _, row in release_df.drop_duplicates(subset=['key']).iterrows():
        # sub_df contains all release events recorded for key {row['key']}
        sub_df = release_df[release_df["key"] == row['key']]
        # lower_bound is a time-cursor that records the last known release event timestamp
        lower_bound = None
        for sub_id, sub_row in sub_df.reset_index().iterrows():
            try:
                # higher_bound runs through the latest release event timestamp
                higher_bound = sub_row["timestamp"]
                if sub_id == 0:
                    # match the release event to the press event
                    # when a user holds a key for a long amount of time, the keylogger will records multiple press events, so we will keep only the first press event timestamp
                    press_time = press_df[(press_df["key"] == sub_row["key"]) & (press_df["timestamp"] < higher_bound)].iloc[0]["timestamp"]
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

    # Features extraction

    # Hold time is computed on the whole columns rather than row by row
    dataset["hold_time"] = (dataset["released"] - dataset["pressed"]) / pd.Timedelta(microseconds=1)

    # press_press_time, press_release_time, release_release_time are computed row by row
    press_press_time = []
    press_release_time = []
    release_release_time = []

    for index, row in dataset.reset_index().iterrows():
        # press_press_time is the time between 2 consecutive press events
        press_press_delta = (dataset.iloc[index+1]["pressed"] - dataset.iloc[index]["pressed"]) / pd.Timedelta(microseconds=1)
        press_press_time.append(press_press_delta)
        # release_release_time is the time between 2 consecutive release events
        release_release_delta = (dataset.iloc[index+1]["released"] - dataset.iloc[index]["released"]) / pd.Timedelta(microseconds=1)
        release_release_time.append(release_release_delta)
        # press_release_time is the time between the previous release event and the current press event
        press_release_delta = (dataset.iloc[index+1]["pressed"] - dataset.iloc[index]["released"]) / pd.Timedelta(microseconds=1)
        press_release_time.append(press_release_delta)

        if index == len(dataset) - 2:
            press_press_time.append(0)
            press_release_time.append(0)
            release_release_time.append(0)
            break

    # Add features to final dataset
    dataset["press_press_time"] = press_press_time
    dataset["press_release_time"] = press_release_time
    dataset["release_release_time"] = release_release_time

    # Run some user-based statistics
    average_hold_time = dataset["hold_time"].mean()
    average_press_press_time = dataset.iloc[:len(dataset)-1]["press_press_time"].mean()
    average_press_release_time = dataset.iloc[:len(dataset)-1]["press_release_time"].mean()
    average_release_release_time = dataset.iloc[:len(dataset)-1]["release_release_time"].mean()
    # User's action per minute
    apm = len(dataset) * 60 * math.pow(10, 6) / ((dataset.iloc[len(dataset)-1]["pressed"] - dataset.iloc[0]["pressed"]) / pd.Timedelta(microseconds=1))

    print("average_hold_time", average_hold_time)
    print("average_press_press_time", average_press_press_time)
    print("average_press_release_time", average_press_release_time)
    print("average_release_release_time", average_release_release_time)
    print("apm", apm)

    # Save dataset as a .csv file that will be used for Data Mining
    dataset[:-1].to_csv("dataset.csv", index=False)

    return dataset


if __name__ == "__main__":
    dataframe = preprocess(sys.argv[1])
