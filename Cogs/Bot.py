import traceback
import sys

from typing import Text
import discord #import all the necessary modules
from discord.ext import commands

from Cogs.RandomCommands import RandomCommands, random_quote, late_game
from Cogs.SummonerInfo import SummonerCommands
from Cogs.Teams import Teams
from Cogs.Tips import Tips
from Cogs.News import News

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
        traceback.print_exc(file=sys.stdout)
        print(error)
        message = "Oh no! Something went wrong while running the command!"

      await ctx.send(message, delete_after=5)
      await ctx.message.delete(delay=5)



def create_bot():
    help_command = commands.DefaultHelpCommand(
        no_category = 'Commands'
    )
    bot = commands.Bot(
    command_prefix='$',
    help_command= help_command
    ) #define command decorator

    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(RandomCommands(bot))
    bot.add_cog(SummonerCommands(bot))
    bot.add_cog(Teams(bot))
    bot.add_cog(Tips(bot))
    bot.add_cog(News(bot))


    return bot

class DiscordBot():
    bot = create_bot()

    def __init__(self, token):
        if self.bot is None:
            self.bot = self.create_bot()

        self.bot.run(token) #run the client using using my bot's token

    # bot funcions--------------------------------------------
    @bot.event #print that the bot is ready to make sure that it actually logged on
    async def on_ready():
        print('Logged in as:')
        print(DiscordBot.bot.user.name)

    @staticmethod
    @bot.event
    async def on_message(message):
        #Return if message is from the bot itself
        if message.author == DiscordBot.bot.user:
            return  

        mention = f'<@!{DiscordBot.bot.user.id}>'
        if mention == message.content:
            await message.channel.send(random_quote())

        if 'late' in message.content.lower().replace('?', '').split(' '):
            await message.channel.send(late_game())
        
        await DiscordBot.bot.process_commands(message)