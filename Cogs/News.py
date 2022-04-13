from sre_parse import CATEGORIES
import discord #import all the necessary modules
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from datetime import datetime

CATEGORIES = [
    'community',
    'dev',
    'esports',
    'game-updates',
    'lore',
    'media',
    'merch',
    'riot-games',
]


class News(commands.Cog):
  """A collection of the summoner commands"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command(name='categories')
  async def list_categories(self, ctx):
    "Lists the available categories"
    await ctx.send(', '.join(CATEGORIES))


  @commands.command(name='news')
  async def news(self, ctx, *command):
    # formatting example
    "Retrieves League of legends news"
    category = None

    for s in command:
        if s.startswith('--category'):
            category = s.split('=')[-1]
            

    articles = get_news(category)

    for article in articles:
        author = article.get('Author')
        date_time = article.get('Time')
        date_time = date_time.strftime('%d %B %Y')
        footer = date_time
        article_description=article.get('Description')
        article_description = article_description if article_description else discord.Embed.Empty
        if author:
            footer = "{} - {}".format(author, footer)
            
        embed=discord.Embed(
            title=article.get('Title'), 
            url=article.get('Url'),
            color=discord.Color.purple(),
            description=article_description
            )
        embed.set_thumbnail(url=article.get('Image'))
        embed.set_footer(text=footer)
        embed.set_author(name=article.get('Category'))
        await ctx.send(embed=embed)
    
def get_news(category = None):
    BASE_URL = 'https://www.leagueoflegends.com'
    NEWS_LOCATION = '/en-us/news/'
    URL = BASE_URL+NEWS_LOCATION

    if category:
        URL = f'{URL}/{category}'
    headers = {'user-agent': 'LeagueOfChange/1.0.0'}
    page = requests.get(URL, headers=headers)
    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text, 'html.parser')
    
    articles_soup = soup.find_all(class_='style__Wrapper-sc-1h41bzo-0')

    articles = []
    for article in articles_soup:
        img = article.find('img').get('src')
        category = article.find(class_='style__Category-d3b0qh-0')
        category = category.text if category else None
        title = article.find('h2')
        title = title.text if title else None
        author = article.find(class_='style__Author-sc-1h41bzo-11')
        author = author.text if author else None
        description = article.find(class_="style__Blurb-sc-1h41bzo-9 cSdFEy")
        description = description.text if description else None
        time = article.find('time')
        if time:
            time = time.get('datetime')
            time = time.replace('T', '').replace('Z', '')
            time = datetime.strptime(time, '%Y-%m-%d%H:%M:%S.%f')#f'{datetime(time):%Y-%m-%d %H:%M:%S%z}'
        url = article.get('href')
        url = url if URL in url else URL + url

        article = {
            'Title': title,
            'Image': img,
            'Category': category,
            'Description': description,
            'Author': author,
            'Time': time,
            'Url': url,
        }
        articles.append(article)
    return articles

if __name__ == '__main__': 
    news = (get_news(CATEGORIES[7]))
    for new in news:
        print(new)