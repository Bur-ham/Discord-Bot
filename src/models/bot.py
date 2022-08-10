
import aiohttp
import discord
from discord.ext import commands

from src.utils.consts import COG_FILES, DEFAULT_PREFIX, INTENTS
from src.utils.functions import get_prefix

from .cache import MasterCache, Cache

from .database import Database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            intents=INTENTS,
            command_prefix=get_prefix
        )

        self.session: aiohttp.ClientSession = None
        self.database: Database = None
        self.cache = MasterCache()

    async def on_ready(self):
        print("I am working!")

    async def start(self, *args, **kwargs):
        async with Database() as self.database:
            async with aiohttp.ClientSession() as self.session:
                return await super().start(*args, **kwargs)

    async def load_cogs(self):
        cogs = COG_FILES
        for cog in cogs:
            await self.load_extension(cog.replace('/', '.')[:-3])

    async def setup_hook(self):
        await self.load_cogs()
