import requests
import subprocess
import time

def detect_face():
    r = requests.get('http://192.168.0.8:5000/face')
    
    if r.status_code == 200:
        return(r.content.decode())


def main():
    while True:
        info = detect_face()
        print(info)
        if info == 'Face detected':
            p = subprocess.Popen(['python3 /home/pi/HomeAutomation/home_automation/switcher.py -d llamp -on'], shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()
            time.sleep(60)
        else:
            p = subprocess.Popen(['python3 /home/pi/HomeAutomation/home_automation/switcher.py -d llamp -off'], shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()


if __name__ == '__main__':
    main()
