from __future__ import annotations
from discord.ext import commands
from discord import *
import discord
import assets.constants as constants
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Shade

class Information(commands.Cog):
    """This Cog has commands that show information from Discord."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

        self.user_ctx_menu = app_commands.ContextMenu(
            name='User Information',
            callback=self.user_information
        )
        self.bot.tree.add_command(self.user_ctx_menu)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.user_ctx_menu.name, type=self.user_ctx_menu.type)
    
    @app_commands.command(description='Check the latency of the bot')
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f'Hey! Latency is **{round(self.bot.latency * 1000)}ms.**'
        )

    @app_commands.command(description='Show information about Shade')
    async def about(self, interaction: Interaction):
        embed = Embed(title='Information about me', description=f'{self.bot.application.description}\n\n'
                      '[Check out my GitHub Repository!](https://github.com/Drazkai/shade)')

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.add_field(name='Development', inline=True, value=f'''
**Developer:** [{self.bot.application.owner}](https://discord.com/users/{self.bot.owner_id})
**Running on:** Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}
**Library:** discord.py {discord.__version__}
        '''
        )

        embed.add_field(name='Counts', inline=False, value=f'''
**Servers I'm in:** {len(self.bot.guilds)}
**Users I'm helping:** {len(list(filter(lambda user: not user.bot, self.bot.users)))}
**Total commands:** {len(self.bot.tree._get_all_commands())}
**Total cogs:** {len(self.bot.cogs)}
        '''
        )

        embed.add_field(name='Connection', value=f'''
**Up since:** <t:{self.bot.uptime}> - <t:{self.bot.uptime}:R>
**Latency:** {round(self.bot.latency * 1000)}ms
        '''
        )

        await interaction.response.send_message(embed=embed)

    async def show_user_information(self, interaction: Interaction, target: User or Member):
        user = await self.bot.fetch_user(target.id)

        embed = Embed(title=user)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        if user.banner: embed.set_image(url=user.banner.url)

        embed.add_field(name='User', inline=True, value=f'''
**ID:** {user.id}
**Type:** {"Bot" if user.bot else "User"}
**Flags:** {' '.join(list(map(lambda flag: constants.user_flags[flag], user.public_flags.all()))) or 'None'}
**Created at:** <t:{round(user.created_at.timestamp())}> - <t:{round(user.created_at.timestamp())}:R>
        '''
        )

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
    
    @app_commands.command(description='Show information about a Discord user')
    @app_commands.describe(
        target='Who you want to check the information of; if not provided, defaults to yourself'
    )
    async def user(self, interaction: Interaction, target: User = None):
        embed = (await self.show_user_information(interaction, target or interaction.user))

        await interaction.response.send_message(embed=embed)

    async def user_information(self, interaction: Interaction, target: User):
        embed = (await self.show_user_information(interaction, target or interaction.user))

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))