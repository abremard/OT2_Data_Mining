import preprocess as prp
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy.spatial import distance
from model import *

# Collect, clean and format raw data
dataframe = prp.preprocess()
X = dataframe[dataframe.columns.difference(
    ['user', 'pressed', 'released', 'key'])]

# Load model
loaded_knn = pickle.load(open('models/knnpickle_file', 'rb'))
loaded_gb = pickle.load(open('models/gbpickle_file', 'rb'))

# Statistics
stats = compute_statistics(dataframe)
clusters = pd.read_csv("statistics.csv")
stats = [*stats.values()]
for index, cluster in clusters.iterrows():
    print(cluster["user"])
    user_cluster = [*cluster.drop("user").to_dict().values()]
    dist = distance.euclidean(stats, user_cluster)
    print(dist)

# KNN
knn_result = loaded_knn.predict(X)
print(knn_result)
print(list(np.bincount(knn_result)))
certainty = max(np.bincount(knn_result)) * 100 / sum(np.bincount(knn_result))
print(certainty)
# Visualize
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
user = ['Alex', 'Stefan', 'Zihao', 'Zineb']
ax.bar(user, list(np.bincount(knn_result)))
plt.show()
# GB
gb_result = loaded_gb.predict(X)
print(gb_result)
print(list(np.bincount(gb_result)))
certainty = max(np.bincount(gb_result)) * 100 / sum(np.bincount(gb_result))
print(certainty)
# Visualize
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
user = ['Alex', 'Stefan', 'Zihao', 'Zineb']
ax.bar(user, list(np.bincount(gb_result)))
plt.show()
