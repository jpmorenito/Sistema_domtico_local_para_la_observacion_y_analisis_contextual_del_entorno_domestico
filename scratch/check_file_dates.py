import os
import datetime

files = [
    "c:/Users/jacob/Downloads/TFG/pi_automations.yaml",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-nodo-ambiente.yaml",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-escritorio.yaml",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-puerta.yaml"
]

for f in files:
    if os.path.exists(f):
        mtime = os.path.getmtime(f)
        dt = datetime.datetime.fromtimestamp(mtime)
        print(f"{f.split('/')[-1]}: modified on {dt} ({os.path.getsize(f)} bytes)")
