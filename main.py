import os
from dotenv import load_dotenv
from Cogs.Bot import DiscordBot

if __name__ == '__main__':
  load_dotenv()
  os.environ["TOKEN"]
  DISCORD_TOKEN = os.environ["TOKEN"]

  DiscordBot(DISCORD_TOKEN)