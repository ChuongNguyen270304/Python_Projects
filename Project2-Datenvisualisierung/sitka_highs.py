from pathlib import Path
import csv

import matplotlib.pyplot as plt

path = Path('weather_data/sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()
reader = csv.reader(lines)
header_row = next(reader)

#for index, column_header in enumerate(header_row):
    #print(index, column_header)

# Hoechsttemperaturen extrahieren.
highs = []
for row in reader:
    high = int(row[4])
    highs.append(high)

# Stellt die Hoechsttemperaturen grafisch dar.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(highs, color='red')

# Formatiert das Diagramm.
plt.title("Daily High temperature, July 2021", fontsize=24)
plt.xlabel('', fontsize = 16)
plt.ylabel("Temperature (F)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)

plt.show()