import os

import brawlstats
import configparser
from discord import Embed

from commands.base_command import BaseCommand


class ReturnTop5(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Retrieve top 5 members of a club"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["club_id"]

        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        user_name = str(message.author)
        club_id = str(params[0])
        brawl_client = brawlstats.Client(self.brawl_api)
        list_clubs = [line.rstrip() for line in open(os.path.join('config_files', 'tags.txt'))]

        if "#" in club_id:
            club = brawl_client.get_club(club_id.upper())
            club_name = club.name
            club_info = club.members
        elif int(club_id) in range(len(list_clubs)):
            club_id = int(club_id) - 1
            club = brawl_client.get_club((list_clubs[club_id]).upper())
            club_name = club.name
            club_info = club.members

        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(user_name)

        embed_msg = Embed(title=f'{club_name} Club List', color=0x00ff00)

        for i in range(5):
            try:
                embed_msg.add_field(name="Player Name", value=club_info[i].name, inline=True)
                embed_msg.add_field(name="Player Tag", value=club_info[i].tag, inline=True)
                embed_msg.add_field(name="Player Trophies", value=club_info[i].trophies, inline=True)
            except Exception:
                break

        embed_msg.set_footer(text=user_name, icon_url=member_object.avatar_url)

        await message.channel.send(embed=embed_msg)
