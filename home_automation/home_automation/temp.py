import subprocess
import time
import os

from home_automation import system

while True:
    p = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = str(out)[7:-5]

    if os.path.exists(system.TEMPERATURE_PATH):
        with open(system.TEMPERATURE_PATH, 'w') as f:
            f.write(out)
    else:
        with open(system.TEMPERATURE_PATH, 'a') as f:
            f.write(out)

    time.sleep(5)
