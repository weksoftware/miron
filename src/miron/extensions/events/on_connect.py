from loguru import logger
from disnake.ext import commands

from custom_types import AnyBot


class OnConnectEvent(commands.Cog):
    def __init__(self, bot: AnyBot):
        self.bot = bot

    @commands.Cog.listener(name="on_connect")
    async def on_connect(self):
        logger.info(f"Connected as {self.bot.user} (ID: {self.bot.user.id})")


def setup(bot: commands.InteractionBot):
    bot.add_cog(OnConnectEvent(bot))
