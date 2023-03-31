from __future__ import annotations
from discord.ext import commands
from discord import *
from typing import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Dust

class Utility(commands.Cog):
    """The description for Utility goes here."""

    def __init__(self, bot: Dust):
        self.bot: Dust = bot

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

        return {
            'url': f'{avatar.with_format(extension.lower()).with_size(size)}',
            'target': target,
            'size': size,
            'format': format,
            'server': server,
            'property': avatar
        }

    @app_commands.command(name='avatar', description='Show the avatar of someone')
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
        avatar = (await self.show_avatar(interaction, target or interaction.user, size or 1024, format or None, server))

        embed = Embed(
            title=avatar['target'],
            description=f'''**{avatar["size"]}** pixels, in **{avatar["format"]}** format
{"**Server Avatar**" if avatar["property"] is Member.guild_avatar else "**Default Avatar**"}'''
        ).set_image(url=avatar["url"])

        await interaction.response.send_message(embed=embed)

    async def user_avatar(self, interaction: Interaction, target: User):
        avatar = (await self.show_avatar(interaction, target))

        embed = Embed(
            title=avatar['target'],
            description=f'''**{avatar["size"]}** pixels, in **{avatar["format"]}** format
{"**Server Avatar**" if avatar["property"] is Member.guild_avatar else "**Default Avatar**"}'''
        ).set_image(url=avatar["url"])

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
