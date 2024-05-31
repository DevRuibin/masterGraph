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


def main():
    capacity = 2.29
    power_consumption = calculate_power_consumption() / 24
    days = capacity / power_consumption
    print(f"Power Consumption: {power_consumption:.2f} Wh")
    print(f"Days: {days:.2f}")


if __name__ == '__main__':
    main()
