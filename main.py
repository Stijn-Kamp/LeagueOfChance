import discord #import all the necessary modules
from discord.ext import commands
import os
import random

# for champion_counter
from bs4 import BeautifulSoup
import requests

from Constants import MYTHICS, CHAMPIONS, BOOTS, ITEMS, ROLES, SUMMONER_SPELLS, RUNES, QUOTES

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

def random_build():
  champion = random_champion()
  role = random_role()

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
    'Summoner spells': summoner_spells,
    'Boots': boots,
    'Mythic': mythic,
    'Items': items
  }
  return build

def late_game():
  i = random.randrange(0, 10)
  return('Ja' if i < 6 else 'Nee')

# command handling ----------------------------------
class CommandsHandler(commands.Cog):
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

  @commands.command()
  async def late(self, ctx):
    "Calculates if you have early or late game"
    await ctx.send(late_game())

  @commands.command()
  async def counter(self, ctx, *champion):
    champion = '-'.join(champion)
    "Gives a random tip to counter a champion"
    await ctx.send(champion_counter(champion))


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
    await ctx.send(random_runes())


  @commands.command(name="sum")
  async def summoner_spell(self, ctx):
    "Displays a random summoners spell"
    await ctx.send(random_summoner_spell())


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
    sums = ', '.join(build.get('Summoner spells'))
    items = ', '.join(build.get('Items'))

    embed=discord.Embed(color=discord.Color.blue())
    embed.set_author(
      name="{}".format(champion), icon_url="http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(PATCH, champion)
    )

    embed.add_field(name="**Role**", value=build.get('Role'), inline=False)
    embed.add_field(name="**Primary runes - {}**".format(primary.get('name')), value=', '.join(primary.get('keystones')), inline=False)
    embed.add_field(name="**Secondary runes - {}**".format(secondary.get('name')), value=', '.join(secondary.get('keystones')), inline=False)
    embed.add_field(name="**Summoner spells**", value=sums, inline=False)
    embed.add_field(name="**Boots**", value=build.get('Boots'), inline=False)
    embed.add_field(name="**Mythic**", value=build.get('Mythic'), inline=False)
    embed.add_field(name="**Items**", value=items, inline=False)

    await ctx.send(embed=embed)

  @commands.command()
  async def embed(self, ctx):
      embed=discord.Embed(
      title="Text Formatting",
          url="https://realdrewdata.medium.com/",
          description="Here are some ways to format text",
          color=discord.Color.blue())
      embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData", icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
      #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
      embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
      embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
      embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
      embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
      embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
      embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
      embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
      embed.set_footer(text="Learn more here: realdrewdata.medium.com")
      await ctx.send(embed=embed)

def setup(bot: commands.Bot):
  bot.add_cog(CommandsHandler(bot))




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
    if mention in message.content:
        await message.channel.send(random_quote())

    if 'late' in message.content.lower().split(' '):
        await message.channel.send(late_game())
    
    await bot.process_commands(message)

setup(bot)
bot.run(DISCORD_TOKEN) #run the client using using my bot's token

