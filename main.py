#import discord #import all the necessary modules
from discord.ext import commands
import os
import random

from Constants import MYTHICS, CHAMPIONS, BOOTS, ITEMS, ROLES, SUMMONER_SPELLS, RUNES, QUOTES

DISCORD_TOKEN = os.environ["TOKEN"]

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(
  command_prefix='$',
  help_command= help_command
  ) #define command decorator


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
          message = "Oh no! Something went wrong while running the command!"

      await ctx.send(message, delete_after=5)
      await ctx.message.delete(delay=5)

  @commands.command()
  async def late(ctx):
    "Calculates if you have early or late game"
    await ctx.send(late_game())

  @commands.command()
  async def quote(ctx):
    "Displays a random champion quote"
    await ctx.send(random_quote())

  @commands.command()
  async def mythic(ctx):
    "Displays one random mythic"
    await ctx.send(random_mythic())

  @commands.command()
  async def item(ctx):
    "Displays one random unique item"
    await ctx.send(random_item())

  @commands.command()
  async def boots(ctx):
    "Displays a random pair of boots"
    await ctx.send(random_boots())

  @commands.command()
  async def champion(ctx):
    "Displays a random champion"
    await ctx.send(random_champion())

  @commands.command()
  async def role(ctx):
    "Displays a random role"
    await ctx.send(random_role())

  @commands.command()
  async def runes(ctx):
    "Displays a runepage with random keystones"
    await ctx.send(random_runes())


  @commands.command(name="sum")
  async def summoner_spell(ctx):
    "Displays a random summoners spell"
    await ctx.send(random_summoner_spell())

  @commands.command()
  async def build(ctx):
    "Generates a random build"
    build = random_build()
    build = '\n'.join(["{}: {}".format(*item) for item in build.items()])
    await ctx.send(build)

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
