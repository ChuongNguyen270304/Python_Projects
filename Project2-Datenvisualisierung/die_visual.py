import plotly.express as px
from die import Die

# Erstellt einen W6.
die = Die()

# Wuerfelt mehrere Male und speichert die Ergebnisse in einer Liste.
results = []
for roll_num in range(1000):
    result = die.roll()
    results.append(result)

# Analysiert die Ergebnisse.
frequencies = []
poss_results = range(1, die.num_sides+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# Stellt die Ergebnisse grafisch dar.
# Die Ergebnisse visualisieren.
title = "Results of Rolling One D6 1,000 Times"
labels = {'x':'Results', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)
fig.show()
#fig = px.scatter(x=poss_results, y=frequencies)
#fig = px.line(x=poss_results, y=frequencies)
#fig = px.area(x=poss_results, y=frequencies)
#fig = px.funnel(x=poss_results, y=frequencies)
