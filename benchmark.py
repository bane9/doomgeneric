import asyncio
import subprocess
import time
import argparse
import csv
from datetime import datetime
import psutil
import numpy as np

def get_filename(test_type):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{test_type}_{now}.csv"

async def run_and_time_program(program, iterations=15):
    timings = []
    previous_time = None
    for i in range(iterations):
        print(f"Run {i + 1} of {iterations}...", end=" ")
        process = await asyncio.create_subprocess_exec(
            *program.split(),
            stdout=subprocess.PIPE,
        )

        while True:
            output = await process.stdout.readline()
            if b"Run /init as init process" in output:
                current_time = time.time() * 1000
                if previous_time is not None:
                    time_diff = current_time - previous_time
                    print(f"Time taken: {time_diff:.2f} ms")
                    timings.append(time_diff)
                previous_time = current_time
                break

        process.kill()

    filename = get_filename('timing_results')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Time (ms)"])
        for i, timing in enumerate(timings, start=2):
            writer.writerow([i, timing])

async def run_and_record_memory(program, iterations=10):
    memory_usages = []
    for i in range(iterations):
        print(f"Run {i + 1} of {iterations}...", end=" ")
        process = await asyncio.create_subprocess_exec(
            *program.split(),
            stdout=subprocess.PIPE,
        )
        util = psutil.Process(process.pid)

        doom_draw_count = 0

        while True:
            output = await process.stdout.readline()
            if b"doom_draw" in output:
                doom_draw_count += 1
                if doom_draw_count == 5:
                    memory_info = util.memory_full_info()
                    usage = memory_info.rss
                    human = psutil._common.bytes2human(usage)
                    print(f"Memory usage: {usage} bytes ({human})")
                    memory_usages.append(usage)

                    break

        process.kill()

    filename = get_filename('memory_usage_results')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Memory Usage (bytes)"])
        for i, memory_usage in enumerate(memory_usages, start=1):
            writer.writerow([i, memory_usage])

async def run_and_record_timestamps(program, occurrences=100, repeats=15):
    averaged_timestamps = []

    for repeat in range(repeats):
        doom_draw_timestamps = []
        previous_timestamp = None

        process = await asyncio.create_subprocess_exec(
            *program.split(),
            stdout=subprocess.PIPE,
        )
        start_time = datetime.now()
        doom_draw_count = 0

        while doom_draw_count < occurrences:
            output = await process.stdout.readline()
            if b"doom_draw" in output:
                current_timestamp = datetime.now()
                if previous_timestamp is not None:
                    time_diff = (current_timestamp - previous_timestamp).total_seconds() * 1e3 
                    doom_draw_timestamps.append(time_diff)
                previous_timestamp = current_timestamp
                doom_draw_count += 1
                print(f"Repeat {repeat + 1}/{repeats}: Captured {doom_draw_count}/{occurrences} 'doom_draw' occurrences")

        process.kill()

        average_timestamp = np.mean(doom_draw_timestamps)
        averaged_timestamps.append(average_timestamp)
        print(f"Repeat {repeat + 1}/{repeats}: Averaged timestamp {average_timestamp:.2f} ms")

    filename = get_filename('doom_draw_timestamps')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Repeat", "Timestamp (ms)"])
        for i, avg_timestamp in enumerate(averaged_timestamps, start=1):
            writer.writerow([i, avg_timestamp])

    print(f"Averaged timestamps recorded in {filename}")

def main():
    parser = argparse.ArgumentParser(description="Benchmarking script for RISC-V emulator.")
    parser.add_argument("program", help="The emulator program to run, e.g., 'start-emu.sh'")
    args = parser.parse_args()

    while True:
        print("Choose an option:")
        print("1. Measure time to 'Run /init as init process'")
        print("2. Measure memory usage after fifth 'doom_draw'")
        print("3. Record timestamps of 'doom_draw'")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            asyncio.run(run_and_time_program(args.program))
        elif choice == "2":
            asyncio.run(run_and_record_memory(args.program))
        elif choice == "3":
            asyncio.run(run_and_record_timestamps(args.program))
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
