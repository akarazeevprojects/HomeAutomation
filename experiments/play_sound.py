import subprocess
import time

player = subprocess.Popen(["mplayer", "song.mp3", "-ss", "30"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(5)

player.stdin.write("q")
