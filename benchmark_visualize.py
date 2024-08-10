import csv
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def annotate_extremes(ax, x, y, color, unit):
    max_value = max(y)
    min_value = min(y)
    max_idx = y.index(max_value)
    min_idx = y.index(min_value)
    difference = max_value - min_value

    ax.annotate(f'Maks: {max_value:.2f}{unit}', xy=(x[max_idx], max_value), xytext=(0, 10),
                textcoords='offset points', ha='center', va='bottom', color=color, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=color))

    ax.annotate(f'Min: {min_value:.2f}{unit}', xy=(x[min_idx], min_value), xytext=(0, -15),
                textcoords='offset points', ha='center', va='top', color=color, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=color))

    return difference

def place_diff_annotations(ax, diffs, colors, unit):
    y_base = 0.95
    y_step = 0.05
    
    for i, (diff, color) in enumerate(zip(diffs, colors)):
        y_pos = y_base - i * y_step
        ax.annotate(f'Razlika: {diff:.2f}{unit}', xy=(1.02, y_pos), xycoords='axes fraction', ha='left', va='center', color=color, fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor=color, facecolor="white"))

def calculate_percentage_differences(values):
    percentages = []
    for i, val1 in enumerate(values):
        for j, val2 in enumerate(values):
            if i < j:
                percentage_diff = 100 * (val2 - val1) / val1 if val1 != 0 else 0
                percentages.append((i, j, percentage_diff))
    return percentages

def visualize_timing_results(filenames):
    plt.figure(figsize=(10, 6))
    
    diffs = []
    colors = []
    
    for filename in filenames:
        data = read_csv(filename)
        times = [float(row['Time (ms)']) for row in data]
        run_numbers = range(1, len(times) + 1)

        scatter = plt.scatter(run_numbers, times, label=filename.replace(".csv", "").replace("timing_results_", "").replace("_", " "))
        color = scatter.get_edgecolor()
        diff = annotate_extremes(plt.gca(), list(run_numbers), times, color, "ms")
        diffs.append(diff)
        colors.append(color)
    
    place_diff_annotations(plt.gca(), diffs, colors, "ms")
    
    plt.title('Raspršeni Dijagram Rezultata Merenja Vremena')
    plt.xlabel('Broj Pokretanja')
    plt.ylabel('Vreme (s)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    
    average_times = []
    labels = []
    
    for filename in filenames:
        data = read_csv(filename)
        times = [float(row['Time (ms)']) for row in data]
        average_time = np.mean(times)
        average_times.append(average_time)
        label = filename.replace(".csv", "").replace("timing_results_", "").replace("_", " ")
        labels.append(label)
        plt.bar(label, average_time)
    
    percentage_differences = calculate_percentage_differences(average_times)
    
    text_to_add = ""
    for i, j, percentage_diff in percentage_differences:
        text_to_add += f'{labels[i]} u poređenju sa {labels[j]}: {percentage_diff:.2f}%\n'
    
    plt.title('Prosečno Vreme')
    plt.ylabel('Vreme (ms)')
    plt.xlabel(f'Platforma\n{text_to_add}')
    plt.grid(True)
    plt.show()

def visualize_memory_usage(filenames):
    plt.figure(figsize=(10, 6))
    
    diffs = []
    colors = []
    
    for filename in filenames:
        data = read_csv(filename)
        memory_usages = [int(row['Memory Usage (bytes)']) / (1024 * 1024) for row in data]
        run_numbers = range(1, len(memory_usages) + 1)

        scatter = plt.scatter(run_numbers, memory_usages, label=filename.replace(".csv", "").replace("memory_usage_results_", "").replace("_", " "))
        color = scatter.get_edgecolor()
        diff = annotate_extremes(plt.gca(), list(run_numbers), memory_usages, color, "MB")
        diffs.append(diff)
        colors.append(color)
    
    place_diff_annotations(plt.gca(), diffs, colors, "MB")
    
    plt.title('Raspršeni Dijagram Rezultata Korišćenja Memorije')
    plt.xlabel('Broj Pokretanja')
    plt.ylabel('Korišćenje Memorije (MB)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    
    average_memory_usages = []
    labels = []
    
    for filename in filenames:
        data = read_csv(filename)
        memory_usages = [int(row['Memory Usage (bytes)']) / (1024 * 1024) for row in data]
        average_memory_usage = np.mean(memory_usages)
        average_memory_usages.append(average_memory_usage)
        label = filename.replace(".csv", "").replace("memory_usage_results_", "").replace("_", " ")
        labels.append(label)
        plt.bar(label, average_memory_usage)
    
    percentage_differences = calculate_percentage_differences(average_memory_usages)
    
    text_to_add = ""
    for i, j, percentage_diff in percentage_differences:
        text_to_add += f'{labels[i]} u poređenju sa {labels[j]}: {percentage_diff:.2f}%\n'
    
    plt.title('Prosečno Korišćenje Memorije')
    plt.ylabel('Korišćenje Memorije (MB)')
    plt.xlabel(f'Platforma\n{text_to_add}')
    plt.grid(True)
    plt.show()

def visualize_timestamps(filenames):
    plt.figure(figsize=(10, 6))
    
    diffs = []
    colors = []
    
    for filename in filenames:
        data = read_csv(filename)
        timestamps = [float(row['Timestamp (ms)']) for row in data]
        occurrences = range(1, len(timestamps) + 1)

        scatter = plt.scatter(occurrences, timestamps, label=filename.replace(".csv", "").replace("doom_draw_timestamps_", "").replace("_", " "))
        color = scatter.get_edgecolor()
        diff = annotate_extremes(plt.gca(), list(occurrences), timestamps, color, "ms")
        diffs.append(diff)
        colors.append(color)
    
    place_diff_annotations(plt.gca(), diffs, colors, "ms")
    
    plt.title('Raspršeni Dijagram Vremenskih Oznaka Izvršavanja Frejm-ova')
    plt.xlabel('Broj Pokretanja')
    plt.ylabel('Vreme Izvršavanja Frejm-ova (ms)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    
    average_timestamps = []
    labels = []
    
    for filename in filenames:
        data = read_csv(filename)
        timestamps = [float(row['Timestamp (ms)']) for row in data]
        average_timestamp = np.mean(timestamps)
        average_timestamps.append(average_timestamp)
        label = filename.replace(".csv", "").replace("doom_draw_timestamps_", "").replace("_", " ")
        labels.append(label)
        plt.bar(label, average_timestamp)
    
    percentage_differences = calculate_percentage_differences(average_timestamps)
    
    text_to_add = ""
    for i, j, percentage_diff in percentage_differences:
        text_to_add += f'{labels[i]} u poređenju sa {labels[j]}: {percentage_diff:.2f}%\n'
    
    plt.title('Prosečno Vreme Izvršavanja Frejm-ova')
    plt.xlabel(f'Platforma\n{text_to_add}')
    plt.ylabel('Vreme Izvršavanja Frejm-ova (ms)')
    plt.grid(True)
    plt.show()

def find_csv_files(pattern):
    return glob(pattern)

def main():
    timing_files = find_csv_files('timing_results_*.csv')
    memory_files = find_csv_files('memory_usage_results_*.csv')
    timestamp_files = find_csv_files('doom_draw_timestamps_*.csv')

    if timing_files:
        print(f"Pronađeno {len(timing_files)} fajlova sa rezultatima merenja vremena.")
        visualize_timing_results(timing_files)
    else:
        print("Nema fajlova sa rezultatima merenja vremena.")

    if memory_files:
        print(f"Pronađeno {len(memory_files)} fajlova sa rezultatima korišćenja memorije.")
        visualize_memory_usage(memory_files)
    else:
        print("Nema fajlova sa rezultatima korišćenja memorije.")

    if timestamp_files:
        print(f"Pronađeno {len(timestamp_files)} fajlova sa vremenskim oznakama doom_draw.")
        visualize_timestamps(timestamp_files)
    else:
        print("Nema fajlova sa vremenskim oznakama doom_draw.")

if __name__ == "__main__":
    main()
