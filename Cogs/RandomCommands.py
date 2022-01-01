from typing import Text
import discord #import all the necessary modules
from discord.ext import commands
import random
from dotenv import load_dotenv


from Cogs.Constants import MYTHICS, BOOTS, ITEMS, ROLES, RUNES, QUOTES, SHARDS, ABILITIES
from Cogs.RemoteData import get_champion_image, champions, get_champion_description, summoner


class RandomCommands(commands.Cog):
  """A collection of the random commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command()
  async def late(self, ctx):
    "Calculates if you have early or late game"
    await ctx.send(late_game())

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
    champion = champions.get(random_champion())
    if champion:
      await ctx.send(champion.get('name'))
    else:
      await ctx.send("Couldn't generate a champion")

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
  async def summability_order(self, ctx):
    "Displays the abilities in random order"
    abilities = random_ability_order()
    await ctx.send(', '.join(abilities))


  @commands.command(name="random", aliases=['rb'])
  async def random_build(self, ctx):
    # https://python.plainenglish.io/python-discord-bots-formatting-text-efca0c5dc64a
    # formatting example
    "Generates a random build"
    PATCH = '11.24.1'
    build = random_build()
    lookup_name = build.get('Champion')
    champion = champions.get(lookup_name)
    champion_name = champion.get('name')
    primary = build.get('Primary runes')
    secondary = build.get('Secondary runes')
    shards = ', '.join(build.get('Shards'))
    sums = ', '.join(build.get('Summoner spells'))
    abilities = ', '.join(build.get('Abilities'))
    items = ', '.join(build.get('Items'))
    icon_url = get_champion_image(lookup_name)
    description = get_champion_description(lookup_name)

    embed=discord.Embed(
        color=discord.Color.blue(),
        description = description
    )
    embed.set_author(
      name="{}".format(champion_name), 
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

# Functions
def random_quote():
  return random.choice(QUOTES)

def random_mythic():
  return random.choice(MYTHICS)

def random_item():
  return random.choice(ITEMS)

def random_boots():
  return random.choice(BOOTS)

def random_champion():
  champion_list = list(champions.keys())
  return random.choice(champion_list)

def random_role():
  return random.choice(ROLES)

def random_summoner_spell():
  spells = list(summoner.keys())
  summoner_spells = []
  for spell in spells:
    if 'CLASSIC' in summoner.get(spell).get('modes'):
      summoner_spells.append(spell)
  summoner_spell = random.choice(summoner_spells)
  summoner_spell = summoner.get(summoner_spell).get('name')
  return summoner_spell

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
  return('Yes' if i < 6 else 'No')