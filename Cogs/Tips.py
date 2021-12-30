from typing import Text
import discord #import all the necessary modules
from discord.ext import commands
import os
import random

# for champion_counter
from bs4 import BeautifulSoup
import requests


class Tips(commands.Cog):
  """A collection of tips"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command()
  async def counter(self, ctx, *champion):
    "Gives a random tip to counter a champion"
    champion = '-'.join(champion)
    if champion:
      await ctx.send(champion_counter(champion))
    else:
      await ctx.send("Please give the name of the champion you would like to counter.")

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
