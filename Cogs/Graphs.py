from Cogs.SummonerInfo import get_summoner_mastery
import matplotlib.pyplot as plt
import os
import discord #import all the necessary modules
from discord.ext import commands
import tempfile

mastery_colors = {
    7:'indigo',
    6:'rebeccapurple',
    5:'slateblue',
    4:'royalblue',
    3:'royalblue',
    2:'royalblue',
    1:'royalblue',
}

def set_colors():
    # colors
    plt.rcParams.update({
        "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
        "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
        "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
    }) 
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

class Graphs(commands.Cog):
  """A collection of commands to create graphs"""

  def __init__(self, bot: commands.Bot):
      self.bot = bot

  @commands.command(name='masterygraph')
  async def create_mastery_graph(self, ctx, *summoner_name):
    "Generates a graph of the mastery of a summoner"
    if summoner_name:
        summoner_name = ' '.join(summoner_name)
    async with ctx.typing():
        graph = create_mastery_graph(summoner_name)
        if graph:
            await ctx.send(file=discord.File(graph))
            os.remove(graph)
        else:
            await ctx.send('Failed to generate graph.')

def create_mastery_graph(summoner_name):
    mastery = get_summoner_mastery(summoner_name)
    if mastery is None:
        return None
    total_mastery = sum([int(champion.get('Points')) for champion in mastery])
    mastery = mastery[:30]
    points = [int(champion.get('Points')) for champion in mastery]
    names = [champion.get('Champion') for champion in mastery]
    colors = [mastery_colors.get(champion.get('Level')) for champion in mastery]

    # Figure Size
    fig, ax = plt.subplots(figsize =(16, 9))
    
    # Horizontal Bar Plot
    ax.barh(names, points, color=colors)
    
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    # Add x, y gridlines
    ax.grid(visible = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
    # Show top values
    ax.invert_yaxis()
    
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='white')
    
    # Add Plot Title
    ax.set_title(f'Mastery of {summoner_name} - Total mastery {"{:,}".format(total_mastery)} points',
                loc ='left', )
    
    # Add Text watermark
    fig.text(0.9, 0.15, 'League Of Chance', fontsize = 12,
            color ='grey', ha ='right', va ='bottom',
            alpha = 0.7)
    

    # Show Plot
    fp = tempfile.NamedTemporaryFile() 
    fp = f'{fp.name}.png'
    plt.savefig(fp)
    return fp

set_colors()

if __name__ == '__main__':
    create_mastery_graph('a penguin')
