import json
import glob
import os
import pyperclip
import io
import csv
import datetime

clipboard_string = pyperclip.waitForNewPaste()
if "hardware" in clipboard_string:
    print(111)