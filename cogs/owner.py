from discord.ext import commands
from discord import *
from contextlib import redirect_stdout

import io
import textwrap
import traceback
import asyncio
import subprocess
import requests

class Owner(commands.Cog):
    """Commands for the bot developer."""

    def __init__(self, bot):
        self.bot = bot

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
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e: SyntaxError) -> str:
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *, module : str):
        """Loads a mddule."""
        try:
            await ctx.message.add_reaction('\u2705')
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply(f'{module.capitalize()} Cog loaded.')

    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, module: str):
        """Reloads a module."""
        try:
            await ctx.message.add_reaction('\u2705')
            self.bot.reload_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.reply(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.reply(f'{module.capitalize()} Cog reloaded.')

    @commands.command(aliases=['eval'], hidden=True)
    @commands.is_owner()
    async def evaluate(self, ctx: commands.Context, *, body: str):
        """Evaluates code."""
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'requests': requests
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
