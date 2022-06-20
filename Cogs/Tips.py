from cgitb import lookup
import discord #import all the necessary modules
from discord.ext import commands
import random

from Cogs.RemoteData import get_champion_description, get_champion_image, to_item, format_name
from Cogs.Constants import ROLES


# for champion_counter
from bs4 import BeautifulSoup
import requests


class Tips(commands.Cog):
  """A collection of tips and tricks"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command()
  async def counter(self, ctx, *command):
    "Gives a random tip to counter a champion"
    command = list(command)
    
    
    # Show all tips, even badly rated tips
    show_all = True
    if '-a' in command:
        command.remove('-a')
    elif '--show_all' in command:
        command.remove('--show_all')
    else:
        show_all = False


    champion = '-'.join(command)
    if champion:
        tips = champion_counter(champion, show_all)
        if tips:
            reply = random.choice(tips)
        else:
            reply = "Sorry, I could not find a tip to play against {}.".format(champion)
    else:
      reply = "Please give the name of the champion you would like to counter."

    await ctx.send(reply)

  @commands.command(name="build", aliases=['b'])
  async def build(self, ctx, *champion):
    # https://python.plainenglish.io/python-discord-bots-formatting-text-efca0c5dc64a
    # formatting example
    "Retrieves the most played build from the internet"
    role = champion[-1].capitalize()
    if role in ROLES or role == 'Aram':
        champion = champion[:-1]
    else:
        role = None
    lookup_name = ''.join(champion)
    build = champion_build(lookup_name, role)

    if build:
        champion = build.get('Champion')
        lookup_name = format_name(champion)

        icon = get_champion_image(lookup_name)
        description = get_champion_description(lookup_name)
        url = build.get('Url')

        runes = build.get('Runes')
        primary = ', '.join(runes[0]) if runes else None
        secondary = ', '.join(runes[1]) if runes else None
        shards = ', '.join(build.get('Shards'))
        sums = ', '.join(build.get('Summoner spells'))
        abilities = ', '.join(build.get('Abilities'))
        starter_items = ', '.join(build.get('Starter items'))
        items = ', '.join(build.get('Items'))
        boots = build.get('Boots')

        embed=discord.Embed(
            color=discord.Color.blue(),
            description = description
        )
        embed.set_author(
        name="{}".format(champion), 
        icon_url=icon,
        url=url,
        )

        embed.add_field(name="**Role**", value=build.get('Role'), inline=False)
        embed.add_field(name="**Primary runes**", value=primary, inline=False)
        embed.add_field(name="**Secondary runes**", value=secondary, inline=False)
        embed.add_field(name="**Shards**", value=shards, inline=False)
        embed.add_field(name="**Summoner spells**", value=sums, inline=False)
        embed.add_field(name="**Ability order**", value=abilities, inline=False)
        embed.add_field(name="**Boots**", value=boots, inline=False)
        embed.add_field(name="**Starter items**", value=starter_items, inline=False)
        embed.add_field(name="**Items**", value=items, inline=False)

        await ctx.send(embed=embed)        
    else:
        errorMessage = "Sorry, I couldn't find a build for {}.".format(' '.join(champion))
        await ctx.send(errorMessage)

class Trends(commands.Cog):
    """A collection of tips and tricks"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def get_trends(champion, params=None):
        if params is None:
            params = "SUMMONERS_RIFT_DRAFT_PICK&region=WORLD"
        URL = f"https://champion.gg/champion/{champion}?{params}"

        try:
            page = requests.get(URL).text
            soup = BeautifulSoup(page, 'html.parser')
            champion = soup.find('h1').text[:-4]
            role = soup.find('option', selected=True).text
            trends = soup.find_all(class_="type-body2")
            trends = [trend.find_all('span')[1].text.replace(',', '') for trend in trends]
            trends = {
                'champion': champion,
                'role': role,
                'kills': trends[0],
                'deaths': trends[1],
                'assists': trends[2],
                'damage': trends[3],
                'damage mitigated': trends[4],
                'gold earned': trends[5]
            }
        except AttributeError as e:
            trends = {}
        except Exception as e:
            print(e)
            trends = {}
        finally:
            return trends
        


# Functions
def to_summoners_spell(string):
    if 'SummonerFlash' in string:
        return 'Flash'    
    elif 'SummonerTeleport' in string:
        return 'Teleport'    
    elif 'SummonerSmite' in string:
        return 'Smite'    
    elif 'SummonerDot' in string:
        return 'Ignite'    
    elif 'SummonerHeal' in string:
        return 'Heal'    
    elif 'SummonerExhaust' in string:
        return 'Exhaust'
    elif 'SummonerHaste' in string:
        return 'Ghost'
    elif 'SummonerBarrier' in string:
        return 'Barrier'   
    elif 'SummonerCleanse' in string:
        return 'Cleanse'
    elif 'SummonerSnowball' in string:
        return 'Mark'
    elif 'SummonerMana' in string:
        return 'Clarity' 
    else:
        return None

# Functions
def to_shard(string):    
    if '5001' in string:
        return 'Health'    
    elif '5002' in string:
        return 'Armor'    
    elif '5003' in string:
        return 'Magic resist'  
    if '5005' in string:
        return 'Attack speed'    
    elif '5007' in string:
        return 'Ability haste'   
    elif '5008' in string:
        return 'Adaptive force'   
    else:
        return None

def url_to_item(url):
    try:
        item = str(url).split('item/')[1].split('.')[0]
        item = to_item(item)
    except:
        item = None
    return item

def champion_counter(champion, show_all=False):
  BASE_URL = "https://lolcounter.com/tips/{}/general" if show_all else "https://lolcounter.com/champions/{}"
  URL = BASE_URL.format(champion.replace("'",""))
  try:
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'html.parser')
    tips = soup.find_all("span", class_="_tip")
    tips = [tip.text for tip in tips]
  except Exception as e:
    print(e)
    tips = []
  return tips

def champion_build(name, role=None, ):
    if str(role).lower() == 'aram':
        BASE_URL = "https://euw.op.gg/aram/{}/statistics/450/build"
        url = BASE_URL.format(name)
    else:
        BASE_URL = "https://www.op.gg/champion/{}"
        url = BASE_URL.format(name)
        if role is not None:
            url += '/statistics/{}/build'.format(role)

        print(url)
    try:
        print('test')
        headers = {'user-agent': 'LeagueOfChange/1.0.0'}
        page = requests.get(url, headers=headers).text        
        soup = BeautifulSoup(page, 'html.parser')
        build = soup.find_all('ul')
        print(len(build))
        print(build)
        if build is None or len(build) < 12:
            return None
        
        champion_name = soup.find(class_="name")
        champion_name = ' '.join(champion_name.text.split(' ')) if champion_name else None

        summoner_spells = build[2]
        summoner_spells = summoner_spells.find_all('img') if summoner_spells else []
        summoner_spells = [img.get('alt') for img in summoner_spells] if summoner_spells else None

        abilities = build[4].find_all('span')
        abilities = [ability.text for ability in abilities] if abilities else None

        starter_items = build[5].find_all('img')
        starter_items = [item.get('alt') for item in starter_items] if starter_items else None

        items = build[7].find_all('img')
        items = [item.get('alt') for item in items] if items else []
        items = [item for item in items if item != 'Right Arrow'] # Remove None 
        
        boots = build[12].find('img')
        boots = url_to_item(boots.get('src')) if boots else None

        if role == None:
            role = soup.find('link').get('href').split('/')[-2]
        role = role.capitalize() if role else None

        rune_page = soup.find(class_='rune_box')
        rune_page = rune_page.find_all('div', recursive=False) if rune_page else []
        rune_page = [item for item in rune_page if 'divider' not in str(item)] # remove the dividers

        runes = [[]]*2

        if rune_page:
            #Loop through each runepage
            for i in range(len(runes)):
                # divide all the rows
                rows = rune_page[i].find_all(class_='row')[1:]
                for j in range(len(rows)):      # loop through rows
                    row = rows[j].find_all('img')  
                    for img in row:
                        if 'grayscale' not in str(img): # Check the opacity of the image to see if shard is active or not
                            rune = img.get('alt')
                            runes[i].append(rune)
                            break
        
        runes = [runes[0][:4], runes[1][4:]] # QUICK FIX, NEED TO BE REMOVED LATER

        if len(rune_page) >= 3:
            shard_page = rune_page[2]
            rows = shard_page.find_all(class_='row') if shard_page else []
            shards = []
            for i in range(len(rows)):
                row = rows[i].find_all('div')
                for item in row:
                    img = item.find('img')
                    if '0.5' not in str(img): # Check the opacity of the image to see if shard is active or not
                        shard = to_shard(img.get('src'))
                        shards.append(shard)
                        break
        build = {
            "Url": url,
            "Champion": champion_name,
            "Role": role,
            "Summoner spells": summoner_spells,
            "Abilities": abilities,
            "Shards": shards,
            "Starter items": starter_items,
            "Items": items,
            "Boots": boots,
            "Runes": runes
        }
    except SyntaxError as e:
        print(e)
        build = None

    
    return build

if __name__ == '__main__':
    build = champion_build(2)
    print(build)