import subprocess
import time
import itertools

# Change channel
def channel_hop():
    channel_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 36, 40, 44, 48, 52, 56,
                    60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149]

    for channel in itertools.cycle(channel_list):
        channel_change = subprocess.run(["iwconfig", "wlan0mon", "channel", str(channel)])
        time.sleep(2)

channel_hop()