"""We assume the GPS module's usage frequency is once every minutes and with a short burst time which is 20 seconds.
We also assume the lock and unlock are operated 3 times each day with a short burst time of 6 seconds. The operation
of locking and unlocking need NFC, Servo and Lora module. All the other times, the lock stays in normal situation.

"""

power_consumption = {
    "Normal": 0.6825457698899189,
    "Servo": 0.6866665719827936,
    "Nfc": 0.24885038011942015,
    "Lora": 0.21193549955187696,
    "Gps": 0.677694435685375
}


def calculate_gps():
    minutes_interval = 5
    burst_time = 20
    power = power_consumption["Gps"]
    seconds = (60 / minutes_interval) * burst_time * 24
    return power * seconds


def calculate_lock():
    times_per_day = 6
    burst_time = 6
    power = power_consumption["Servo"] + power_consumption["Nfc"] + power_consumption["Lora"]
    seconds = times_per_day * burst_time
    return power * seconds


def calculate_normal():
    return power_consumption["Normal"] * 24 * 60 * 60


def calculate_power_consumption():
    gps = calculate_gps()
    lock = calculate_lock()
    normal = calculate_normal()
    return gps + lock + normal

def get_milliampere():
    """
    the return value of calculate_power_consumption is in watts(P = UI)
    our battery is 5 volts, so we need to divide the power by 5 to get the current in amperes
    then we still need to divide it by 1000 to get the current in milli amperes
    :return: milliampere * 24 hours
    """
    return calculate_power_consumption() / 5 * 1000

def main():
    capacity = 620
    power_consumption = get_milliampere()
    days = capacity / power_consumption
    print(f"Power Consumption: {power_consumption:.2f} Wh / day")
    print(f"Days: {days:.2f}")


if __name__ == '__main__':
    main()
