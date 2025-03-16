import disnake
from disnake.ext import commands
from memory_profiler import memory_usage

from utils import EmbedHelper
from custom_types import AnyBot


class PingCommand(commands.Cog):
    def __init__(self, bot: AnyBot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Показать среднюю задержку бота"
    )
    async def ping(self, inter: disnake.AppCmdInter):
        embed = disnake.Embed(
            color=EmbedHelper.transparent_color(),
            title="Понг | 🏓 ",
            description=(
                f"**Средняя задержка**: `{round(self.bot.latency * 1000)}мс`\n"
                f"**Потребление ОЗУ**: `{round(memory_usage()[0])}мб`\n"
            )
        )
        await inter.send(embed=embed, ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(PingCommand(bot))
