from discord.ext import commands
from bs4 import BeautifulSoup
import requests

class Backstory(commands.Cog):
  """A collection of the champion backstory commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot


  @commands.command(name='biography')
  async def biography(self, ctx, *command):
    "Retrieves biography of a champion"
    
    champion = ''.join(command)
    
    async with ctx.typing():
        biography = get_biography(champion)
        for paragraph in split_text(biography):
            await ctx.send(paragraph)

  @commands.command(name='story')
  async def story(self, ctx, *command):
    "Retrieves the story of a champion"
    
    champion = ''.join(command)
    
    async with ctx.typing():
        story = get_backstory(champion)
        for paragraph in split_text(story):
            await ctx.send(paragraph)

def split_text(text):
    TEXT_LIMIT = 2000
    text = text.split('.')
    split_text = []

    joined_sentence = ''
    for sentence in text:
        if len(sentence) == 0:
            continue
        elif len(joined_sentence) + len(sentence) + 2 <= TEXT_LIMIT:
            if not sentence.startswith(' ') and joined_sentence.endswith('.'):
                sentence = ' ' + sentence
            joined_sentence = f'{joined_sentence}{sentence}.'
        else:
            split_text.append(joined_sentence.strip())
            joined_sentence = f'{sentence}.'
    split_text.append(joined_sentence.strip())
    return split_text
    
def get_champion_background(info, champion, lang=None):
    if lang is None:
        lang = 'en_US'
    champion = str.lower(champion)

    if info == 'biography':
        url = f"https://universe.leagueoflegends.com/{lang}/story/champion/{champion}/"
    elif info == 'story':
        url = f"https://universe.leagueoflegends.com/{lang}/story/{champion}-color-story/"

    headers = {'user-agent': 'LeagueOfChange/1.0.0'}
    page = requests.get(url, headers=headers)
    page.encoding = page.apparent_encoding
    text = page.text
    text = text.replace('"C"', "'C'") # Bugfix for Caitlyn story
    soup = BeautifulSoup(text, 'html.parser')
    backstory = soup.find("meta", {'name': 'description'})
    return backstory.get('content') if backstory else None

def get_backstory(champion, lang=None):
    return get_champion_background('story', champion, lang)

def get_biography(champion, lang=None):
    return get_champion_background('biography', champion, lang)

if __name__ == '__main__': 
    champion = 'ivern'
    backstory = get_biography(champion)
    print((split_text(backstory)))
