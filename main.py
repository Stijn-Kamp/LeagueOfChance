from typing import Text
import discord #import all the necessary modules
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# for champion_counter
from bs4 import BeautifulSoup
import requests

from Constants import MYTHICS, CHAMPIONS, BOOTS, ITEMS, ROLES, SUMMONER_SPELLS, RUNES, QUOTES, SHARDS, ABILITIES

load_dotenv()
os.environ["TOKEN"]
DISCORD_TOKEN = os.environ["TOKEN"]

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(
  command_prefix='$',
  help_command= help_command
  ) #define command decorator

# Functions
def champion_counter(champion):
  BASE_URL = "https://lolcounter.com/champions/{}"
  URL = BASE_URL.format(champion.replace("'",""))
  try:
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'html.parser')
    tips = soup.find_all("span", class_="_tip")
    tip = random.choice(tips).text
  except Exception as e:
    print(e)
    tip = "Sorry, I couldn't find a tip to play against {}".format(champion)
  return tip

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

# random functions
def random_quote():
  return random.choice(QUOTES)

def random_mythic():
  return random.choice(MYTHICS)

def random_item():
  return random.choice(ITEMS)

def random_boots():
  return random.choice(BOOTS)

def random_champion():
  return random.choice(CHAMPIONS)

def random_role():
  return random.choice(ROLES)

def random_summoner_spell():
  return random.choice(SUMMONER_SPELLS)

def random_ability_order():
  abilities = ABILITIES
  random.shuffle(abilities)
  return abilities

def random_runes():
  pagename = random.choice(list(RUNES.keys()))
  runepage = RUNES[pagename]
  keystones = []
  for i in range(len(runepage)):
    keystone = random.choice(runepage[i])
    keystones.append(keystone)
  
  runepage = {
    "name" : pagename,
    "keystones" : keystones
  }
  return runepage

def random_shards():
  return [random.choice(shards) for shards in SHARDS]

def random_build():
  champion = random_champion()
  role = random_role()

  ability_order = random_ability_order()
  summoner_spells = []
  if role == "Jungle": summoner_spells = summoner_spells + ["Smite"] 
  while len(summoner_spells) < 2:
    summoner_spell = random_summoner_spell()
    if summoner_spell not in summoner_spells:
      summoner_spells.append(summoner_spell)

  primairy_runes = random_runes()
  secondary_runes = None
  while secondary_runes is None:
    runes = random_runes()
    if runes['name'] != primairy_runes['name']:
      runes['keystones'].pop(0) # remove the first runepage
      runes['keystones'].pop(random.randrange(0, len(runes['keystones'])))
      secondary_runes = runes

  shards = random_shards()

  #items
  boots = random_boots()
  mythic = random_mythic()
  items = []
  while len(items) < 4:
    item = random_item()
    if item not in items:
      items.append(item)

  build = {
    'Champion': champion,
    'Role': role,
    'Primary runes': primairy_runes,
    'Secondary runes': secondary_runes,
    'Shards': shards,
    'Summoner spells': summoner_spells,
    'Abilities': ability_order,
    'Boots': boots,
    'Mythic': mythic,
    'Items': items
  }
  return build

def late_game():
  i = random.randrange(0, 10)
  return('Ja' if i < 6 else 'Nee')

# command handling ----------------------------------
class ErrorHandler(commands.Cog):
  """A cog for global error handling."""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
      """A global error handler cog."""
      if isinstance(error, commands.CommandNotFound):
          return  # Return because we don't want to show an error for every command not found
      elif isinstance(error, commands.CommandOnCooldown):
          message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
      elif isinstance(error, commands.MissingPermissions):
          message = "You are missing the required permissions to run this command!"
      elif isinstance(error, commands.UserInputError):
          message = "Something about your input was wrong, please check your input and try again!"
      else:
          print(error)
          message = "Oh no! Something went wrong while running the command!"

      await ctx.send(message, delete_after=5)
      await ctx.message.delete(delay=5)

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

        embed=discord.Embed(color=discord.Color.green())
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




class RandomCommands(commands.Cog):
  """A collection of the random commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command()
  async def late(self, ctx):
    "Calculates if you have early or late game"
    await ctx.send(late_game())

  @commands.command()
  async def counter(self, ctx, *champion):
    "Gives a random tip to counter a champion"
    champion = '-'.join(champion)
    if champion:
      await ctx.send(champion_counter(champion))
    else:
      await ctx.send("Please give the name of the champion you would like to counter.")



  @commands.command()
  async def quote(self, ctx):
    "Displays a random champion quote"
    await ctx.send(random_quote())

  @commands.command()
  async def mythic(self, ctx):
    "Displays one random mythic"
    await ctx.send(random_mythic())

  @commands.command()
  async def item(self, ctx):
    "Displays one random unique item"
    await ctx.send(random_item())

  @commands.command()
  async def boots(self, ctx):
    "Displays a random pair of boots"
    await ctx.send(random_boots())

  @commands.command()
  async def champion(self, ctx):
    "Displays a random champion"
    await ctx.send(random_champion())

  @commands.command()
  async def role(self, ctx):
    "Displays a random role"
    await ctx.send(random_role())

  @commands.command()
  async def runes(self, ctx):
    "Displays a runepage with random keystones"
    runes = random_runes()
    name = runes.get('name')
    keystones = runes.get('keystones')
    await ctx.send("{}: {}".format(name, ', '.join(keystones)))

  @commands.command()
  async def shards(self, ctx):
    "Displays random rune shards"
    shards = random_shards()
    await ctx.send(', '.join(shards))

  @commands.command(name="sum")
  async def summoner_spell(self, ctx):
    "Displays a random summoners spell"
    await ctx.send(random_summoner_spell())

  @commands.command(name="abilities")
  async def summoner_spell(self, ctx):
    "Displays the abilities in random order"
    abilities = random_ability_order()
    await ctx.send(', '.join(abilities))


  @commands.command()
  async def build(self, ctx):
    # https://python.plainenglish.io/python-discord-bots-formatting-text-efca0c5dc64a
    # formatting example
    "Generates a random build"
    PATCH = '11.24.1'
    build = random_build()
    champion = build.get('Champion')
    primary = build.get('Primary runes')
    secondary = build.get('Secondary runes')
    shards = ', '.join(build.get('Shards'))
    sums = ', '.join(build.get('Summoner spells'))
    abilities = ', '.join(build.get('Abilities'))
    items = ', '.join(build.get('Items'))

    icon_url = champion.split('&', 1)[0].replace('.', '').replace(' ', '').replace(' ', ' ')
    icon_url = "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(PATCH, icon_url)
    embed=discord.Embed(color=discord.Color.blue())
    embed.set_author(
      name="{}".format(champion), 
      icon_url=icon_url
    )

    embed.add_field(name="**Role**", value=build.get('Role'), inline=False)
    embed.add_field(name="**Primary runes - {}**".format(primary.get('name')), value=', '.join(primary.get('keystones')), inline=False)
    embed.add_field(name="**Secondary runes - {}**".format(secondary.get('name')), value=', '.join(secondary.get('keystones')), inline=False)
    embed.add_field(name="**Shards**", value=shards, inline=False)
    embed.add_field(name="**Summoner spells**", value=sums, inline=False)
    embed.add_field(name="**Ability order**", value=abilities, inline=False)
    embed.add_field(name="**Boots**", value=build.get('Boots'), inline=False)
    embed.add_field(name="**Mythic**", value=build.get('Mythic'), inline=False)
    embed.add_field(name="**Items**", value=items, inline=False)

    await ctx.send(embed=embed)



def setup(bot: commands.Bot):
  bot.add_cog(ErrorHandler(bot))
  bot.add_cog(RandomCommands(bot))
  bot.add_cog(SummonerCommands(bot))

# bot funcions--------------------------------------------
@bot.event #print that the bot is ready to make sure that it actually logged on
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)

@bot.event
async def on_message(message):
    #Return if message is from the bot itself
    if message.author == bot.user:
      return  

    mention = f'<@!{bot.user.id}>'
    if mention == message.content:
        await message.channel.send(random_quote())

    if 'late' in message.content.lower().split(' '):
        await message.channel.send(late_game())
    
    await bot.process_commands(message)

setup(bot)
bot.run(DISCORD_TOKEN) #run the client using using my bot's token
