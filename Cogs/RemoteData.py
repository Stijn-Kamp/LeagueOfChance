import json
from bs4 import BeautifulSoup
import requests


# Item ids, need to find a work around
# http://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/champion.json
# https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html?highlight=items#data-dragon

ITEM_URL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json"
CHAMPION_URL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json"

PATCH = '11.24.1'
soup = requests.get(ITEM_URL.format(PATCH))
items = json.loads(soup.text).get('data')

soup = requests.get(CHAMPION_URL.format(PATCH))
champions = json.loads(soup.text).get('data')

def format_name(champion):
    return champion.split('&', 1)[0].replace('.', '').replace(' ', '').replace("'", '')

def get_champion_description(champion):
    description = champions.get(format_name(champion))
    if description:
        description = description.get('title')
    else:
        description = ''
    return description

def get_champion_image(champion):
    champion = format_name(champion)
    return "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(PATCH, champion)

def to_item(id):
    item = items.get(str(id))
    if item:
        item = item.get('name')
    return item

if __name__ == '__main__':
    print(champions.keys())

