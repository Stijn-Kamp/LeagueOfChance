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

        primary = ', '.join(build.get('Runes')[0])
        secondary = ', '.join(build.get('Runes')[1])
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
        headers = {'user-agent': 'LeagueOfChange/1.0.0'}
        page = requests.get(url, headers=headers).text        
        soup = BeautifulSoup(page, 'html.parser')
        build = soup.find_all(class_='champion-stats__list')

        champion_name = soup.find(class_="champion-stats-header-info__name").text.split(' ')[0]

        summoner_spells = build[0].find_all('img')
        summoner_spells = [to_summoners_spell(img.get('src')) for img in summoner_spells]

        abilities = build[2].find_all('span')
        abilities = [ability.text for ability in abilities]

        starter_items = build[3].find_all('img')
        starter_items = [url_to_item(item.get('src')) for item in starter_items]

        items = build[5].find_all('img')
        items = [url_to_item(item.get('src')) for item in items]
        items = [item for item in items if item] # Remove None 

        
        boots = build[10].find('img')
        boots = url_to_item(boots.get('src'))

        if role == None:
            role = soup.find('link').get('href').split('/')[-2]
        role = role.capitalize()

        pages = 2
        runes = soup.find_all(class_='perk-page')[:pages]

        for i in range(pages):
            runes[i] = runes[i].find_all(class_='perk-page__item--active')
            runes[i] = [rune.find('img').get('alt') for rune in runes[i]]
        
        shards = soup.find(class_='fragment-page').find_all(class_='active')
        shards = [to_shard(shard.get('src')) for shard in shards]

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
    except Exception as e:
        print(e)
        build = None
    if role is not None:
        url += "/statistics/{}/build".format(role)
    
    return build

if __name__ == '__main__':
    build = champion_build('teemo', 'aram')
    print(build)