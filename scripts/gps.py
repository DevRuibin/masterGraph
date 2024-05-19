"""
read the measured coordinates and actual coordinates from the GPS csv file
The file format is as follows:
location,measuredLatitude,measuredLongitude,actualLatitude,actualLongitude
then plot the difference between the measured and actual coordinates on a scatter plot
Then create another functions to calculate the distance between the measured and actual coordinates
"""

import csv
import matplotlib.pyplot as plt
import math


def read_gps_data(file_path: str):
    with open(file_path, "r") as fp:
        csv_reader = csv.reader(fp)
        next(csv_reader)
        data = [row for row in csv_reader]
    return data


def plot_gps_data(data: list):
    measured_latitude = [float(row[1]) for row in data]
    measured_longitude = [float(row[2]) for row in data]
    actual_latitude = [float(row[3]) for row in data]
    actual_longitude = [float(row[4]) for row in data]
    locations = [f"Loc{i}" for i in range(len(data))]

    plt.scatter(measured_latitude, measured_longitude, color="red", label="Measured")
    plt.scatter(actual_latitude, actual_longitude, color="blue", label="Actual")

    for i, location in enumerate(locations):
        plt.annotate(location, (measured_latitude[i], measured_longitude[i]))
        # plt.annotate(location, (actual_latitude[i], actual_longitude[i]))

    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.legend()
    plt.show()


def print_distance(data: list):
    for row in data:
        location = row[0]
        measured_latitude = float(row[1])
        measured_longitude = float(row[2])
        actual_latitude = float(row[3])
        actual_longitude = float(row[4])

        distance = calculate_distance(measured_latitude, measured_longitude, actual_latitude, actual_longitude)
        print(f"Location: {location}, Distance: {distance:.2f} km")


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Calculate the distance between two coordinates
    """
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def main():
    data = read_gps_data("../data/gps/measure.csv")
    # plot_gps_data(data)
    print_distance(data)


if __name__ == "__main__":
    main()
