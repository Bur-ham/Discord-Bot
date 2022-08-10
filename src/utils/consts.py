import os
from glob import glob

import discord
from dotenv import load_dotenv

load_dotenv('./.env', verbose=True)

COG_FILES = glob("src/cogs/*.py", recursive=True)
DEFAULT_PREFIX = ">>"
TOKEN = os.getenv("TOKEN")

INTENTS = discord.Intents.default()

INTENTS.members = True
INTENTS.message_content = True

INTENTS.typing = False
INTENTS.integrations = False
INTENTS.dm_typing = False
