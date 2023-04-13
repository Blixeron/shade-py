from __future__ import annotations
from discord import *
from discord.ext import commands
import random
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Shade

class Fun(commands.Cog):
    """Commands made for fun and enjoyment."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    @app_commands.command(name='8ball', description='Ask the magic 8 Ball a question')
    @app_commands.describe(question='Ask something')
    async def eightball(self, interaction: Interaction, question: app_commands.Range[str, 0, 1000]):
        answers = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', "I don't think so.", 'It is decidedly not.',
            'Yes.', 'No.', 'Take this 🛏️, so you can keep dreaming.', 'Yeah... no.',
            'Bruh.', 'Signs point to yes.', 'Reply hazy, try again.',
            'Ask again later.', 'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', "Don't count on it.", 'My sources say no.',
            'Of course.', "Don't bet on it.", 'Yes, definitely.',
            'My reply is no.', "I don't know.", "I don't care.",
            'What the hell is this question?', 'Are you seriously asking this?', "I'm not sure.",
            '✨ Y E S ✨', '✨ N O ✨', '✨ I D K ✨'
        ]

        await interaction.response.send_message(
            f'{question if question.endswith("?") else f"{question}?"}\n🎱 **{random.choice(answers)}**'
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

    @app_commands.command(name='cat', description='Show a cat image and a cat fact 😺')
    async def cat(self, interaction: Interaction):
        await interaction.response.defer()

        fact = requests.get('https://catfact.ninja/fact')
        image = requests.get('https://api.thecatapi.com/v1/images/search?limit=1&size=full', headers={
            'x-api-key': self.bot.config.cat_api_key
        })

        embed = Embed(title='Cat fact!', description=fact.json()['fact'])
        embed.set_image(url=image.json()[0]['url'])

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='dog', description='Show a dog image and a dog fact 🐶')
    async def dog(self, interaction: Interaction):
        await interaction.response.defer()

        fact = requests.get('https://dog-api.kinduff.com/api/facts')
        image = requests.get('https://api.thedogapi.com/v1/images/search?limit=1&size=full', headers={
            'x-api-key': self.bot.config.cat_api_key
        })

        embed = Embed(title='Dog fact!', description=fact.json()['facts'][0])
        embed.set_image(url=image.json()[0]['url'])

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='meme', description='Show a random meme from Reddit')
    async def meme(self, interaction: Interaction):
        meme = requests.get(f'https://meme-api.com/gimme/{random.choice(["meme", "memes"])}').json()

        embed = Embed(title=meme['title'], description=f'''
**By [u/{meme['author']}](https://reddit.com/user/{meme['author']} "{meme['author']}")**
[Jump to post]({meme['postLink']})
        '''
        )

        embed.set_image(url=meme['url'])
        embed.set_footer(text=f'{meme["ups"]} upvotes')

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))