import os
from discord.ext import commands
from discord import *

class Info(commands.Cog):
    """This Cog has commands that show information from different sources."""

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name='ping',
        description='Check the bot latency'
    )
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f'Hey! Latency is {round(self.bot.latency * 1000)}ms.'
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))