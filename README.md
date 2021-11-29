# Data Mining and Analytics Project

This project explores the topic of keyboard dynamics and their application in the identification of users using keystroke patterns. The project contains a keylogger for data acquisition, as well as multiple methods of data evaluation. Furthermore, multiple ML models are implemented for the purpose of identification of a user using typing patterns, as well as a practical example.

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
Project realized by Alexandre Bremard, Zineb Fadili, Zihao Hua, Stefan Ristovski
## License
[MIT](https://choosealicense.com/licenses/mit/)