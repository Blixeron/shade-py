from discord import *
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='8ball',
        description='Ask the magic 8 Ball a question'
    )
    @app_commands.describe(question='Ask something')
    async def eightball(self, interaction: Interaction, question: str):
        answers = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', "I don't think so.", 'It is decidedly not.',
            'Outlook not so good.', 'Yes.', 'No.',
            'Take this 🛏️, so you can keep dreaming.', 'Yeah... no.', 'Bruh.',
            'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
            "Don't count on it.", 'My sources say no.', 'Of course.',
            'Outlook good.', "Don't bet on it.", 'Yes, definitely.',
            'My reply is no.', "I don't know.", "I don't care.",
            'What the hell is this question?', 'Are you seriously asking this?', "I'm not sure.",
            '✨ Y E S ✨', '✨ N O ✨', '✨ I D K ✨'
        ]

        if len(question) > 1900:
            await interaction.response.send_message(
                "That's a bit too long for me to answer...", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'{question if question.endswith("?") else f"{question}?"}\n**{random.choice(answers)}**'
            )

async def setup(bot):
    await bot.add_cog(Fun(bot))
