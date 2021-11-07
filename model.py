from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import glob
import math
import pickle
import json

files = glob.glob("dataset/*.csv")
rows = []
dataframe = pd.DataFrame()

def compute_statistics(dataset):
    average_hold_time = dataset["hold_time"].mean()
    average_press_press_time = dataset.iloc[:len(
        dataset)-1]["press_press_time"].mean()
    average_press_release_time = dataset.iloc[:len(
        dataset)-1]["press_release_time"].mean()
    average_release_release_time = dataset.iloc[:len(
        dataset)-1]["release_release_time"].mean()
    apm = len(dataset) * 60 * math.pow(10, 6) / ((dataset.iloc[len(
        dataset)-1]["pressed"] - dataset.iloc[0]["pressed"]) / pd.Timedelta(microseconds=1))
    error_rate = len(
        dataset[dataset["key"] == "[backspace]"]) * 100 / len(dataset)
    ret = {
            "average_hold_time": average_hold_time,
            "average_press_press_time": average_press_press_time,
            "average_press_release_time": average_press_release_time,
            "average_release_release_time": average_release_release_time,
            "apm": apm,
            "error_rate": error_rate
        }
    return ret

if __name__ == "__main__":
    print("------------------------- Statistics -------------------------")
    for file in files:
        dataset = pd.read_csv(file, parse_dates=['pressed', 'released'])
        dataframe = dataframe.append(dataset)
        # Analyse statistique
        stats = compute_statistics(dataset)
        stats["user"] = dataset.iloc[0]["user"]

        print("")
        print(json.dumps(stats, sort_keys=True, indent=4))
        print("")
        print("=================================================")
        rows.append(stats)

    pd.DataFrame(rows).to_csv("statistics.csv", index=False)
    print("------------------------- Statistics -------------------------")
    print("\n")
    print("------------------------- KNN -------------------------")
    # KNN
    X = dataframe[dataframe.columns.difference(
        ['user', 'pressed', 'released', 'key'])]

    lb_make = LabelEncoder()
    dataframe['user_code'] = lb_make.fit_transform(dataframe["user"])

    print(dataframe[['user', 'user_code']].drop_duplicates())

    dataframe = dataframe.drop(columns=['user'])

    y = dataframe['user_code'].values
    #y = dataframe["user"].values
    # print(y[0:5])
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    scalerPickle = open('models/scalerpickle_file', 'wb')
    pickle.dump(scaler, scalerPickle)

    # Instantiate the model with 4 neighbors.
    knn = KNeighborsClassifier(n_neighbors=4)
    # Fit the model on the training data.
    knn.fit(X_train, y_train)
    # print(knn.predict(X_test)[0:5])
    # See how the model performs on the test data.

    knnPickle = open('models/knnpickle_file', 'wb')
    pickle.dump(knn, knnPickle)

    print(knn.score(X_test, y_test))
    print("------------------------- KNN -------------------------")
    print("\n")
    print("------------------------- GRADIENT BOOSTER -------------------------")
    gb = GradientBoostingClassifier(
        n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(X_train, y_train)
    print(gb.score(X_test, y_test))
    gbPickle = open('models/gbpickle_file', 'wb')
    pickle.dump(gb, gbPickle)
    print("------------------------- GRADIENT BOOSTER -------------------------")
