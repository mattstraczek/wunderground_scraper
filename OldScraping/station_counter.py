original_file = open("zip_codes$latlong$id.txt", "r")
new_file = open("zip_codes$latlong$idNEW.txt", "r")
station_count_map = {}

for line in original_file:
    if line[5] != ":":
        zip, latlong, id = line.split("$")
        id = id[:len(id) - 1]
        if id != "NA":
            if station_count_map.get(id, 0) == 0:
                station_count_map[id] = 1
            else:
                station_count_map[id] += 1
        


for line in new_file:
    if line[5] != ":":
        zip, latlong, id = line.split("$")
        id = id[:len(id) - 1]
        if id != "NA":
            if station_count_map.get(id, 0) == 0:
                station_count_map[id] = 1
            else:
                station_count_map[id] += 1

print(station_count_map)           
print(len(station_count_map))
sum = 0
for value in station_count_map:
    sum += station_count_map[value]

print(sum)

original_file.close()
new_file.close()