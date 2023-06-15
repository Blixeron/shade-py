from __future__ import annotations
import os
from typing import TYPE_CHECKING

from discord.ext import commands
from discord import *


if TYPE_CHECKING:
    from main import Shade


class Owner(commands.Cog):
    """Commands for the bot developer."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    async def reload_modules(self, ctx: commands.Context, module: str = None) -> str:
        if module:
            try:
                await self.bot.reload_extension(f'cogs.{module}')
            except commands.ExtensionError as e:
                return await ctx.reply('{}: {}'.format(type(e).__name__, e))
            else:
                return await ctx.reply(f'`{module.capitalize()}` has been reloaded.')
        else:
            success = False

            for file in os.listdir('./cogs'):
                try:
                    if file.endswith('.py'):
                        await self.bot.reload_extension(f'cogs.{file[:-3]}')
                except commands.ExtensionError as e:
                    await ctx.reply('{}: {}'.format(type(e).__name__, e))
                    break
                else:
                    success = True

            if success:
                return await ctx.reply('All cogs have been reloaded.')

    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, module: str = None):
        """Reloads a module or all of them."""

        await self.reload_modules(ctx, module)

    @commands.command(aliases=['s'], hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """Synchronizes the command tree."""

        await self.reload_modules(ctx)

        try:
            await self.bot.tree.sync()
        except app_commands.CommandSyncFailure as e:
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send(f'The command tree has been synced globally.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
