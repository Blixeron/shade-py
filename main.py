import os
import time

from discord import *
from discord.ext import commands

import config


class ShadeTree(app_commands.CommandTree):
    async def on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.BotMissingPermissions):
            missing = [
                perm.replace('_', ' ').replace('guild', 'server').title()
                for perm in error.missing_permissions
            ]

            if len(missing) > 2:
                permissions = '{}, and {}'.format(', '.join(missing[:-1]), missing[-1])
            else:
                permissions = ' and '.join(missing)

            await interaction.response.send_message(
                f'I need **{permissions}** permissions to run this command.',
                ephemeral=True,
            )
        else:
            await super().on_error(interaction, error)


initial_time = time.time()


class Shade(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            help_command=None,
            intents=Intents.all(),
            application_id=config.app_id,
            tree_cls=ShadeTree,
            owner_id=config.dev_id,
        )

        self.config = config

    @property
    def uptime(self):
        """Timestamp of when the bot started running."""
        return round(time.time() - (time.time() - initial_time))

    async def setup_hook(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')

        await bot.tree.sync()

    async def on_ready(self):
        print(f'{self.user} is ready. ID: {self.user.id}')


bot = Shade()

bot.run(config.token)
