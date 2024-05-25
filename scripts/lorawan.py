"""
Generate a graph of the largest RSSI and SNR
Also Generate a report to tell how many are lost. Each location should have 10.
"""
import glob
import json
import matplotlib.pyplot as plt


def read_json(file_path: str):
    with open(file_path, "r") as fp:
        data = json.load(fp)
    return data


def get_metadata(data: dict):
    metadata = data["uplink_message"]["rx_metadata"]
    return metadata


def get_data_list(metadata: dict, data_type: str):
    data_list = []
    for item in metadata:
        try:
            data_list.append(item[data_type])
        except KeyError:
            pass
    return data_list


def get_max_data(data: dict, data_type):
    rssi_list = get_data_list(data, data_type)
    # max based on the absolute value
    max_rssi = max(rssi_list, key=abs)
    return abs(max_rssi)


def get_average_data(max_rssis: list):
    return sum(max_rssis) / len(max_rssis)


def get_lost_packets(name: str):
    files = glob.glob(f"../data/lorawan/{name}_*.json")
    return 10 - len(files)


def get_locations():
    files = glob.glob("../data/lorawan/*.json")
    locations = []
    for file in files:
        location = file.split("/")[-1].split("_")[0]
        if location is not None and location not in locations:
            locations.append(location)
    return locations


# def get_locations_abbreviations():
#     locations = get_locations()
#     locations_abbreviations = []
#     for location in locations:
#         locations_abbreviations.append(location[:1].upper())
#         for i in range(1, len(location)):
#             c = location[i]
#             if c.isupper():
#                 locations_abbreviations[-1] += c
#         locations_abbreviations[-1] += location[-1]
#     return locations_abbreviations

def get_locations_abbreviations():
    locations = get_locations()
    locations_abbreviations = []
    i = 0
    for location in locations:
        locations_abbreviations.append(f"Loc{i}")
        i+=1
    return locations_abbreviations


"""
data format:
{
    "title": "title",
    "rssis": [1, 2, 3, 4, 5],
    "snrs": [1, 2, 3, 4, 5],
    "lost_packets": [1, 2, 3, 4, 5],
    "locations": ["location1", "location2", "location3", "location4", "location5"]
    "locationAbbreviation": ["loc1", "loc2", "loc3", "loc4", "loc5"]
}
"""


def plot_graph(data):
    font_size = 100
    # Create a figure and a set of subplots
    fig, axs = plt.subplots(3, 1, figsize=(40, 60))

    # Plot RSSI
    axs[0].bar(data['locationAbbreviation'], data['rssis'], color='b')
    axs[0].set_title('RSSI', fontsize=font_size + 20)
    axs[0].set_xlabel('Locations', fontsize=font_size)
    axs[0].set_ylabel('RSSI', fontsize=font_size)
    axs[0].tick_params(axis='x', labelsize=font_size - 20)
    axs[0].tick_params(axis='y', labelsize=font_size - 20)

    # Plot SNR
    axs[1].bar(data['locationAbbreviation'], data['snrs'], color='r')
    axs[1].set_title('SNR', fontsize=font_size + 20)
    axs[1].set_xlabel('Locations', fontsize=font_size)
    axs[1].set_ylabel('SNR', fontsize=font_size)
    axs[1].tick_params(axis='x', labelsize=font_size - 20)
    axs[1].tick_params(axis='y', labelsize=font_size - 20)

    # Plot Lost Packets
    axs[2].bar(data['locationAbbreviation'], data['lost_packets'], color='g')
    axs[2].set_title('Lost Packets', fontsize=font_size + 20)
    axs[2].set_xlabel('Locations', fontsize=font_size)
    axs[2].set_ylabel('Lost Packets', fontsize=font_size)
    axs[2].tick_params(axis='x', labelsize=font_size - 20)
    axs[2].tick_params(axis='y', labelsize=font_size - 20)
    # Display the figure
    plt.tight_layout()
    plt.show()


def main():
    locations = get_locations()
    locations_abbreviations = get_locations_abbreviations()
    data_for_graph = {"title": "LoRaWAN Data",
                      "rssis": [],
                      "snrs": [],
                      "lost_packets": [],
                      "locations": locations,
                      "locationAbbreviation": locations_abbreviations}
    for location in locations:
        max_rssis = []
        max_snrs = []
        files = glob.glob(f"../data/lorawan/{location}_*.json")
        for file_path in files:
            data = read_json(file_path)
            metadata = get_metadata(data)
            max_rssi = get_max_data(metadata, "rssi")
            max_rssis.append(max_rssi)
            max_snr = get_max_data(metadata, "snr")
            max_snrs.append(max_snr)
        data_for_graph["lost_packets"].append(get_lost_packets(location))
        average_rssi = get_average_data(max_rssis)
        average_snr = get_average_data(max_snrs)
        lost_packets = get_lost_packets(location)
        data_for_graph["rssis"].append(average_rssi)
        data_for_graph["snrs"].append(average_snr)
        print(f"Location: {location}")
        print(f"Average RSSI: {average_rssi}")
        print(f"Average SNR: {average_snr}")
        print(f"Lost Packets: {lost_packets}")
        print("\n")
    print(data_for_graph)
    plot_graph(data_for_graph)


if __name__ == "__main__":
    print(get_locations())
    print(get_locations_abbreviations())
    print("LoRaWAN Script")
    main()
    print("End of LoRaWAN Script")