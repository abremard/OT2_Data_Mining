# Data Mining and Analytics Project

This project explores the topic of keyboard dynamics and their application in the identification of users using keystroke patterns. The project contains a keylogger for data acquisition, as well as multiple methods of data evaluation. Furthermore, multiple ML models are implemented for the purpose of identification of a user using typing patterns, as well as a distance-based statistical analysis approach. Finally, a practcal example is included showing the combination of these approaches in an user authentication system.

Three main research questions are being explored in this project:

- Which metric is the most interesting to identify a user using keystroke dynamics? - Hold Time, Press-Press Time, Press-Release Time.
- How to define a user's signature using keystroke dynamics? - Using classifying ML agorithms, like Random Forest Classifier or Gradient Boosting.
- How to detect an intruder in a keystroke dynamics authentication system? - Using statistical analysis, using a distance-based approach in combination with the ML algorithms.

These questions are expored and answered in-depth in the report contained in the main notebook of the project.

### Scientific Sources

- M. Karnan, M. Akila and N. Krishnaraj, “Biometric personal authentication using keystroke dynamics: A review,” (online) Applied Soft Computing, vol. 11, no. 2, March 2011, p. 1565-1573. Available on: https://www.sciencedirect.com/science/article/abs/pii/S156849461000205X
- J. Ilonen, "Keystroke dynamics," (online) Advanced Topics in Information processing–lecture, 2003. Available on: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.99.9014&rep=rep1&type=pdf
- K. Shenoy, “Keystroke Dynamics Analysis and Prediction,” (online) on Medium, January 18th, 2021. Available on: https://towardsdatascience.com/keystroke-dynamics-analysis-and-prediction-part-1-eda-3fe2d25bac04

## Keylogger

There are multiple ways to run the keylogger included in this project for the purposes of data acquisition.

On a windows machine, please use the following command to launch the keylogger (instantly for press and release events):

```bash
./start.bat [Your Name]
```

Alternatively, use the following commands in separate terminals to launch the press and release event loggers separately:

```bash
python .\keylogger.py press [Your name]

python .\keylogger.py release [Your name]
```

The files will be saved in the /logs/yourname folder. You can modify the parameters of recording keystrokes in the keylogger.py file by changing the following values:

```python
#Time interval for saving a single log file
SEND_REPORT_EVERY = 10 # in seconds, 60 means 1 minute and so on
#Total time of keylogging
INTERRUPT_AFTER = 300 # in seconds, 60 means 1 minute and so on
```

## Usage

The entirety of the code for the project (excluding the keylogger) can be found and executed on the Notebook contained in the project (main.ipynb)

## Credits

Project realized by Alexandre Bremard, Zineb Fadili, Zihao Hua, Stefan Ristovski.

## License

[MIT](https://choosealicense.com/licenses/mit/)
