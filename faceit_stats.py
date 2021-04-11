import requests
import json
from aiohttp import ClientSession
import asyncio

with open('key.api', 'r') as f:
    API_KEY = f.readline().strip()
DATA_API_URL = 'https://open.faceit.com/data/v4'
headers = {'Authorization': f'Bearer {API_KEY}'}


def request(url, **kwargs):
    return json.loads(requests.get(DATA_API_URL + url.format(**kwargs), headers=headers).content)


def get_history(nickname, limit, game_id='csgo'):
        player_id = request('/players?nickname={nickname}', nickname=nickname)['player_id']
        history = request('/players/{player_id}/history?game={game_id}&offset=0&limit={limit}',
                      player_id=player_id, limit=limit, game_id=game_id)['items']
        return history, player_id


async def get_stats(match_id, player_id):
    async with ClientSession() as session:
        resp = await session.get(
            DATA_API_URL + f'/matches/{match_id}/stats',
            headers=headers)
        data = await resp.json()
    for team in data['rounds'][0]['teams']:
        for player in team['players']:
            if player_id == player['player_id']:
                kills = int(player['player_stats']['Kills'])
                deaths = int(player['player_stats']['Deaths'])
    return kills, deaths


def get_coros(nickname, limit):
    history, player_id = get_history(nickname, limit)
    to_do = [get_stats(match['match_id'], player_id) for match in history]
    return to_do


async def player_stat(nickname, limit):
    to_do = get_coros(nickname, limit)
    res = await asyncio.gather(*to_do)
    return res
