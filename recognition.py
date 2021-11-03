import preprocess as prp
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Collect, clean and format raw data
dataframe = prp.preprocess()
X = dataframe[dataframe.columns.difference(
    ['user', 'pressed', 'released', 'key'])]

# Load model
loaded_knn = pickle.load(open('models/knnpickle_file', 'rb'))
loaded_gb = pickle.load(open('models/gbpickle_file', 'rb'))
# Predict
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
