import requests
import json
import collections

with open('key.api', 'r') as f:
    API_KEY = f.readline().strip()
DATA_API_URL = 'https://open.faceit.com/data/v4'
headers = {'Authorization': f'Bearer {API_KEY}'}


def request(url, **kwargs):
    return json.loads(requests.get(DATA_API_URL + url.format(**kwargs), headers=headers).content)


def get_stats(nickname, limit, game_id='csgo'):
    player_id = request('/players?nickname={nickname}', nickname=nickname)['player_id']
    history = request('/players/{player_id}/history?game={game_id}&offset=0&limit={limit}',
                      player_id=player_id, limit=limit, game_id=game_id)
    matches = [item['match_id'] for item in history['items']]
    stats = collections.defaultdict(list)
    for match_id in matches:
        data = request('/matches/{match_id}/stats', match_id=match_id)
        for team in data['rounds'][0]['teams']:
            for player in team['players']:
                if player_id == player['player_id']:
                    stats['Kills'].append(int(player['player_stats']['Kills']))
                    stats['Deaths'].append(int(player['player_stats']['Deaths']))
    return stats
