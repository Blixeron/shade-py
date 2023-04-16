from __future__ import annotations
from discord import *
from discord.ext import commands
import time
import random
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Shade

class Fun(commands.Cog):
    """Commands made for fun and enjoyment."""

    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    random = app_commands.Group(name='random', description='Tools based on randomness')

    @random.command(name='8ball', description='Ask the magic 8 Ball a question')
    @app_commands.describe(question='Ask something')
    async def eightball(self, interaction: Interaction, question: app_commands.Range[str, 0, 1000]):
        res = requests.get(f'https://eightballapi.com/api?question={question}&lucky=false')

        if res.status_code != 200:
            interaction.response.send_message(
                'Oops, looks like I dropped the 8 Ball... Maybe come back later?',
                ephemeral=True
            )
        else:
            answer = res.json()
            
            await interaction.response.send_message(
                f'{question if question.endswith("?") else f"{question}?"}\n🎱 **{answer["reading"]}**',
                allowed_mentions=AllowedMentions.none()
            )

    @random.command(description='Rate how much of anything is someone or something')
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
            f'{target} is **{random.randint(0, 100)}%** {input}.',
            allowed_mentions=AllowedMentions.none()
        )

    @random.command(description='Do a coin flip')
    async def coinflip(self, interaction: Interaction):
        await interaction.response.send_message('🪙')
        
        time.sleep(1)

        await interaction.edit_original_response(content=f'The coin landed on **{random.choice(["heads", "tails"])}!**')

    @app_commands.command(description='Show a cat image and a cat fact 😺')
    async def cat(self, interaction: Interaction):
        fact = requests.get('https://catfact.ninja/fact')
        image = requests.get('https://api.thecatapi.com/v1/images/search?limit=1&size=full', headers={
            'x-api-key': self.bot.config.cat_api_key
        })

        if fact.status_code != 200 or image.status_code != 200:
            interaction.response.send_message(
                'An error occurred while getting the fact or the image.',
                ephemeral=True
            )
        else:
            embed = Embed(title='Cat fact!', description=fact.json()['fact'])
            embed.set_image(url=image.json()[0]['url'])

            await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Show a dog image and a dog fact 🐶')
    async def dog(self, interaction: Interaction):
        fact = requests.get('https://dog-api.kinduff.com/api/facts')
        image = requests.get('https://api.thedogapi.com/v1/images/search?limit=1&size=full', headers={
            'x-api-key': self.bot.config.cat_api_key
        })

        if fact.status_code != 200 or image.status_code != 200:
            interaction.response.send_message(
                'An error occurred while getting the fact or the image.',
                ephemeral=True
            )
        else:
            embed = Embed(title='Dog fact!', description=fact.json()['facts'][0])
            embed.set_image(url=image.json()[0]['url'])

            await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Show a random meme from Reddit')
    async def meme(self, interaction: Interaction):
        res = requests.get(f'https://meme-api.com/gimme/{random.choice(["meme", "memes"])}')

        if res.status_code != 200:
            interaction.response.send_message(
                'An error occurred while getting the meme.',
                ephemeral=True
            )
        else:
            meme = res.json()
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