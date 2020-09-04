import configparser
import os

import requests
from discord import Embed

from commands.base_command import BaseCommand


class ReturnMap(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Get Current Maps"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.star_api = str(self.config.get('ConfigInfo', 'STAR_API_KEY'))

        # Headers for authentication
        self.starlist_url = "https://api.starlist.pro/v1/events"
        self.headers = {
            'Authorization': self.star_api,
        }

        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["map_name"]

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
        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(user_name)

        # Request current maps
        response_starlist = requests.request("GET", self.starlist_url, headers=self.headers)
        data_maps = response_starlist.json()

        current_events = data_maps["current"]

        try:
            map_name = str(params[0])
        
            for individual_event in current_events:
                if map_name.lower() in (individual_event["gameMode"].replace(" ", "")).lower():
                    embed_msg = Embed(title=f'{individual_event["gameMode"]}', color=0x00ff00)
                    embed_msg.set_image(url=individual_event["mapImageUrl"])
                    embed_msg.add_field(name="Map Name", value=individual_event["mapName"], inline=False)
                    embed_msg.set_footer(text=user_name, icon_url = member_object.avatar_url)

                    await message.channel.send(embed=embed_msg)

        except Exception:
            await message.channel.send(
                                      "Please, provide valid map name")
            return

