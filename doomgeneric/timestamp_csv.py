import subprocess
import csv
import signal
import sys
import argparse
import os
import time

output_data = []
start_time = None

def signal_handler(sig, frame):
    with open("output.csv", "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp (ns)"])
        csv_writer.writerows([[timestamp] for timestamp in output_data])
    print("\nData saved to output.csv")
    sys.exit(0)

def run_subprocess(command, filter_word):
    global start_time

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True, shell=True)

    for line in process.stdout:
        if line and filter_word in line:
            if start_time is None:
                start_time = time.time_ns()
            timestamp = time.time_ns() - start_time
            output_data.append(timestamp)
    
    process.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a subprocess and log timestamps in nanoseconds for lines containing a specific word.")
    parser.add_argument("command", help="The command to run as a subprocess.")
    parser.add_argument("filter_word", help="The word to filter the output by.")
    args = parser.parse_args()

    command_path = os.path.dirname(os.path.abspath(args.command))
    os.chdir(command_path)

    signal.signal(signal.SIGINT, signal_handler)
    run_subprocess(args.command, args.filter_word)
