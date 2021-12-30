from typing import Text
import discord #import all the necessary modules
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from datetime import datetime
class SummonerCommands(commands.Cog):
  """A collection of the summoner commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command(name='info')
  async def summoner_info(self, ctx, *summoner_name):
    # formatting example
    "Gives information on a summoner"
    if summoner_name:
      summoner_info = get_summoner_info('+'.join(summoner_name))
      if summoner_info:
        summoner_name = summoner_info.get('Summoner name')
        summoner_icon = summoner_info.get('Icon')
        summoner_level = summoner_info.get('Level')
        win_rate = summoner_info.get('Win ratio')
        solo_rank = summoner_info.get('Solo rank')
        flex_rank = summoner_info.get('Flex rank')

        embed=discord.Embed(
            #title='Summoner info',
            color=discord.Color.green()
        )
        embed.set_author(
          name="{}".format(summoner_name), 
          icon_url=summoner_icon
        )
        embed.add_field(name="**Level**", value=summoner_level, inline=False)
        embed.add_field(name="**Win ratio**", value=win_rate, inline=False)
        embed.add_field(name="**Solo rank**", value=solo_rank, inline=False)
        embed.add_field(name="**Flex rank**", value=flex_rank, inline=False)

        await ctx.send(embed=embed)
      else:
        await ctx.send("Sorry, I couldn't find info on {}".format(' '.join(summoner_name)))

    else:
      await ctx.send("Please give the name of the summoner you would like to have info on.")

  @commands.command(name='mastery')
  async def summoner_mastery(self, ctx, *summoner_name):
    # formatting example
    "Gives the mastery poinst of a summoner"
    if summoner_name:
        lookup_name = '+'.join(summoner_name)
        summoner_info = get_summoner_info(lookup_name)
        mastery = get_summoner_mastery(lookup_name, amount=20)

        if mastery:
            description = ''
            for item in mastery:
                item = "**{:15}** Lvl {} - {}\n".format(item.get('Champion'), item.get('Level'), item.get('Points'))
                print(item)
                description += item
            
        else:
            description = "Mastery not found"

        if summoner_info:
            summoner_name = summoner_info.get('Summoner name')
            summoner_icon = summoner_info.get('Icon')
            embed=discord.Embed(
                title='Mastery', 
                description=description, 
                color=discord.Color.gold()
                )
            embed.set_author(
            name="{}".format(summoner_name), 
            icon_url=summoner_icon
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't find the mastery of {}".format(' '.join(summoner_name)))

    else:
      await ctx.send("Please give the name of the summoner you would like to have info on.")


# Functions
def get_summoner_info(summoner_name, server='euw'):
  BASE_URL = "https://{}.op.gg/summoner/userName={}"
  URL = BASE_URL.format(server, summoner_name)
  try:
    headers = {'user-agent': 'LeagueOfChange/1.0.0'}
    page = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    summoner_name = soup.find(class_='Name')
    if(summoner_name is None):
      return None
    else: 
      summoner_name = summoner_name.text
    icon = 'https:' + soup.find(class_='ProfileImage')['src']
    level = soup.find(class_='Level').text
    win_ratio = soup.find_all(class_='WinRatioGraph')[-1].find(class_='Text').text
    solo_rank = soup.find(class_='TierRank').text.replace('\n','').replace('\t','')
    flex_rank = soup.find(class_='sub-tier__rank-tier').text.replace('\n','').replace('\t','')
    summoner_info = {
      'Summoner name': summoner_name,
      'Icon': icon,
      'Level': level,
      'Win ratio': win_ratio,
      'Solo rank': solo_rank,
      'Flex rank': flex_rank
    }
    return summoner_info
  except Exception as e:
    print(e)
    summoner_info = None
  return summoner_info


def get_summoner_mastery(summoner_name, server='euw', amount=0):
  BASE_URL = "https://championmastery.gg/summoner?summoner={}&region={}"
  URL = BASE_URL.format(summoner_name, server)
  try:
    headers = {'user-agent': 'LeagueOfChange/1.0.0'}
    page = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    mastery = soup.find(class_='well').find('tbody').find_all('tr')

    if amount != 0:
        mastery = mastery[:amount]

    summoner_mastery = []
    for item in mastery:
        item = item.find_all('td')

        champion_name = item[0].find('a').text
        level = item[1].text
        chest = (item[3].get('data-value') == '1')
        last_played = datetime.fromtimestamp(int(item[4].get('data-value')[:-3])).strftime("%d/%m/%Y, %H:%M:%S")
        progress = item[5].get('title')
        points = int(item[6].get('data-value'))
        points = points if points < 90000 else 'N/A'

        item = {
            "Champion": champion_name,
            "Level": level,
            "Chest": chest,
            "Last played": last_played,
            "Progress": progress,
            "Points": points
        }
        summoner_mastery.append(item)
  except Exception as e:
    print(e)
    summoner_mastery = None
  return summoner_mastery

