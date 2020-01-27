import subprocess
import time
import sys
from threading import Thread
import itertools

# The 1st argument it is  inf name, the second it is the.......
args = sys.argv

# Set the wireless interface in monitor mode


def set_mon_mode(inf_name):
    mon_mode_wlan = subprocess.run(["airmon-ng", "start", inf_name])

# Kill all running processes in regards to wireless com


def kill_run_proc_wlan():
    kill_process = subprocess.run(["airmon-ng", "check", "kill"])

# Change channel


def channel_hop():
    print("Inside Channel Hop")
    channel_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 36, 40, 44, 48, 52, 56,
                    60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149]

    if args[2] == "probe":
        for channel in itertools.cycle(channel_list):
            channel_change = subprocess.run(
                ["iwconfig", "wlan0mon", "channel", str(channel)])
            time.sleep(2)

    else:
        for channel in itertools.cycle(channel_list):
            channel_change = subprocess.run(
                ["iwconfig", "wlan0mon", "channel", str(channel)])
            time.sleep(5)

# Capture beacon requests on different channels in the wireless interface


def capture_beacons(inf_name_mon):
    capture_beacons = open("/tmp/capture_beacons.txt", "w+")
    while(1):
        capture_beacons = subprocess.call(
            ["/usr/sbin/tcpdump", "-i", inf_name_mon, "type", "mgt", "subtype", "beacon"], stdout=capture_beacons)
        # print(capture_beacons)

# Capture beacon requests on different channels in the wireless interface


def capture_probes(inf_name_mon):
    capture_probes = open("/tmp/capture_probes.txt", "w+")
    while(1):
        #capture_probes = subprocess.run(["/usr/sbin/tcpdump", "-i", inf_name_mon, "type", "mgt", "subtype", "probe-req"])
        capture_probes = subprocess.call(
            ["/usr/sbin/tcpdump", "-i", inf_name_mon, "type", "mgt", "subtype", "probe-req"], stdout=capture_probes)


def main():

    kill_run_proc_wlan()
    time.sleep(5)

    inf_name = args[1]
    set_mon_mode(inf_name)
    time.sleep(2)
    inf_name_mon = inf_name + "mon"

    beacon_or_probe = args[2]
    if beacon_or_probe == "beacon":
        Thread(target=channel_hop).start()
        Thread(target=capture_beacons(inf_name_mon)).start()

    elif beacon_or_probe == "probe":
        Thread(target=channel_hop).start()
        Thread(target=capture_probes(inf_name_mon)).start()

    else:
        exit()


if __name__ == "__main__":
    main()
