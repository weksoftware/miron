import disnake
from loguru import logger
from disnake.ext import commands

from custom_types import AnyBot


class OnReadyEvent(commands.Cog):
    def __init__(self, bot: AnyBot):
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        logger.info("Bot is ready")
        
        await self.bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="👀🦆"))


def setup(bot: commands.InteractionBot):
    bot.add_cog(OnReadyEvent(bot))
