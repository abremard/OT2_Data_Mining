# OT2_Data_Mining

## TODO

Data-Processing:
1) ✅ Remove uneccessary "press" logs when button is held (use hashmap)
2) ✅ Map press events to release events (use stack)
3) ✅ Format to : Keyname | Time-pressed | Time released | User (use pandas dataframe)
4) Aggregate the format : Average hold time, press-press time, release-press time, APM (actions per minute)
5) Add backspace counter compared to all key counter

Algo:
1) EDA
2) KNN
3) Gradient booster (XGB / LGBM)

## Key logging

Run both scripts in 2 different terminals

```python .\keylogger.py press```

```python .\keylogger.py release``` 

## Data preprocessing

```python .\preprocess.py [Your name]```