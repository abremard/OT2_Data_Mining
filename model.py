from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

import pandas as pd
import glob
import math

files = glob.glob("dataset/*.csv")
rows = []
dataframe = pd.DataFrame()

for file in files:
    dataset = pd.read_csv(file, parse_dates=['pressed', 'released'])
    dataframe = dataframe.append(dataset)
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
    error_rate = len(
        dataset[dataset["key"] == "[backspace]"]) * 100 / len(dataset)

    print("")
    print("USER - {}".format(dataset.iloc[0]["user"]))
    print("average_hold_time", average_hold_time)
    print("average_press_press_time", average_press_press_time)
    print("average_press_release_time", average_press_release_time)
    print("average_release_release_time", average_release_release_time)
    print("apm", apm)
    print("error_rate", error_rate)
    print("")
    print("=================================================")

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

# Instantiate the model with 4 neighbors.
knn = KNeighborsClassifier(n_neighbors=4)
# Fit the model on the training data.
knn.fit(X_train, y_train)
# print(knn.predict(X_test)[0:5])
# See how the model performs on the test data.
print(knn.score(X_test, y_test))
