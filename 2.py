import requests
from pprint import pprint

'''Example 1 - получим токен'''
api_key = '844341b11efbd8d576ecc5c38d78f3c6'
url1 = f'https://api.themoviedb.org/3/authentication/token/new?api_key={api_key}'
r = requests.get(url1)

'''Example 2 - получим список фильмов с сортировкой  по популярности'''
api_key = '844341b11efbd8d576ecc5c38d78f3c6'
sort_by = 'popularity.desc'
url2 = f'https://api.themoviedb.org/3/discover/movie?'\
    f'api_key={api_key}&'\
    'language=ru-RU&'\
    f'sort_by={sort_by}&'\
    'include_adult=false&'\
    'include_video=true&'\
    'page=1'
r2 = requests.get(url2)


'''Example 3 - Получим список фильмов еще одним способом с сортировкой по дате релиза '''
params = {
    'api_key': '844341b11efbd8d576ecc5c38d78f3c6',
    'language': 'ru-RU',
    'sort_by': 'release_date.desc',
    'include_adult': 'false',
    'include_video': 'false',
    'page': 1
}
base_url = 'https://api.themoviedb.org/3/discover/movie'
api_key = '844341b11efbd8d576ecc5c38d78f3c6'
r3 = requests.get(base_url, params=params)


pprint(('токен: ', r.json()['request_token'], '\n', 'список фильмов с сортировкой  по популярности: ', r2.text, '\n',\
        'список фильмов еще одним способом с сортировкой по дате релиза: ', r3.text))

if r.ok and r2.ok and r3.ok:
    import json
    path = 'films_list.json'
    with open(path, 'w') as f:
        json.dump(r.json()['request_token'] and r2.json() and r3.json(), f)
