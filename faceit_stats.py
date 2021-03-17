import requests
import json
import collections

with open('key.api', 'r') as f:
    API_KEY = f.readline().strip()
DATA_API_URL = 'https://open.faceit.com/data/v4'
headers = {'Authorization': f'Bearer {API_KEY}'}

def get_player_id(nickname):
    resp = requests.get(DATA_API_URL + f'/players?nickname={nickname}', headers=headers)
    user_data = json.loads(resp.content)
    return user_data['player_id']


def get_history(player_id, limit=20, game_id='csgo'):
    resp = requests.get(DATA_API_URL + f'/players/{player_id}/history?game={game_id}&offset=0&limit={limit}',
                        headers=headers)
    data = json.loads(resp.content)
    return [item['match_id'] for item in data['items']]


def get_stats(nickname, limit):
    player_id = get_player_id(nickname)
    matches = get_history(player_id, limit)
    stats = collections.defaultdict(list)
    for match_id in matches:
        resp = requests.get(DATA_API_URL + f'/matches/{match_id}/stats', headers=headers)
        data = json.loads(resp.content)
        for team in data['rounds'][0]['teams']:
            for player in team['players']:
                if player_id == player['player_id']:
                    stats['Kills'].append(int(player['player_stats']['Kills']))
                    stats['Deaths'].append(int(player['player_stats']['Deaths']))
    return stats
