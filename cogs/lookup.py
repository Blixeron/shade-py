from __future__ import annotations
from discord.ext import commands
from discord import *
from typing import TYPE_CHECKING
from .utils.time_formatter import iso_to_timestamp
import requests

if TYPE_CHECKING:
    from main import Shade

class Lookup(commands.Cog):
    """This Cog has commands tp lookup information from different sources of the internet."""
    
    def __init__(self, bot: Shade):
        self.bot: Shade = bot

    @app_commands.command(description='Check information from a GitHub user or repository')
    @app_commands.describe(search='What to search for; {username} for user lookup, and {username}/{repository} for repository lookup')
    async def github(self, interaction: Interaction, search: str):
        input = search.split('/')

        if len(input) < 2:
            res = requests.get(f'https://api.github.com/users/{input[0]}', headers={
                'Authorization': f'Bearer {self.bot.config.github_token}'
            })
            
            if res.status_code != 200:
                await interaction.response.send_message(
                    'An error occurred while requesting the information, or the user does not exist.',
                    ephemeral=True
                )
            else:
                lookup = res.json()
                
                embed = Embed(title=lookup['login'], description=lookup['bio'] or None)
                embed.set_thumbnail(url=lookup['avatar_url'])

                if lookup['twitter_username']:
                    twitter = '[@{0}](https://twitter.com/{0})'.format(lookup["twitter_username"])
                else:
                    twitter = 'Not provided'

                embed.add_field(name='Profile', inline=True, value=f'''
**Nickname:** {lookup['name'] or 'None'}
**Location:** {lookup['location'] or 'Not provided'}
**{lookup['following']}** following - **{lookup['followers']}** followers
                '''
                )

                embed.add_field(name='Contact', value=f'''
**Email:** {lookup['email'] or 'Not provided'}
**Twitter:** {twitter}
**Works at:** {lookup['company'] or 'Unknown'}
                '''
                )

                embed.add_field(name='Account Details', inline=False, value=f'''
**ID:** {lookup['id']}
**Type:** {lookup['type']}
**Created at:** <t:{round(iso_to_timestamp(lookup['created_at']))}> - <t:{round(iso_to_timestamp(lookup['created_at']))}:R>
**Updated at:** <t:{round(iso_to_timestamp(lookup['updated_at']))}> - <t:{round(iso_to_timestamp(lookup['updated_at']))}:R>
                '''
                )

                embed.add_field(name='Counts', inline=True, value=f'''
**Repositories:** {lookup['public_repos']}
**Gists:** {lookup['public_gists']}
                '''
                )

                embed.add_field(name='Links', value=f'''
**[User Overview]({lookup['html_url']})**{f' - **[Website]({lookup["blog"]})**' if lookup['blog'] else ''}
                '''
                )

                await interaction.response.send_message(embed=embed)
        else:
            res = requests.get(f'https://api.github.com/repos/{input[0]}/{input[1]}', headers={
                'Authorization': f'Bearer {self.bot.config.github_token}'
            })

            if res.status_code != 200:
                await interaction.response.send_message(
                    'An error occurred while requesting the information, the user does not exist or the repository could not be found.',
                    ephemeral=True
                )
            else:
                lookup = res.json()

                embed = Embed(title=lookup['full_name'], description=lookup['description'] or None)
                
                embed.add_field(name='Overview', inline=False, value=f'''
**Owner:** [{lookup['owner']['login']}]({lookup['owner']['html_url']})
**Topics:** {' - '.join(lookup['topics']) if lookup['topics'] else None}
**Created at:** <t:{round(iso_to_timestamp(lookup['created_at']))}> - <t:{round(iso_to_timestamp(lookup['created_at']))}:R>
**Last push:** <t:{round(iso_to_timestamp(lookup['pushed_at']))}> - <t:{round(iso_to_timestamp(lookup['pushed_at']))}:R>
                '''
                )

                embed.add_field(name='Repository Details', value=f'''
**Language:** {lookup['language'] or 'Unknown'}
**Default branch:** {lookup['default_branch']}
**Is a fork:** {'Yes' if lookup['fork'] else 'No'}
**Is forkable:** {'Yes' if lookup['allow_forking'] else 'No'}
**License:** {lookup['license']['name'] if lookup['license'] else None}
                '''
                )

                embed.add_field(name='Counts', inline=True, value=f'''
**Issues:** {lookup['open_issues']}
**Watchers:** {lookup['watchers']}
**Subscribers:** {lookup['subscribers_count']}
**Forks:** {lookup['forks']}
                '''
                )

                embed.add_field(name='Links', value=f'''
**[Repository Overview]({lookup['html_url']})**
{f'**[Homepage]({lookup["homepage"]})**' if lookup['homepage'] else ''}
                '''
                )

                await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Lookup(bot))