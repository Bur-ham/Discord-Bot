from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from src.utils.consts import DEFAULT_PREFIX
from src.models.cache import Cache

if TYPE_CHECKING:
    from src.models.bot import Bot

class General(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def get_or_push_prefix(self, gid: int):
        cache = self.bot.cache.get_cache(gid)
        if not cache:
            cache = Cache(prefix=DEFAULT_PREFIX)
            self.bot.cache.insert_cache(gid, cache)
        return cache

    async def update_cache(self, gid: int, new_prefix: str) -> None:
        cache = self.bot.cache.get_cache(gid)
        connection = self.bot.database.get_connection('config')
        async with connection.cursor() as cursor:
            query = """
            INSERT INTO prefixes(guild_id, prefix) VALUES(?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET prefix = ?
            """
            await cursor.execute(query, (gid, new_prefix, new_prefix))
        cache.prefix = new_prefix
        


    @commands.hybrid_command()
    async def setprefix(self, ctx: commands.Context[Bot], prefix: str = None):
        """
        Command to set a guild's command prefix.

        Usage: {prefix}setprefix <new prefix>
        """
        if not prefix:
            await ctx.send("**Please include a prefix to set the new prefix to!**")
        cache = self.get_or_push_prefix(ctx.guild.id)

        await self.update_cache(ctx.guild.id, prefix) # type: ignore
        await ctx.send(f"Prefix has been succesfully set to: {prefix}")


async def setup(bot: Bot):
    await bot.add_cog(General(bot))