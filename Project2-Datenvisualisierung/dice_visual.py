import plotly.express as px
from die import Die

# Erstellt zwei W6-Wuerfel.
die_1 = Die()
die_2 = Die(10)

# Wuerfelt mehrere Male und speichert die Ergebnisse in einer Liste.
results = []
for roll_num in range(50_000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

# Analysiert die Ergebnisse.
frequencies = []
max_results = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_results+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)
#frequency = [results.count(value) for value in poss_results]
#frequencies.append(frequency)

# Stellt die Ergebnisse grafisch dar.
# Die Ergebnisse visualisieren.
title = "Results of Rolling a D6 and a D10 50,000 Times"
labels = {'x':'Results', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)
# Further customize chart.
fig.update_layout(xaxis_dtick=1)
fig.show()
#fig.write_html('dice_visual_d6d10.html')
#fig = px.scatter(x=poss_results, y=frequencies)
#fig = px.line(x=poss_results, y=frequencies)
#fig = px.area(x=poss_results, y=frequencies)
#fig = px.funnel(x=poss_results, y=frequencies)
