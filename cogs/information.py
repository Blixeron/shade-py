from __future__ import annotations
import sys
from typing import TYPE_CHECKING

from discord.ext import commands
from discord import *
import discord


if TYPE_CHECKING:
    from main import Shade


class Information(commands.Cog):
    """This Cog has commands that show information from Discord."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """Shows my current latency with the Discord API."""

        await interaction.response.send_message(
            f'Hey! Latency is **{round(self.bot.latency * 1000)}ms.**'
        )

    @app_commands.command()
    async def about(self, interaction: Interaction):
        """Shows information about me."""

        embed = Embed(
            title='Information about me',
            description=(
                f'{self.bot.application.description}\n\n'
                f'[GitHub Repository]({self.bot.config.github_repo})'
            ),
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.add_field(
            name='Development',
            inline=True,
            value=(
                f'**Developer:** [{self.bot.application.owner}](https://discord.com/users/{self.bot.owner_id})\n'
                f'**Running on:** Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}\n'
                f'**Library:** discord.py {discord.__version__}'
            ),
        )

        embed.add_field(
            name='Counts',
            value=(
                f"**Servers I'm in:** {len(self.bot.guilds)}\n"
                f"**Users I'm helping:** {len(list(filter(lambda user: not user.bot, self.bot.users)))}\n"
                f'**Total commands:** {len(self.bot.tree._get_all_commands())}\n'
                f'**Total cogs:** {len(self.bot.cogs)}'
            ),
        )

        embed.add_field(
            name='Connection',
            inline=False,
            value=(
                f'**Up since:** <t:{self.bot.uptime}> - <t:{self.bot.uptime}:R>\n'
                f'**Latency:** {round(self.bot.latency * 1000)}ms'
            ),
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))
