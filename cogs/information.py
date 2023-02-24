from __future__ import annotations
from discord.ext import commands
from discord import *
import utils.http
import asyncio
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
        
    ############ WIP ############
    async def show_user_information(self, bot: Dust, interaction: Interaction, target: User or Member):
        future_data = utils.http.get_json(f'https://discord.com/api/users/{target.id}', {
            'Authorization': f'Bot {bot.config.token}'
        })

        data: list = await asyncio.gather(future_data)

        embed = Embed(title=target, color=Colour.from_str(data[0]["banner_color"]))
        embed.set_thumbnail(url=target.avatar.url)

        if target.banner: embed.set_image(url=target.banner.url)

        embed.add_field(name='User', value=f'''
**ID:** {target.id}
**Type:** {"Bot" if target.bot else "User"}
        '''
        )

        return embed
    
    @app_commands.command(
        name='user',
        description='Show information about a Discord user'
    )
    @app_commands.describe(
        target='Who you want to check the information of; if not provided, defaults to yourself'
    )
    async def user(self, interaction: Interaction, target: User = None):
        user_embed = (await self.show_user_information(self.bot, interaction, target or interaction.user))

        await interaction.response.send_message(embed=user_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))