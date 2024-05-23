"""
Input data: power consumption data in csv format: ../data/power
Output: power consumption plots in directory: ../plots/power

Input data name convention:
1. operation_name.csv
2. The first character of the operation name should be uppercase.


"""

from typing import Tuple, List

import pandas as pd
import matplotlib.pyplot as plt
import glob


## get all csv files in the directory:
def get_all_csv_files(directory):
    files = glob.glob(directory + "/*.csv")
    return files


def draw_each_csv_file(file_path, voltage=5, interval=200):
    data = pd.read_csv(file_path)
    title = file_path.split('/')[-1].split('.')[0]
    data['Power (W)'] = data['Reading'] * voltage
    data['Interval'] = data.index // interval
    numeric_cols = data.select_dtypes(include='number').columns
    average_power_data = data.groupby('Interval')[numeric_cols].mean()

    average_power = data['Power (W)'].mean()
    print(f'Average Power Consumption: {average_power} W')
    plt.figure(figsize=(100, 50))
    font_size = 100
    plt.plot(average_power_data.index * 0.2, average_power_data['Power (W)'],
             marker='o', linestyle='-', color='b', markersize=10, linewidth=2, label='Power (W)')
    plt.title(f'{title} Operation Power Consumption', fontsize=font_size + 20, color='black', fontweight='bold')
    plt.xlabel('Interval', fontsize=font_size)
    plt.ylabel('Average Power (W)', fontsize=font_size)
    plt.grid(True)
    # Annotate only the max and min data points
    max_value = average_power_data['Power (W)'].max()
    min_value = average_power_data['Power (W)'].min()

    max_index = average_power_data['Power (W)'].idxmax()
    min_index = average_power_data['Power (W)'].idxmin()

    plt.text(max_index * 0.2, max_value, f'{max_value:.2f}', fontsize=font_size,
             ha='right', va='bottom', color='red')
    plt.text(min_index * 0.2, min_value, f'{min_value:.2f}', fontsize=font_size,
             ha='right', va='bottom', color='green')

    plt.xticks(fontsize=font_size - 20)
    plt.yticks(fontsize=font_size - 20)
    plt.savefig(f'../plots/power/{title}.png')
    return title, average_power


def draw_average_power_consumption(operations: List[Tuple[str, float]]):
    plt.figure(figsize=(100, 50))
    font_size = 100
    for operation in operations:
        print(operation[0], operation[1])
        plt.bar(operation[0], operation[1], color='r', label='Power (W)', alpha=0.7)
    plt.title('Average Power Consumption', fontsize=font_size + 20, color='black', fontweight='bold')
    plt.xlabel('Operation', fontsize=font_size)
    plt.ylabel('Average Power (W)', fontsize=font_size)
    plt.grid(True)
    plt.xticks(fontsize=font_size - 20)
    plt.yticks(fontsize=font_size - 20)
    plt.savefig('../plots/power/average_power.png')


if __name__ == '__main__':
    files = get_all_csv_files('../data/power')
    list_of_operations = []
    for file in files:
        title, average_power = draw_each_csv_file(file)
        list_of_operations.append((title, average_power))
    draw_average_power_consumption(list_of_operations)
    print('All files have been processed.')
