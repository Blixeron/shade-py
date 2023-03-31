from __future__ import annotations
import os
from discord.ext import commands
from discord import *
from contextlib import redirect_stdout
import utils.http as http
import io
import textwrap
import traceback
import asyncio
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Dust

class Owner(commands.Cog):
    """Commands for the bot developer."""

    def __init__(self, bot: Dust):
        self.bot: Dust = bot

    @property
    async def run_process(self, command: str) -> list[str]:
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e: SyntaxError) -> str:
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *, module: str):
        """Loads a mddule."""
        try:
            await ctx.message.add_reaction('<:loading:1091424189270986822>')
            await self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
            await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))
        else:
            await ctx.reply(f'{module.capitalize()} Cog loaded.')
            await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))

    async def reload_modules(self, ctx: commands.Context, module: str = None) -> str:
        if module:
            try:
                await ctx.message.add_reaction('<:loading:1091424189270986822>')
                await self.bot.reload_extension(f'cogs.{module}')
            except commands.ExtensionError as e:
                response = '{}: {}'.format(type(e).__name__, e)
                await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))
            else:
                response = f'`{module.capitalize()}` has been reloaded.'

            return response
        else:
            success = False

            for file in os.listdir('./cogs'):
                try:
                    await ctx.message.add_reaction('<:loading:1091424189270986822>')
                    if file.endswith('.py'): await self.bot.reload_extension(f'cogs.{file[:-3]}')
                except commands.ExtensionError as e:
                    response = '{}: {}'.format(type(e).__name__, e)
                    await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))
                    break
                else:
                    success = True

            if success: response = 'All Cogs have been reloaded.'

            return response

    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, module: str = None):
        """Reloads a module or all of them."""

        await ctx.reply(await self.reload_modules(ctx, module))
        await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """Synchronizes the command tree."""

        await ctx.message.add_reaction('<:loading:1091424189270986822>')

        try:
            await self.bot.tree.sync()
        except app_commands.CommandSyncFailure as e:
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply('The command tree has been synced globally.')
            await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))

    @commands.command(aliases=['rls'], hidden=True)
    @commands.is_owner()
    async def reloadandsync(self, ctx: commands.Context, *, module: str = None):
        """Reloads a module or all of them, and synchronizes the command tree."""

        response = await self.reload_modules(ctx, module)

        try:
            await self.bot.tree.sync()
        except app_commands.CommandSyncFailure as e:
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply(f'{response.replace(".", "")}, and the command tree has been synced globally.')
            await ctx.message.remove_reaction('<:loading:1091424189270986822>', Object(id=ctx.me.id))

    @commands.command(aliases=['eval'], hidden=True)
    @commands.is_owner()
    async def evaluate(self, ctx: commands.Context, *, body: str):
        """Evaluates code."""
        env = {
            'http': http,
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            await ctx.reply(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.reply(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.reply(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.reply(f'```py\n{value}{ret}\n```')

async def setup(bot):
    await bot.add_cog(Owner(bot))