import os

import brawlstats
import configparser
from utilities import database
from discord import Embed
from discord.utils import find

from commands.base_command import BaseCommand


class DebugDB(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Info from Club Database"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["discord_id"]

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

        brawl_client = brawlstats.Client(self.brawl_api)
        brawl_database = database.SQL_Server()
        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return
        try:
            discord_id = str(message.mentions[0].id)
            message_author = str(message.author)
            mentioned_object = activeServers.get_member_named(message_author)
        except Exception:
            await message.channel.send(
                "Please, provide valid Discord Id")
            return

        if not brawl_database.information_present(discord_id):
            player_club = False
        else:
            player_info = brawl_client.get_player((brawl_database.view_information_user(discord_id)).upper())
            player_club = player_info.club.name

        embed_msg = Embed(title='User Information', color=0x00ff00)
        embed_msg.add_field(name="User Tag", value=brawl_database.view_information_user(discord_id), inline=False)
        embed_msg.add_field(name="User Club", value=player_club, inline=False)
        embed_msg.add_field(name="User Warning", value=brawl_database.return_userWarning(discord_id), inline=False)
        embed_msg.set_footer(text=discord_id, icon_url=mentioned_object.avatar_url)

        await message.channel.send(embed=embed_msg)
