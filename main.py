from discord.ext import commands

from src.utils.consts import TOKEN
from src.models.bot import Bot

bot = Bot()

@bot.check
async def ready_check(ctx: commands.Context[Bot]):
    await bot.wait_until_ready()
    return True

bot.run(TOKEN)