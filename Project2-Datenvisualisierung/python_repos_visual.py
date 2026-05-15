import requests

import plotly.express as px

# Fuehrt einen API-Aufruf durch und prueft die Antwort.
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
url += "?q=language:python+sort:stars+stats:>10000"
headers = {"Accept":"application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Process overall results.
response_dict = r.json()
print(f"Complete results: {not response_dict['incomplete_results']}")

# Process repository information.
repo_dicts = response_dict['items']
repo_links, stars, hover_texts = [], [], []
for repo_dict in repo_dicts:
    # Repo-Namen in aktiven Links konvertieren
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)

    star = repo_dict['stargazers_count']
    stars.append(star)
    
    # Maustext erzeugen.
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)

# Make visualization.
title = "Most-Starred Python Projects on Github"
labels = {'x':'Repository', 'y':'Stars'}
fig = px.bar(x=repo_links, y=stars, title=title, labels=labels,
    hover_name=hover_texts)
fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
    yaxis_title_font_size=20)
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)
fig.show()