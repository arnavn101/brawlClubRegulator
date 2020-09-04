import configparser
import os

import requests
from discord import Embed

from commands.base_command import BaseCommand


class ReturnBrawler(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Get Brawler Info"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.star_api = str(self.config.get('ConfigInfo', 'STAR_API_KEY'))

        # Headers for authentication
        self.starlist_url = "https://api.starlist.pro/v1/brawlers"
        self.headers = {
            'Authorization': self.star_api,
        }

        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["brawler_name"]

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
        data_brawlers = response_starlist.json()

        try:
            brawler_name = (str(params[0])).lower()

            for individual_brawler in data_brawlers:
                if brawler_name in (individual_brawler["name"].replace(" ", "")).lower():
                    embed_msg = Embed(title=f'{individual_brawler["name"]}', color=0x00ff00)
                    embed_msg.set_image(url=individual_brawler["imageUrl"])
                    embed_msg.add_field(name="Brawler Rarity", value=individual_brawler["rarity"], inline=False)
                    embed_msg.add_field(name="Brawler Class", value=individual_brawler["class"], inline=False)
                    embed_msg.add_field(name="Brawler Description", value=individual_brawler["description"],
                                        inline=False)

                    brawler_starPowers = individual_brawler["starPowers"]

                    star_powersList = [d['name'] for d in brawler_starPowers]
                    star_powersString = (", ".join(star_powersList))
                    embed_msg.add_field(name="Brawler Star Powers", value=star_powersString, inline=False)

                    embed_msg.set_footer(text=user_name, icon_url=member_object.avatar_url)
                    await message.channel.send(embed=embed_msg)
                    break

        except Exception as e:
            print(e)
            await message.channel.send(
                "Please, provide valid brawler name")
            return
