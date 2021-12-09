mode 800
start cmd /k "python .\keylogger.py press %1"
choice /t 0.3 /d y
start cmd /k "python .\keylogger.py release %1"
choice /t 0.5 /d y
start "" "typing_test.html"