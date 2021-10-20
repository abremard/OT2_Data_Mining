mkdir press
mkdir release
start cmd /k "python .\keylogger.py press"
choice /t 0.5 /d y
start cmd /k "python .\keylogger.py release"