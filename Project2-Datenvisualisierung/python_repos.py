import requests

# Fuehrt einen API-Aufruf durch und prueft die Antwort.
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
url += "?q=language:python+sort:stars+stats:>10000"
headers = {"Accept":"application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")


# Konvertiert das Antwort-Objekt in ein Dictionary.
response_dict = r.json()
print(f"Total repositories: {response_dict['total_count']}")
print(f"Complete results: {not response_dict['incomplete_results']}")

# Gibt Informationen ueber die Repositores aus.
repo_dicts = response_dict['items']
print(f"Repositories returned: {len(repo_dicts)}")

# Untersucht das erste Repository.
#repo_dict = repo_dicts[0]
#print(f"\nKeys: {len(repo_dict)}")
#for key in sorted(repo_dict.keys()):
    #print(key)
# Verarbeitet die Ergebnisse.
#print(response_dict.keys())

print("\nSelected information about each repository: ")
for repo_dict in repo_dicts:
    print(f"\nName: {repo_dict['name']}")
    print(f"Owner: {repo_dict['owner']['login']}")
    print(f"Stars: {repo_dict['stargazers_count']}")
    print(f"Repository: {repo_dict['html_url']}")
    
    print(f"Description: {repo_dict['description']}")

#print(f"Created: {repo_dict['created_at']}")
#print(f"Updated: {repo_dict['updated_at']}")