mkdir press
mkdir release
start cmd /k "python .\keylogger.py press %1"
choice /t 0.5 /d y
start cmd /k "python .\keylogger.py release %1"