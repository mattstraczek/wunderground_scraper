import pandas
#This file is for fixing formatting inconsistencies between PWS (Personal Weather Station) scraping and existing stations

month_dict = {"January":"1", "February":"2", "March":"3", "April":"4", "May":"5", "June":"6", "July":"7", "August":"8", "September":"9", "October":"10", "November":"11", "December":"12"}

def rename_columns(old_file, new_file):
    df1 = pandas.read_excel(old_file)
    new_columns = df1.columns.tolist()
    # print(new_columns)

    columns_dict = {}
    for i in range(2,len(new_columns)):
        column = new_columns[i]
        # print(column)
        month, day, year = column.split("-")
        new_column = month_dict[month]
        new_column += "/"
        new_column += day + "/" + year
        columns_dict[column] = new_column

    df1.rename(columns=columns_dict, inplace=True)
    df1.to_excel(new_file)

# rename_columns("weather_output_1", "weather_output_1_renamed.xlsx")

def reformat_data_2(old_file, new_file):
    df = pandas.read_excel(old_file)
    columns = df.columns.to_list()
    columns = columns[3:len(columns)]
    print(columns)

    for index, row in df.iterrows():
        print(row["Unnamed: 0"])

        for col in columns:
            # print(row[col])
            if isinstance(row[col], str):
                data = row[col].split("/")
                if len(data) > 0:
                    for i in range(len(data)):
                        d = data[i]
                        # print(data[i])
                        if len(data[i]) > 0:
                            if data[i][0] == "-":
                                data[i] = data[i].replace("-", ";", 8)
                                data[i] = data[i].replace(";;", ";-", 8)
                                data[i] = "-" + data[i][1:len(data[i])]
                            else:
                                data[i] = data[i].replace("-", ";", 8)
                                data[i] = data[i].replace(";;", ";-", 8)
                            data[i] = data[i].replace("--;-;-;-", "", 8)
                            
                            
                            data[i] = data[i].replace(" °F", "", 8)
                            data[i] = data[i].replace(" %", "", 8)
                            data[i] = data[i].replace(" mph", "", 8)
                            data[i] = data[i].replace(" in", "", 8)
                            
                    new_data = ""
                    for i in range(len(data)):
                        new_data += data[i] + "/"
                    new_data = new_data[0:len(new_data) - 1]
                    # print(new_data)
                    df.at[index, col] = new_data
                    # print(df.at[index, col])

    df.to_excel(new_file, index=False)
    
# reformat_data_2("weather_output_2.xlsx", "weather_output_2_reformatted.xlsx")

def reformat_data(old_file, new_file):
    df = pandas.read_excel(old_file)
    columns = df.columns.to_list()
    columns = columns[3:len(columns)]
    print(columns)

    for index, row in df.iterrows():
        print(row["Unnamed: 0"])

        for col in columns:
            # print(row[col])
            if isinstance(row[col], str):
                data = row[col].split("/")
                if len(data) > 0:
                    for i in range(len(data)):
                        d = data[i]
                        if data[i][0] == "-":
                            data[i] = data[i].replace("-", ";", 8)
                            data[i] = data[i].replace(";;", ";-", 8)
                            data[i] = "-" + data[i][1:len(data[i])]
                        else:
                            data[i] = data[i].replace("-", ";", 8)
                            data[i] = data[i].replace(";;", ";-", 8)
                        data[i] = data[i].replace("--;-;-;-", "", 8)
                        
                    new_data = ""
                    for i in range(len(data)):
                        new_data += data[i] + "/"
                    new_data = new_data[0:len(new_data) - 1]
                    # print(new_data)
                    df.at[index, col] = new_data
                    # print(df.at[index, col])

    df.to_excel(new_file)

# reformat_data2("weather_output_1_renamed.xlsx", "weather_output_1_reformatted.xlsx")

df = pandas.read_excel("reformatted_weather_output_2.xlsx")
columns = df.columns.to_list()
columns = columns[3:len(columns)]
print(columns)

for index, row in df.iterrows():

    for col in columns:
        # print(row[col])
        if isinstance(row[col], str):
            data = row[col].split("/")
            if len(data) > 0:
                for i in range(len(data)):
                    d = data[i]
                    # print(data[i])
                    if len(data[i]) > 0:
                        data[i] = data[i].replace("--;-;-", ";;", 8)
                        
                new_data = ""
                for i in range(len(data)):
                    new_data += data[i] + "/"
                new_data = new_data[0:len(new_data) - 1]
                # print(new_data)
                df.at[index, col] = new_data
                # print(df.at[index, col])

# df.to_excel("reformatted_weather_output_2_new.xlsx", index=False)
