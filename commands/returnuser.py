import os

import brawlstats
import configparser
from discord import Embed

from commands.base_command import BaseCommand


class ReturnUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Retrieve brawl stars id"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["user_name"]

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
        player_id = str(params[0])
        brawl_client = brawlstats.Client(self.brawl_api)
        list_clubs = [line.rstrip() for line in open(os.path.join('config_files','tags.txt'))];print(list_clubs)

        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(user_name)
        variable_set = False

        for i in range(len(list_clubs)):
            if variable_set:
                break
            
            club = brawl_client.get_club((list_clubs[i]).upper())
            club_name = club.name
            club_info = club.members
            embed_msg = Embed(title=f'{club_name} Member', color=0x00ff00)

            for member in club_info:
                if  player_id.lower() in (member.name.replace(" ", "")).lower():
                    embed_msg.add_field(name="Player Name", value=member.name, inline=True)
                    embed_msg.add_field(name="Player Tag", value=member.tag, inline=True)
                    embed_msg.add_field(name="Player Trophies", value=member.trophies, inline=True)
                    embed_msg.set_footer(text=user_name, icon_url = member_object.avatar_url)
                    variable_set = True
                    break
        
        if variable_set:
            await message.channel.send(embed=embed_msg)
        else:
            msg = f" The User {player_id} does not exist in the clubs"
            await message.channel.send(msg)
