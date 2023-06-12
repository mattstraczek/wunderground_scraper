# This file takes the parallelized results from all_stations_scraper.py (these results were stored in 1-4.txt files), and combines all unique
# stations into one file all_stations.txt

file_1 = open("1.txt", "r")
file_2 = open("2.txt", "r")
file_3 = open("3.txt", "r")
file_4 = open("4.txt", "r")
station_count_map = {}

for line in file_1:
    id = line[:len(line) - 1]
    if station_count_map.get(id, 0) == 0:
        station_count_map[id] = 1
    else:
        station_count_map[id] += 1

for line in file_2:
    id = line[:len(line) - 1]
    if station_count_map.get(id, 0) == 0:
        station_count_map[id] = 1
    else:
        station_count_map[id] += 1

for line in file_3:
    id = line[:len(line) - 1]
    if station_count_map.get(id, 0) == 0:
        station_count_map[id] = 1
    else:
        station_count_map[id] += 1

for line in file_4:
    id = line[:len(line) - 1]
    if station_count_map.get(id, 0) == 0:
        station_count_map[id] = 1
    else:
        station_count_map[id] += 1
        
# print(station_count_map)           
print(len(station_count_map))
sum = 0
for value in station_count_map:
    sum += station_count_map[value]
print(sum)

output_file = open("all_stations.txt", "w")
for station in station_count_map:
    output_file.write(station + "\n")
output_file.close()

file_4.close()
file_3.close()
file_2.close()
file_1.close()