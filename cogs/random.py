from __future__ import annotations
from typing import TYPE_CHECKING
import random

from discord.ext import commands
from discord import *


if TYPE_CHECKING:
    from main import Shade


class Fun(commands.Cog):
    """Commands based on randomness and RNG."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    @app_commands.command(name='8ball')
    async def eightball(self, interaction: Interaction, question: app_commands.Range[str, 0, 1000]):
        """Ask a question to the magic 8 Ball.

        Args:
            question: What you want to ask?
        """
        
        answers = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', "I don't think so.", 'It is decidedly not.',
            'Outlook not so good.', 'Yes.', 'No.',
            'Take this 🛏️, so you can keep dreaming.', 'Yeah... no.', 'Bruh',
            'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
            "Don't count on it.", 'My sources say no.', 'Of course.',
            'Outlook good.', "Don't bet on it.", 'Yes, definitely.',
            'I say... no.', "I don't know.", "I don't care.",
            'What the hell is this question?', 'Are you seriously asking this?', "I'm not sure.",
            "✨ Y E S ✨", "✨ N O ✨", "✨ I D K ✨"
        ]
            
        await interaction.response.send_message(
            (
                f'{question if question.endswith("?") else f"{question}?"}\n'
                f'🎱 **{random.choice(answers)}**'
            ),
            allowed_mentions=AllowedMentions.none())
            
    @app_commands.command()
    async def percentage(
            self, interaction: Interaction,
            target: app_commands.Range[str, 0, 500],
            calculation: app_commands.Range[str, 0, 500]):
        """Rate how much percentage of anything is someone or something.

        Args:
            target: What or who you want to calculate the percentage of.
            calculation: What you want to calculate?
        """

        await interaction.response.send_message(
            f'{target} is **{random.randint(0, 100)}%** {calculation}.',
            allowed_mentions=AllowedMentions.none())


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))