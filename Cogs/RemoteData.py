import json
import requests


# Item ids, need to find a work around
# http://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/champion.json
# https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html?highlight=items#data-dragon

# Versions
VERSION_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
soup = requests.get(VERSION_URL)
versions = list(json.loads(soup.text))
PATCH = versions[0] if versions else '11.24.1' # Backup version

BASE_URL = "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/{}.json"
LANGUAGE = 'en_US'

def get_ddragon_info(name, patch=PATCH, language=LANGUAGE):
    try:
        url = BASE_URL.format(patch, language, name)
        soup = requests.get(url)
        info = json.loads(soup.text)
    except SyntaxError:
        info = None
    return info


# Items
items = get_ddragon_info('item').get('data')

def to_item(id):
    item = items.get(str(id))
    if item:
        item = item.get('name')
    return item

# Summoner spells
summoner = get_ddragon_info('summoner').get('data')

# Runes
runes = get_ddragon_info('runesReforged')

# Champions
champions = get_ddragon_info('champion').get('data') # championFull

def format_name(name):
    for champion in list(champions.keys()):
        if name == champions.get(champion).get('name'):
            return champion
    return name

def get_champion_description(champion):
    description = champions.get(champion)
    if description:
        description = description.get('title')
    else:
        description = ''
    return description

def get_champion_image(champion):
    return "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(PATCH, champion)

if __name__ == '__main__':
    print(champions.keys())

