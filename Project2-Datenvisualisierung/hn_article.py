import requests
import json

# Fuehrt einen API-Aufruf durch und speichert die Antwort.
url = "https://hacker-news.firebaseio.com/v0/item/31353677.json/"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Untersucht die Struktur der Daten.
response_dict = r.json()
response_string = json.dumps(response_dict, indent=4)
print(response_string)