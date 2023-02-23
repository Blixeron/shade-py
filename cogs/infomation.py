from __future__ import annotations
from discord.ext import commands
from discord import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Dust

class Information(commands.Cog):
    """This Cog has commands that show information from different sources."""

    def __init__(self, bot: Dust):
        self.bot: Dust = bot
    
    @app_commands.command(
        name='ping',
        description='Check the bot latency'
    )
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f'Hey! Latency is {round(self.bot.latency * 1000)}ms.'
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))