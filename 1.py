import requests
from pprint import pprint

user_name = 'OlgaP-1'
url = f'https://api.github.com/users/{user_name}/repos'
r = requests.get(url)

for i in r.json():
    pprint(i['name'])
if r.ok:
    import json
    path = 'name_repo_users.json'
    path_2 = 'name_repo'
    it = [(i['name']) for i in r.json()]
    with open(path, 'w') as f:
        json.dump(r.json(), f)
    with open(path_2, 'w') as f:
        json.dump(it, f)

