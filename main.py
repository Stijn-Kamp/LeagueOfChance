import os
from dotenv import load_dotenv
from Cogs.Bot import DiscordBot
from discord import LoginFailure

def get_token():
  """
  Loads discord token
  """
  TOKEN_NAME = "TOKEN"

  load_dotenv()
  try:
    os.environ[TOKEN_NAME]
    token = os.environ[TOKEN_NAME]
  except KeyError:
    token = None
  return token


if __name__ == '__main__':
  DISCORD_TOKEN = get_token()
  if DISCORD_TOKEN is None:
    print("Please make sure that the token is stored in the right place.")
    exit(0)

try:
  DiscordBot(DISCORD_TOKEN)
except LoginFailure:
  print("Improper token has been passed.")
finally:
  exit(0)