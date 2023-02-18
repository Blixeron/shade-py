from discord.ext import commands
from discord import *

class Utility(commands.Cog):
    """The description for Utility goes here."""

    def __init__(self, bot):
        self.bot = bot

    ############# WIP #############
    @app_commands.command(name='avatar', description='Show the avatar of someone')
    @app_commands.describe(
        target='Who you want to check the avatar of; if not provided, defaults to yourself',
        # size='Size of the image, defaults to 1024 pixels',
        # format='Format of the image, defaults to png or gif if the avatar is animated'
    )
    async def avatar(self, interaction: Interaction, target: User):
        await interaction.response.send_message(target.avatar.url)

async def setup(bot):
    await bot.add_cog(Utility(bot))
