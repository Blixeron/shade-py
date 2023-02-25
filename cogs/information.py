from __future__ import annotations
from discord.ext import commands
from discord import *
import assets.constants as constants
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Dust

class Information(commands.Cog):
    """This Cog has commands that show information from different sources."""

    def __init__(self, bot: Dust):
        self.bot: Dust = bot
    
    @app_commands.command(name='ping', description='Check the latency of the bot')
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f'Hey! Latency is {round(self.bot.latency * 1000)}ms.'
        )
        
    ############ WIP ############
    async def show_user_information(self, interaction: Interaction, target: User or Member):
        user = await interaction.client.fetch_user(target.id)

        embed = Embed(title=user)
        embed.set_thumbnail(url=user.avatar.url)

        if user.banner: embed.set_image(url=user.banner.url)

        embed.add_field(name='User', inline=True, value=f'''
**ID:** {user.id}
**Type:** {"Bot" if user.bot else "User"}
**Flags:** {' '.join(list(map(lambda flag: constants.user_flags[flag], user.public_flags.all()))) or 'None'}
**Created at:** <t:{round(user.created_at.timestamp())}> - <t:{round(user.created_at.timestamp())}:R>
        '''
        )

        avatars = [f'[Default]({user.avatar.with_size(1024).url})']

        if interaction.guild and interaction.guild.get_member(user.id) is not None:
            member = (await interaction.guild.fetch_member(user.id))

            embed.color = member.color

            embed.add_field(name='Server', inline=True, value=f'''
**Nick:** {member.nick or 'None'}
**Boosting:** {f"<t:{round(member.premium_since)}> - <t:{round(member.premium_since)}:R>" if member.premium_since else 'No'}
**Joined at:** <t:{round(member.joined_at.timestamp())}> - <t:{round(member.joined_at.timestamp())}:R>
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
        user_embed = (await self.show_user_information(interaction, target or interaction.user))

        await interaction.response.send_message(embed=user_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))