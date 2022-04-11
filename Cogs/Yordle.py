from typing import Text
from discord.ext import commands
import discord
from bs4 import BeautifulSoup
import requests

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

    champion_round = ''.join(7*green)
    ability_round = ''.join(7*green)

    embed=discord.Embed(
        title='Yorlde', 
        url='https://yordle.pages.dev/',
        color=discord.Color.green()
        )
    embed.add_field(name="**Champion round**", value=champion_round, inline=False)
    embed.add_field(name="**Ability round**", value=ability_round, inline=False)

    await ctx.send(embed=embed)
    

def get_letter_amount():
  URL = "https://yordle.pages.dev/"

  try:
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'html.parser')
    letters = soup.find_all("div")
    print(soup)
    #letters = len(letters)
  except Exception as e:
    print(e)
    letters = 0
  return letters

if __name__ == '__main__':
  print(get_letter_amount())