import subprocess
import time

while True:
    p = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = str(output)[7:-5]
    with open('temp.txt', 'w') as f:
        f.write(output)
    time.sleep(5)
