from __future__ import annotations
from discord import *
from discord.ext import commands
import utils.http
import random
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Dust

class Fun(commands.Cog):
    """Commands made for fun and enjoyment."""

    def __init__(self, bot: Dust):
        self.bot: Dust = bot

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
    async def how(
        self,
        interaction: Interaction,
        target: app_commands.Range[str, 0, 500],
        input: app_commands.Range[str, 0, 500]
    ):
        await interaction.response.send_message(
            f'{target} is **{random.randint(0, 100)}%** {input}.'
        )

    @app_commands.command(name='cat', description='Show a cat image and a cat fact. 😺')
    async def cat(self, interaction: Interaction):
        await interaction.response.defer()

        future_fact = utils.http.get_json('https://catfact.ninja/fact')
        future_image = utils.http.get_json('https://api.thecatapi.com/v1/images/search?limit=1&size=full', {
            'x-api-key': self.bot.config.cat_api_key
        })

        fact_json, image_json = await asyncio.gather(future_fact, future_image)

        embed = Embed(title='Cat fact!', description=fact_json['fact'])
        embed.set_image(url=image_json[0]['url'])

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='dog', description='Show a dog image and a dog fact. 🐶')
    async def dog(self, interaction: Interaction):
        await interaction.response.defer()

        future_fact = utils.http.get_json('https://dog-api.kinduff.com/api/facts')
        future_image = utils.http.get_json('https://api.thedogapi.com/v1/images/search?limit=1&size=full', {
            'x-api-key': self.bot.config.cat_api_key
        })

        fact_json, image_json = await asyncio.gather(future_fact, future_image)

        embed = Embed(title='Dog fact!', description=fact_json['facts'][0])
        embed.set_image(url=image_json[0]['url'])

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))