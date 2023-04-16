from __future__ import annotations
from discord.ext import commands
from discord import *
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from main import Shade

class Utility(commands.Cog):
    """The description for Utility goes here."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

        self.avatar_ctx_menu = app_commands.ContextMenu(
            name='User Avatar',
            callback=self.user_avatar
        )
        self.bot.tree.add_command(self.avatar_ctx_menu)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.avatar_ctx_menu.name, type=self.avatar_ctx_menu.type)

    async def show_avatar(
        self,
        interaction: Interaction,
        target: User or Member,
        size: int = 1024,
        format: str = 'PNG' or 'GIF',
        server: bool = False
    ):
        avatar = target.avatar
        avatar_hash = target.avatar.key

        if server:
            if interaction.guild and interaction.guild.get_member(target.id) is not None:
                member = (await interaction.guild.fetch_member(target.id))

                if member.guild_avatar:
                    avatar = member.guild_avatar
                    avatar_hash = member.guild_avatar.key

        extension = format

        if format:
            if format == 'GIF':
                extension = 'GIF' if avatar_hash.startswith('a_') else 'PNG'
        else:
            extension = 'GIF' if avatar_hash.startswith('a_') else 'PNG'

        embed = Embed(
            title=target,
            description=f'''**{size}** pixels, in **{format}** format
{"**Server Avatar**" if avatar is Member.guild_avatar else "**Default Avatar**"}'''
        ).set_image(url=avatar.with_format(extension.lower()).with_size(size))

        return embed

    @app_commands.command(description='Show the avatar of someone')
    @app_commands.describe(
        target='Who you want to check the avatar of; if not provided, defaults to yourself',
        size='Size of the image, defaults to 1024 pixels',
        format='Format of the image, defaults to png or gif if the avatar is animated',
        server='Whether to show the server avatar (if any) or not'
    )
    async def avatar(
        self,
        interaction: Interaction,
        target: User = None,
        size: Literal[128, 256, 512, 1024, 2048, 4096] = 1024,
        format: Literal['JPG', 'PNG', 'JPEG', 'WEBP', 'GIF'] = 'PNG' or 'GIF',
        server: bool = False
    ):
        embed = (await self.show_avatar(interaction, target or interaction.user, size or 1024, format or None, server))

        await interaction.response.send_message(embed=embed)

    async def user_avatar(self, interaction: Interaction, target: User):
        embed = (await self.show_avatar(interaction, target))

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.guild_only
    @app_commands.command(description='Show the current server icon')
    @app_commands.describe(
        size='Size of the image, defaults to 1024 pixels',
        format='Format of the image, defaults to png or gif if the avatar is animated'
    )
    async def icon(
        self,
        interaction: Interaction,
        size: Literal[128, 256, 512, 1024, 2048, 4096] = 1024,
        format: Literal['JPG', 'PNG', 'JPEG', 'WEBP', 'GIF'] = 'PNG' or 'GIF'
    ):
        if not interaction.guild.icon:
            await interaction.response.send_message('This server does not have an icon.', ephemeral=True)
        else:
            extension = format

            if format:
                if format == 'GIF':
                    extension = 'GIF' if interaction.guild.icon.key.startswith('a_') else 'PNG'
            else:
                extension = 'GIF' if interaction.guild.icon.key.startswith('a_') else 'PNG'

            embed = Embed(
                title=interaction.guild.name,
                description=f'**{size}** pixels, in **{format}** format'
            ).set_image(url=interaction.guild.icon.with_format(extension.lower()).with_size(size))

            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))