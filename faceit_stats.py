import requests
import json
import collections
from concurrent.futures import ThreadPoolExecutor


with open('key.api', 'r') as f:
    API_KEY = f.readline().strip()
DATA_API_URL = 'https://open.faceit.com/data/v4'
headers = {'Authorization': f'Bearer {API_KEY}'}


def request(url, **kwargs):
    return json.loads(requests.get(DATA_API_URL + url.format(**kwargs), headers=headers).content)


def get_stats(nickname, limit, game_id='csgo'):
    player_id = request('/players?nickname={nickname}', nickname=nickname)['player_id']
    history = request('/players/{player_id}/history?game={game_id}&offset=0&limit={limit}',
                      player_id=player_id, limit=limit, game_id=game_id)['items']
    with ThreadPoolExecutor(4) as executor:
        stats = list(executor.map(calc_stats, list(history), [player_id]*len(history)))
    kills = [val[0] for val in stats]
    deaths = [val[1] for val in stats]
    return {'Kills': kills, 'Deaths': deaths}


def calc_stats(history, player_id):
    match_id = history['match_id']
    data = request('/matches/{match_id}/stats', match_id=match_id)
    for team in data['rounds'][0]['teams']:
        for player in team['players']:
            if player_id == player['player_id']:
                kills = int(player['player_stats']['Kills'])
                deaths = int(player['player_stats']['Deaths'])
    return kills, deaths
