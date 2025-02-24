import csv
import random

# Retrieve colours from csv file and put them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colors = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_colors.pop(0)
print(all_colors)