from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Message

from src.models.cache import Cache

from .consts import DEFAULT_PREFIX

if TYPE_CHECKING:
    from src.models.bot import Bot

async def get_prefix(bot: Bot, message: Message):
    if message.guild:
        cache = bot.cache.get_cache(message.guild.id)
        if not cache :
            connection = bot.database.get_connection("config")
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (message.guild.id,))
                record = await cursor.fetchone()
            prefix = record[0] if record else DEFAULT_PREFIX
            bot.cache.insert_cache(message.guild.id, Cache(prefix=prefix))
        else:
            prefix = cache.prefix
    else:
        prefix = DEFAULT_PREFIX
    return prefix
        