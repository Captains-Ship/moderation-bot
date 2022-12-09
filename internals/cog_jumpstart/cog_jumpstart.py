import logging

import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("Bot").getChild(self.__class__.__name__)


def ms(cog):
    async def setup(bot):
        await bot.add_cog(cog(bot))
    return setup