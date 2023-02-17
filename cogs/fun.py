from discord import *
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Commands made for fun and enjoyment."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='8ball', description='Ask the magic 8 Ball a question')
    @app_commands.describe(question='Ask something')

    async def eightball(self, interaction: Interaction, question: app_commands.Range[str, 0, 1000]):
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

        await interaction.response.send_message(
            f'{question if question.endswith("?") else f"{question}?"}\n**{random.choice(answers)}**'
        )


    @app_commands.command(name='how', description='Rate how much of anything is someone or something')
    @app_commands.describe(
        target='Type in what or who you want to calculate the percentage of',
        input='Type in what you want to calculate'
    )

    async def how(self, interaction: Interaction, target: app_commands.Range[str, 0, 500], input: app_commands.Range[str, 0, 500]):
        await interaction.response.send_message(
            f'{target} is **{random.randint(0, 100)}%** {input}.'
        )

async def setup(bot):
    await bot.add_cog(Fun(bot))
