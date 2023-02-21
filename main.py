import os
from discord import *
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class Dust(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            help_command=None,
            intents=Intents.all(),
            application_id=os.getenv('APP_ID')
        )

    async def setup_hook(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')
        
        await bot.tree.sync()

    async def on_ready(self):
        print(f'{self.user} is ready. ID: {self.user.id}')

bot = Dust()

bot.run(os.getenv('TOKEN'))