# OT2_Data_Mining

## TODO

Data-Processing:

**gérer le fait qu'il y faut arrêter les scrips de saisie, attendre 30s... et que ce soit opaque à l'utilisateur**
**the logs are under logs/username/eventtype**
**the datasets are under datasets/**
**plot the statistic model (the one that uses euclidian distances)**

1. ✅ Remove uneccessary "press" logs when button is held (use hashmap)
2. ✅ Map press events to release events (use stack)
3. ✅ Format to : Keyname | Time-pressed | Time released | User (use pandas dataframe)
4. Aggregate the format : Average hold time, press-press time, release-press time, APM (actions per minute)
5. Add backspace counter compared to all key counter

Algo:

1. EDA
2. KNN
3. Gradient booster (XGB / LGBM)

Other todo:

- optimize more the KNN, by using grid search to find the optimal param https://towardsdatascience.com/building-a-k-nearest-neighbors-k-nn-model-with-scikit-learn-51209555453a
- one hot encode every key
- choisir le threshold pour les stats

Visualizations:

- cluster des knn pour les projections
- barchart et polar chart pour les counts des prédictions -> KNN et gradient booster
- visualization des stats (box plot, repartition) -> raw data

## Key logging

Run both scripts in 2 different terminals

`python .\keylogger.py press [Your name]`

`python .\keylogger.py release [Your name]`

Or execute directly `start.bat [Your name]` if you're using Windows

## Data preprocessing

`python .\preprocess.py [Your name]`
