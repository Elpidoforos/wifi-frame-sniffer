import subprocess
import time
import sys
from threading import Thread
import itertools
import argparse
import multiprocessing

# Get the current time
def get_current_time():
    return time.strftime("%Y%m%d_%H%M%S")

# Set the wireless interface in monitor mode
def set_mon_mode(inf_name):
    mon_mode_wlan = subprocess.run(["airmon-ng", "start", inf_name])

# Kill all running processes in regards to wireless com
def kill_run_proc_wlan():
    kill_process = subprocess.run(["airmon-ng", "check", "kill"])

# Change channel
def channel_hop():
    channel_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 36, 40, 44, 48, 52, 56,
                    60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149]
    for channel in itertools.cycle(channel_list):
        channel_change = subprocess.run(["iwconfig", "wlan0mon", "channel", str(channel)])
        time.sleep(2)

# Capture beacon requests on different channels in the wireless interface
def capture_beacons(inf_name_mon, output_fld):
    curr_time = get_current_time()
    file_name_path = output_fld + "capture_beacons" + "_" + curr_time + ".txt"
    capture_beacons = open(file_name_path, "w+")
    while(1):
            capture_beacons = subprocess.call(
                ["/usr/sbin/tcpdump", "-i", inf_name_mon, "type", "mgt", "subtype", "beacon"], stdout=capture_beacons)

# Capture beacon requests on different channels in the wireless interface
def capture_probes(inf_name_mon, output_fld):
    curr_time = get_current_time()
    file_name_path = output_fld + "capture_probes" + "_" + curr_time + ".txt"
    capture_probes = open(file_name_path, "w+")
    while(1):
        capture_probes = subprocess.call(
            ["/usr/sbin/tcpdump", "-i", inf_name_mon, "type", "mgt", "subtype", "probe-req"], stdout=capture_probes)


def create_output_folder(output_fld):
    if output_fld == None:
        create_folder = subprocess.run(
            ["mkdir", "/home/wifi-beacon-probe-logs/"])
        return "/home/wifi-beacon-probe-logs/"
    else:
        return output_fld

# The main function
def main():
    args = parse_arguments()
    inf_name = args.inf

    kill_run_proc_wlan()
    time.sleep(2)

    set_mon_mode(inf_name)
    time.sleep(2)

    inf_name_mon = inf_name + "mon"
    output_fld = create_output_folder(args.out)

    beacon_or_probe = args.frm
    if beacon_or_probe == "beacons":
        p_channel_hop = multiprocessing.Process(target=channel_hop,args=(inf_name_mon))
        p_channel_hop.start()
        p_capture_beacons = multiprocessing.Process(target=capture_beacons,args=(inf_name_mon,output_fld))
        p_capture_beacons.start()

    elif beacon_or_probe == "probes":
        p_channel_hop = multiprocessing.Process(target=channel_hop,args=(inf_name_mon))
        p_channel_hop.start()
        p_capture_probes = multiprocessing.Process(target=capture_probes,args=(inf_name_mon,output_fld))
        p_capture_probes.start()

    else:
        exit()

# The 1st argument it is  interface name, the second it is the probe or beacon request, the third argument shall be the directory to save the output files
# (the default shall be /home/wifi-beacon-probe-logs)
def parse_arguments():
    parser = argparse.ArgumentParser()
    # Adding Arguments
    parser.add_argument("--inf_name", "-i", dest="inf",
                        help="Wireless interface name", type=str, required=True)
    parser.add_argument("--beac_prob", "-f", dest="frm",
                        help="Beacon or Probe request (give probes, beacons argument input)", type=str, required=True)
    parser.add_argument("--out_fld", "-o", dest="out",
                        help="Output folder for captured logs, the default it is /home/wifi-beacon-probe-logs", type=str, required=False)
    return parser.parse_args()

def welcome_screen():
    print("\n" + "---------------------------------------------------------------"
          + "\n" + "------  Welcome to the WiFi Beacon-Probe Sniffer  -----------"
          + "\n" + "-----------------------------------------------------------\n")


if __name__ == "__main__":
    main()