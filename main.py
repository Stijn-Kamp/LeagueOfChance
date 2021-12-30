import os
from dotenv import load_dotenv
from Cogs.Bot import DiscordBot
load_dotenv()
os.environ["TOKEN"]
DISCORD_TOKEN = os.environ["TOKEN"]

DiscordBot(DISCORD_TOKEN)