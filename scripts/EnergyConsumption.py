"""
Calculate the power consumption in unit of J
"""
import pandas as pd
from scipy import integrate


def cal_lock_unlock(file_path):
    """
    The start and end point are determined by Original Pro software.
    begin: 940
    end: 6380
    :param file_path:
    :return:
    """
    data = pd.read_csv(file_path)
    data = data[940:6380]
    data['Power (W)'] = data['Reading'] * 5
    x = range(0, 6380 - 940)
    print((6380 - 940) / 1000, 's')
    return integrate.simps(data['Power (W)'], x) / 1000


def cal_gps(file_path):
    data = pd.read_csv(file_path)
    data['Power (W)'] = data['Reading'] * 5
    x = range(len(data))
    return integrate.simps(data['Power (W)'], x) / 1000 * 2


def low_demand():
    """
    1: once of lock, 5.44 seconds
    2: seconds of gps: 20 seconds
    capacity of battery: 2.29 * 3600 J
    :return:
    """
    print("Low Demand")
    total = 3600
    lock = 5.44
    lock_time = 0
    gps_time = 0
    normal = (total - lock * lock_time) * 0.6
    energy = normal + 3.9228 * lock_time + 13.5396 * gps_time
    cap = 2.29 * 3600
    print("Energy", energy)
    print(cap / energy)


def high_demand():
    """
    1. 10 times of lock, 5.44 seconds
    2. 4 times of gps: 20 seconds

    :return:
    """
    print("High Demand")
    total = 3600
    lock = 5.44
    lock_time = 10
    gps_time = 12
    normal = (total - lock * lock_time) * 0.6
    energy = normal + 3.9228 * lock_time + 13.5396 * gps_time
    cap = 2.29 * 3600
    print("Energy", energy)
    print(cap / energy)


if __name__ == '__main__':
    lora_power = cal_lock_unlock('../data/power/Normal.csv')
    print(f'Lock/Unlock Power Consumption: {lora_power} J')

    gps_power = cal_gps('../data/power/Gps.csv')
    print(f'GPS Power Consumption: {gps_power} J in 20 seconds')

    print("---------------------------------")
    low_demand()
    high_demand()
