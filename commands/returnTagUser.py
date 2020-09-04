import os

import configparser
from utilities import database
from discord import Embed

from commands.base_command import BaseCommand


class ReturnTagUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Return Discord id associated with the tag"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["player_tag"]

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
        brawl_database = database.SQL_Server()

        try:
            player_tag = str(params[0])
        except Exception:
            await message.channel.send(
                                      "Please, provide valid Player Tag")
            return

        tag_user = brawl_database.returnTagUser(player_tag)
        embed_msg = Embed(title='Tag Information', color=0x00ff00)
        embed_msg.add_field(name="Discord Id", value=tag_user, inline=False)

        if tag_user and tag_user in activeServers.members:
            mentioned_object = activeServers.get_member_named(tag_user)
            embed_msg.set_footer(text=tag_user, icon_url=mentioned_object.avatar_url)
        else:
            embed_msg.set_footer(text=user_name, icon_url=member_object.avatar_url)

        await message.channel.send(embed=embed_msg)


