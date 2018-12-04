import time
import os
import paho.mqtt.client as mqtt

data_path = "/home/jnct/dev/mesh/data"
filename = "temp_avg_21471.txt"
file_path = os.path.join(data_path, filename)

verdict_filename = "verdict_light.txt"
verdict_path = os.path.join(data_path, verdict_filename)

rip = "10.100.60.17"

client = mqtt.Client()
client.connect(rip, 1883, 60)
client.loop_start()

t = 50

print('Script is running, press Ctrl-C to quit...')
while True:
    time.sleep(0.1)

    with open(verdict_path, 'r') as f:
        verdict = f.read()
        verdict = float(verdict)
    #temp = t
    #t %= 30
    #t += 10

    if verdict < 0.:
        t -= 3
    elif verdict > 0:
        t += 3

    if t >= 100:
        t = 100
    elif t <= 0:
        t = 0

    #t += 1
    #t %= 100

    client.publish('/light', t)
    print('Verdict is {}, {}'.format(verdict, t))
