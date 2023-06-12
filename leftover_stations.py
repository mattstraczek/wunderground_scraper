# This file was used to find the leftover "general" stations that weather_scraper_PWS(2).py that had a different interface from "PWS" stations. 
# The leftover stations were exported to leftover_stations.txt
import pandas

df1 = pandas.read_csv("weather0-50.csv")
new_columns = df1.columns.tolist()

df2 = pandas.read_csv("weather50-100.csv")
df2 = df2.reindex(columns=new_columns)

df3 = pandas.read_csv("weather100-150.csv")
df3 = df3.reindex(columns=new_columns)

df4 = pandas.read_csv("weather150-200.csv")
df4 = df4.reindex(columns=new_columns)

df5 = pandas.read_csv("weather200-250.csv")
df5 = df5.reindex(columns=new_columns)

df6 = pandas.read_csv("weather250-300.csv")
df6 = df6.reindex(columns=new_columns)

df7 = pandas.read_csv("weather300-350.csv")
df7 = df7.reindex(columns=new_columns)

df8 = pandas.read_csv("weather350-390.csv")
df8 = df8.reindex(columns=new_columns)

df = pandas.concat([df1, df2, df3, df4, df5, df6, df7, df8])

station_list = []
with open("all_stations.txt") as f:
    stations = f.readlines()
    for i in range(len(stations)):
        station_list.append(stations[i][:len(stations[i]) - 1])

df = df.reset_index()
# print(df)
# print(station_list)

scraped_stations_list = []
for index, row in df.iterrows():
    scraped_stations_list.append(row["Unnamed: 0"])

# print(scraped_stations_list)

leftover_stations_list = []
for station in station_list:
    if station not in scraped_stations_list:
        leftover_stations_list.append(station)
    
# print(leftover_stations_list)
# print(len(leftover_stations_list))

# for station in leftover_stations_list:
#     f = open("leftover_stations.txt", "a")
#     f.write(station + "\n")
#     f.close()

# i = 0
# for index, row in df.iterrows():
#     print(row["Unnamed: 0"])
#     has_data = True
#     for col in new_columns:
#         if not pandas.isnull(row[col]):
#             # print("empty")
#             has_data = False
#     if has_data:
#         print("empty")
