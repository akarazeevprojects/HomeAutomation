import subprocess
from time import sleep

MAC = "a8:5c:2c:0b:d4:86"

if __name__ == '__main__':
    sleep(0.1)
    while True:
        p = subprocess.Popen("sudo arp-scan -l | grep {}".format(MAC), stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if output:
            print("Yay, the device is connected to your network!")
            p = subprocess.Popen("python3 /home/pi/WD/home_automation/switcher.py -d rlamp -t", stdout=subprocess.PIPE, shell=True)
            (_, _) = p.communicate()
            p_status = p.wait()
            print("On")
        else:
            print("The device is not present!")
            p = subprocess.Popen("python3 /home/pi/WD/home_automation/switcher.py -d rlamp -f", stdout=subprocess.PIPE, shell=True)
            (_, _) = p.communicate()
            p_status = p.wait()
            print("Off")
