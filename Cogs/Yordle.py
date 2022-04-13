from discord.ext import commands
import discord
from time import time
from math import floor
from Cogs.YordleWords import CHAMPIONS, ABILITIES

class Yordle(commands.Cog):
  """Yordle commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command()
  async def yordle(self, ctx):
    # formatting example
    "Solves the yordle of the day"
    green = ":green_square:"
    yellow = ":yellow_square:"
    black = ":black_square:"

    URL = 'https://yordle.pages.dev/'
    IMAGE_LOCATION = "/static/media/thelogogif.fdcac7dbc86950549bc3.gif"
    image_url = "{}/{}".format(URL, IMAGE_LOCATION)

    champion_round = f'||{get_word_of_day(CHAMPIONS)}||'
    ability_round = f'||{get_word_of_day(ABILITIES)}||'

    embed=discord.Embed(
        title='Yorlde', 
        url= URL,
        color=discord.Color.green()
        )
    embed.set_thumbnail(url=image_url)
    embed.add_field(name="**Champion round**", value=champion_round, inline=False)
    embed.add_field(name="**Champion round**", value=ability_round, inline=False)

    await ctx.send(embed=embed)
    

def get_index():
  # export const getWordOfDay = () => {
  # // January 1, 2022 Game Epoch
  # const epochMs = new Date(2022, 0).valueOf()
  # const now = Date.now()
  # const msInDay = 86400000
  # const index = Math.floor((now - epochMs) / msInDay)
  # const nextday = (index + 1) * msInDay + epochMs

  # January 1, 2022 Game Epoch
  epochMs = 1640991600000
  now = floor(time()*1000)
  msInDay = 86400000
  index = floor((now - epochMs) / msInDay)
  nextday = (index + 1) * msInDay + epochMs
  return index

def get_word_of_day(WORDS):
  index = get_index()
  word = WORDS[index % len(WORDS)]
  return word



if __name__ == '__main__':
  print(get_word_of_day(CHAMPIONS))
  print(get_word_of_day(ABILITIES))