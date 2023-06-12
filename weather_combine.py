# This file was used to combine PWS stations (weather_output_2.xslx) and general stations (weather_output_1.xslx)
import pandas
import openpyxl


# df1 = pandas.read_csv("weather0-50.csv")
# new_columns = df1.columns.tolist()

# df2 = pandas.read_csv("weather50-100.csv")
# df2 = df2.reindex(columns=new_columns)

# df3 = pandas.read_csv("weather100-150.csv")
# df3 = df3.reindex(columns=new_columns)

# df4 = pandas.read_csv("weather150-200.csv")
# df4 = df4.reindex(columns=new_columns)

# df5 = pandas.read_csv("weather200-250.csv")
# df5 = df5.reindex(columns=new_columns)

# df6 = pandas.read_csv("weather250-300.csv")
# df6 = df6.reindex(columns=new_columns)

# df7 = pandas.read_csv("weather300-350.csv")
# df7 = df7.reindex(columns=new_columns)

# df8 = pandas.read_csv("weather350-390.csv")
# df8 = df8.reindex(columns=new_columns)

# df = pandas.concat([df1, df2, df3, df4, df5, df6, df7, df8])
# df.to_excel("weather_output_2.xlsx")

# print(df)
# # print(df.loc['KMOCOLUM65'])
# print(df.shape)

df1 = pandas.read_csv("weather0-40.csv")
new_columns = df1.columns.tolist()

df2 = pandas.read_csv("weather40-80.csv")
df2 = df2.reindex(columns=new_columns)

df3 = pandas.read_csv("weather80-120.csv")
df3 = df3.reindex(columns=new_columns)

df4 = pandas.read_csv("weather120-158.csv")
df4 = df4.reindex(columns=new_columns)

df = pandas.concat([df1, df2, df3, df4])
df.to_excel("weather_output_1.xlsx")

print(df)
# print(df.loc['KMOCOLUM65'])
print(df.shape)